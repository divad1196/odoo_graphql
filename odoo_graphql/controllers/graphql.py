from base64 import b64decode
from datetime import datetime
import json
import logging
from time import sleep

import werkzeug
from odoo import http, api
from odoo.http import request, Registry
from dataclasses import dataclass
from typing import Optional, Any
import threading
from contextlib import contextmanager, suppress
from odoo.service.common import exp_login

_logger = logging.getLogger(__name__)


# Based on _serve_db and _open_registry function
def _build_env(db_name, uid, context):
    registry = Registry(db_name)
    cr = registry.cursor(readonly=True)
    registry = registry.check_signaling(cr)
    threading.current_thread().dbname = registry.db_name
    return api.Environment(cr, uid, context)

@contextmanager
def with_env(db_name, uid, context):
    # current_dbname = threading.current_thread().dbname
    try:
        registry = Registry(db_name)
        cr = registry.cursor(readonly=True)
        registry = registry.check_signaling(cr)
        threading.current_thread().dbname = registry.db_name
        yield api.Environment(cr, uid, context)
    except Exception as e:
        _logger.error(f"An unexpected error happened: {e}")
        raise
    finally:
        cr.close()
        # threading.current_thread().dbname = current_dbname



def serialize_sse_field(field: str, value: str) -> str:
    value = value.replace("\n", "\\n").replace("\0", "")
    return f"""{field}: {value}\n"""

# https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events
@dataclass
class ServerSideEvent:
    data: Any
    event: Optional[str] = None
    id: Optional[str] = None
    retry: Optional[int] = None
    
    @property
    def serialized_data(self) -> str:
        if isinstance(self.data, str):
            return self.data
        return json.dumps(self.data)
    
    def dumps(self) -> str:
        lines = []
        if self.id:
            lines.append(serialize_sse_field("id", self.id))
        if self.event:
            lines.append(serialize_sse_field("event", self.event))
        if self.retry and self.retry > 0:
            lines.append(serialize_sse_field("retry", str(self.retry)))

        lines.append(serialize_sse_field("data", self.serialized_data))
        lines.append("")  # End of message
        return "\n".join(lines)


# https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
def to_sse_stream(stream): 
    def sse(stream):
        for e in stream:
            sse = ServerSideEvent(data=e)
            yield sse.dumps()

    headers = [
        ("X-Accel-Buffering", "no"),
        ("Content-Type", "text/event-stream"),
        ("Cache-Control", "no-cache"),
    ]
    return request.make_response(
        sse(stream),
        headers=headers,
        # mimetype="application/octet-stream",
        # direct_passthrough=True,
    )

def get_uid(env, query):
    try:  # Usual format is json with "query" and "variables" entries
        data = json.loads(query)
        query = data["query"]

        auth = data.get("auth", {})
        if not auth:
            return None
        login = auth.get("login")
        if not login:
            login = auth.get("username")
        password = auth.get("password")
        if login and password:
            uid = exp_login(
                env.cr.dbname,
                login,
                password,
            )
            return uid
    except Exception:  # We may have pure graphql query
        _logger.debug("Pure graphql query received")

class GraphQL(http.Controller):

    @http.route(
        "/graphql-sse",
        auth="public",
        type="http",
        website=True,
        sitemap=False,
        csrf=False,
    )
    def graphql_sse(self, query: str):
        uid = get_uid(request.env, query) or request.uid

        # query = request.httprequest.data.decode()  # request.graphqlrequest
        with suppress(Exception):
            query = b64decode(query).decode()
        now = datetime.now()
        response, check_for_changes_functions = request.env["graphql.handler"].handle_query_with_checks(query)
        if check_for_changes_functions is None:
            return to_sse_stream([response])
        
        dbname, context = request.db, request.context
        def stream():
            nonlocal now
            nonlocal response
            nonlocal check_for_changes_functions
            yield response

            while True:
                sleep(5)
                # We need a new `env` everytime we check
                # Otherwise, the changes won't be percieved (transactional mode)
                with with_env(dbname, uid, context) as env:

                    changes_found = False
                    try:
                        changes_found = any(f(env, now) for f in check_for_changes_functions)
                    except Exception as e:
                        _logger.error(f"When checking for changes: {e}")
                    if not changes_found:
                        continue
                    now = datetime.now()
                    response, check_for_changes_functions = env["graphql.handler"].handle_query_with_checks(query)
                    yield response
                
        return to_sse_stream(stream())


    # This route is just a test for Graphql Subscriptions
    @http.route(
        "/graphql",
        auth="public",
        type="http",
        website=True,
        sitemap=False,
        csrf=False,
    )
    def graphql(self):
        query = request.httprequest.data.decode()  # request.graphqlrequest
        env = request.env
        # TODO: Fix login through embedded params
        # uid = get_uid(env, query)
        # if uid is not None:
        #     env = env.with_user(uid)
        response, _ = env["graphql.handler"].handle_query_with_checks(query)
        return json.dumps(response, indent=4)
        
    # @http.route(
    #     "/graphql-full",
    #     auth="public",
    #     type="http",
    #     website=True,
    #     sitemap=False,
    #     csrf=False,
    # )
    # def full_graphql(self):
    #     # query = request.httprequest.data.decode()  # request.graphqlrequest
    #     # query = """
    #     # subscription Test {
    #     #     SaleOrder(domain: [["id", "=", 41]]) {
    #     #         name
    #     #         state
    #     #         note
    #     #     }
    #     # }
    #     # """
    #     query = request.httprequest.data.decode()  # request.graphqlrequest
    #     now = datetime.now()
    #     response, check_for_changes_functions = request.env["graphql.handler"].handle_query_with_checks(query)
    #     if check_for_changes_functions is None:
    #         return json.dumps(response, indent=4)
        
    #     dbname, uid, context = request.db, request.uid, request.context
    #     def stream():
    #         nonlocal now
    #         nonlocal response
    #         nonlocal check_for_changes_functions
    #         yield response

    #         while True:
    #             sleep(5)
    #             # We need a new `env` everytime we check
    #             # Otherwise, the changes won't be percieved (transactional mode)
    #             with with_env(dbname, uid, context) as env:

    #                 changes_found = False
    #                 try:
    #                     changes_found = any(f(env, now) for f in check_for_changes_functions)
    #                 except Exception as e:
    #                     _logger.error(f"When checking for changes: {e}")
    #                 if not changes_found:
    #                     continue
    #                 now = datetime.now()
    #                 response, check_for_changes_functions = env["graphql.handler"].handle_query_with_checks(query)
    #                 yield response
                
    #     return to_sse_stream(stream())

    # @http.route(
    #     "/graphql",
    #     auth="public",
    #     type="http",
    #     website=True,
    #     sitemap=False,
    #     csrf=False,
    # )
    # def graphql(self):
    #     # https://spec.graphql.org/June2018/#sec-Response-Format
    #     query = request.httprequest.data.decode()  # request.graphqlrequest
    #     response = request.env["graphql.handler"].handle_query(query)
    #     return json.dumps(response, indent=4)

    @http.route("/graphiql", type="http", website=True, sitemap=False)
    def graphiql(self):
        introspection = request.env["graphql.handler"].has_introspection()
        if not introspection:
            raise werkzeug.exceptions.NotFound()
            # raise ValidationError("Introspection is not allowed")
        return request.render("odoo_graphql.graphiql")
