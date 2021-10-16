import odoo
from odoo.http import Root
from odoo.http import WebRequest, Response, request  # Http
from odoo.http import (
    serialize_exception,
    SessionExpiredException,
    AuthenticationError,
)  # Exceptions
from odoo.http import memory_info, psutil  # Tools
import werkzeug.exceptions
import pprint
import time
import os
import json

from graphql import parse
from .utils import parse_document

import logging

_logger = logging.getLogger(__name__)
rpc_request = logging.getLogger(__name__ + ".rpc.request")
rpc_response = logging.getLogger(__name__ + ".rpc.response")

MIMETYPE = "application/graphql"

# Based on JsonRequest, TODO: Documentation
class GraphQLRequest(WebRequest):
    """Request handler for GraphQL over HTTP

    Sucessful request::

      --> {"jsonrpc": "2.0",
           "method": "call",
           "params": {"context": {},
                      "arg1": "val1" },
           "id": null}

      <-- {"jsonrpc": "2.0",
           "result": { "res1": "val1" },
           "id": null}

    Request producing a error::

      --> {"jsonrpc": "2.0",
           "method": "call",
           "params": {"context": {},
                      "arg1": "val1" },
           "id": null}

      <-- {"jsonrpc": "2.0",
           "error": {"code": 1,
                     "message": "End user error message.",
                     "data": {"code": "codestring",
                              "debug": "traceback" } },
           "id": null}

    """

    # _request_type = "graphql"
    _request_type = "http"

    def __init__(self, *args):
        super(GraphQLRequest, self).__init__(*args)

        self.params = {}

        # args = self.httprequest.args
        # request = None
        # request_id = args.get('id')

        # regular jsonrpc2
        request = self.httprequest.get_data().decode(self.httprequest.charset)

        # Read POST content or POST Form Data named "request"
        try:
            self.graphqlrequest = request
        except ValueError:
            msg = "Invalid QraphQL data: %r" % (request,)
            _logger.info("%s: %s", self.httprequest.path, msg)
            raise werkzeug.exceptions.BadRequest(msg)

        # self.params = dict(self.graphqlrequest.get("params", {}))
        self.context = self.session.context

    def _graphql_response(self, result=None, error=None):
        if isinstance(result, Response):
            return result
        body = json.dumps(result)

        return Response(
            body,
            status=error and error.pop("http_status", 200) or 200,
            headers=[("Content-Type", MIMETYPE), ("Content-Length", len(body))],
        )

    def _handle_exception(self, exception):
        """Called within an except block to allow converting exceptions
        to arbitrary responses. Anything returned (except None) will
        be used as response."""
        try:
            return super(GraphQLRequest, self)._handle_exception(exception)
        except Exception:
            if not isinstance(exception, SessionExpiredException):
                if (
                    exception.args
                    and exception.args[0] == "bus.Bus not available in test mode"
                ):
                    _logger.info(exception)
                elif isinstance(
                    exception, (odoo.exceptions.UserError, werkzeug.exceptions.NotFound)
                ):
                    _logger.warning(exception)
                else:
                    _logger.exception("Exception during GraphQL request handling.")
            error = {
                "code": 200,
                "message": "Odoo Server Error",
                "data": serialize_exception(exception),
            }
            if isinstance(exception, werkzeug.exceptions.NotFound):
                error["http_status"] = 404
                error["code"] = 404
                error["message"] = "404: Not Found"
            if isinstance(exception, AuthenticationError):
                error["code"] = 100
                error["message"] = "Odoo Session Invalid"
            if isinstance(exception, SessionExpiredException):
                error["code"] = 100
                error["message"] = "Odoo Session Expired"
            return self._graphql_response(error=error)

    def dispatch(self):
        if self._is_cors_preflight(request.endpoint):
            headers = {
                "Access-Control-Max-Age": 60 * 60 * 24,
                "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
            }
            return Response(status=200, headers=headers)
        rpc_request_flag = rpc_request.isEnabledFor(logging.DEBUG)
        rpc_response_flag = rpc_response.isEnabledFor(logging.DEBUG)
        if rpc_request_flag or rpc_response_flag:
            endpoint = self.endpoint.method.__name__

            start_time = time.time()
            start_memory = 0
            if psutil:
                start_memory = memory_info(psutil.Process(os.getpid()))
            if rpc_request and rpc_response_flag:
                rpc_request.debug("%s: %s", endpoint, self.graphqlrequest)

        result = self._call_function()
        # env = request.environ.get
        # result = parse_document(env, parse(self.graphqlrequest))

        if rpc_request_flag or rpc_response_flag:
            end_time = time.time()
            end_memory = 0
            if psutil:
                end_memory = memory_info(psutil.Process(os.getpid()))
            logline = "%s: time:%.3fs mem: %sk -> %sk (diff: %sk)" % (
                endpoint,
                end_time - start_time,
                start_memory / 1024,
                end_memory / 1024,
                (end_memory - start_memory) / 1024,
            )
            if rpc_response_flag:
                rpc_response.debug("%s, %s", logline, pprint.pformat(result))
            else:
                rpc_request.debug(logline)

        return self._graphql_response(result)


# Add the new request type

_get_request = Root.get_request


def get_request(self, httprequest):
    # deduce type of request
    if httprequest.mimetype == MIMETYPE:
        return GraphQLRequest(httprequest)
    return _get_request(self, httprequest)


Root.get_request = get_request
# Add the new request type for routes ? => use http
