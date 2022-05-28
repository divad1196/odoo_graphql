# Researches: Improve security

Currently, there is a CSRF security issue by using the cookie to log in.

* Another website CANNOT use the cookie for it will be banned by the same-origin-policy.
* But it can trick the user with phishing





```python
# Partial CSRF check, only performed when session is authenticated, as there
        # is no real risk for unauthenticated sessions here. It's a common case for
        # embedded forms now: SameSite policy rejects the cookies, so the session
        # is lost, and the CSRF check fails, breaking the post for no good reason.
        csrf_token = request.params.pop('csrf_token', None)
        if request.session.uid and not request.validate_csrf(csrf_token):
            raise BadRequest('Session expired (invalid CSRF token)')
```

```python

    def csrf_token(self, time_limit=None):
        """ Generates and returns a CSRF token for the current session

        :param time_limit: the CSRF token validity period (in seconds), or
                           ``None`` for the token to be valid as long as the
                           current user session is (the default)
        :type time_limit: int | None
        :returns: ASCII token string
        """
        token = self.session.sid

        # if no `time_limit` => distant 1y expiry (31536000) so max_ts acts as salt, e.g. vs BREACH
        max_ts = int(time.time() + (time_limit or 31536000))

        msg = '%s%s' % (token, max_ts)
        secret = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        assert secret, "CSRF protection requires a configured database secret"
        hm = hmac.new(secret.encode('ascii'), msg.encode('utf-8'), hashlib.sha1).hexdigest()
        return '%so%s' % (hm, max_ts)

    def validate_csrf(self, csrf):
        if not csrf:
            return False

        try:
            hm, _, max_ts = str(csrf).rpartition('o')
        except UnicodeEncodeError:
            return False

        if max_ts:
            try:
                if int(max_ts) < int(time.time()):
                    return False
            except ValueError:
                return False

        token = self.session.sid

        msg = '%s%s' % (token, max_ts)
        secret = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        assert secret, "CSRF protection requires a configured database secret"
        hm_expected = hmac.new(secret.encode('ascii'), msg.encode('utf-8'), hashlib.sha1).hexdigest()
        return consteq(hm, hm_expected)
```



```python

def dispatch(method, params):
    (db, uid, passwd ) = params[0], int(params[1]), params[2]

    # set uid tracker - cleaned up at the WSGI
    # dispatching phase in odoo.service.wsgi_server.application
    threading.current_thread().uid = uid

    params = params[3:]
    if method == 'obj_list':
        raise NameError("obj_list has been discontinued via RPC as of 6.0, please query ir.model directly!")
    if method not in ['execute', 'execute_kw']:
        raise NameError("Method not available %s" % method)
    security.check(db,uid,passwd)
    registry = odoo.registry(db).check_signaling()
    fn = globals()[method]
    with registry.manage_changes():
        res = fn(db, uid, *params)
    return res
```

