# -*-coding: utf-8 -*-

from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.auth import OAuthMixin, OAuth2Mixin, _oauth_signature
import urllib
import logging
import time
import binascii
import hashlib
import urlparse
import uuid


class WeiboMixin(OAuthMixin):
    """Sina weibo OAuth authentication."""

    _OAUTH_VERSION = "1.0"
    _OAUTH_REQUEST_TOKEN_URL = "http://api.t.sina.com.cn/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "http://api.t.sina.com.cn/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "http://api.t.sina.com.cn/oauth/authorize"
    _OAUTH_NO_CALLBACKS = False
    _OAUTH_VERSION = "1.0"

    def weibo_request(self, path, callback, access_token=None,
			   post_args=None, **args):
	url = "http://api.t.sina.com.cn" + path
	if access_token:
	    all_args = {}
	    all_args.update(args)
	    all_args.update(post_args or {})
	    consumer_token = self._oauth_consumer_token()
	    method = "POST" if post_args is not None else "GET"
	    oauth = self._oauth_request_parameters(
		url, access_token, all_args, method=method)
	    args.update(oauth)
	if args: url += "?" + urllib.urlencode(args)
	callback = self.async_callback(self._on_weibo_request, callback)
	http = httpclient.AsyncHTTPClient()
	if post_args is not None:
	    http.fetch(url, method="POST", body=urllib.urlencode(post_args),
		       callback=callback)
	else:
	    http.fetch(url, callback=callback)

    def _on_weibo_request(self, callback, response):
	if response.error:
	    logging.warning("Error response %s fetching %s", response.error,
			    response.request.url)
	    callback(None)
	    return
	callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
	self.require_setting("weibo_consumer_key", "Weibo OAuth")
	self.require_setting("weibo_consumer_secret", "Weibo OAuth")
	return dict(
	    key=self.settings["weibo_consumer_key"],
	    secret=self.settings["weibo_consumer_secret"])

    def _oauth_get_user(self, access_token, callback):
	callback = self.async_callback(self._parse_user_response, callback)
	self.weibo_request(
	    "/users/show/%s.json" % access_token["user_id"],
	    access_token=access_token, callback=callback)

    def _parse_user_response(self, callback, user):
	if user:
	    user["username"] = user["id"]
	callback(user)


class QQMixin(OAuthMixin):
    """QQ weibo Open ID / OAuth authentication."""
    _OAUTH_VERSION = "1.0"
    _OAUTH_REQUEST_TOKEN_URL = "https://open.t.qq.com/cgi-bin/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "https://open.t.qq.com/cgi-bin/access_token"
    _OAUTH_AUTHORIZE_URL = "https://open.t.qq.com/cgi-bin/authorize"
    _OAUTH_NO_CALLBACKS = False
    _OAUTH_VERSION = "1.0"

    def authorize_redirect(self, callback_uri=None, extra_params=None):
	if callback_uri and getattr(self, "_OAUTH_NO_CALLBACKS", False):
	    raise Exception("This service does not support oauth_callback")
	http = httpclient.AsyncHTTPClient()
	http.fetch(self._oauth_request_token_url(callback_uri=callback_uri,
	    extra_params=extra_params),
	    self.async_callback(
		self._on_request_token,
		self._OAUTH_AUTHORIZE_URL,
	    callback_uri))

    def _oauth_request_token_url(self, callback_uri=None, extra_params=None):
	consumer_token = self._oauth_consumer_token()
	url = self._OAUTH_REQUEST_TOKEN_URL
	args = dict(
	    oauth_consumer_key=consumer_token["key"],
	    oauth_signature_method="HMAC-SHA1",
	    oauth_timestamp=str(int(time.time())),
	    oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
	    oauth_version=getattr(self, "_OAUTH_VERSION", "1.0a"),
	)
	if callback_uri:
	    args["oauth_callback"] = urlparse.urljoin(
		self.request.full_url(), callback_uri)
	if extra_params: args.update(extra_params)
	signature = _oauth_signature(consumer_token, "GET", url, args)

	args["oauth_signature"] = signature
	return url + "?" + urllib.urlencode(args)

    def _oauth_access_token_url(self, request_token):
	consumer_token = self._oauth_consumer_token()
	url = self._OAUTH_ACCESS_TOKEN_URL
	args = dict(
	    oauth_consumer_key=consumer_token["key"],
	    oauth_token=request_token["key"],
	    oauth_signature_method="HMAC-SHA1",
	    oauth_timestamp=str(int(time.time())),
	    oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
	    oauth_version=getattr(self, "_OAUTH_VERSION", "1.0a"),
	)
	if "verifier" in request_token:
	    args["oauth_verifier"]=request_token["verifier"]

	signature = _oauth_signature(consumer_token, "GET", url, args,
					request_token)

	args["oauth_signature"] = signature
	return url + "?" + urllib.urlencode(args)


    def weibo_request(self, path, callback, access_token=None,
			   post_args=None, **args):
	url = "http://open.t.qq.com/api" + path
	if access_token:
	    all_args = {}
	    all_args.update(args)
	    all_args.update(post_args or {})
	    consumer_token = self._oauth_consumer_token()
	    method = "POST" if post_args is not None else "GET"
	    oauth = self._oauth_request_parameters(
		url, access_token, all_args, method=method)
	    args.update(oauth)
	if args: url += "?" + urllib.urlencode(args)
	callback = self.async_callback(self._on_weibo_request, callback)
	http = httpclient.AsyncHTTPClient()
	if post_args is not None:
	    http.fetch(url, method="POST", body=urllib.urlencode(post_args),
		       callback=callback)
	else:
	    http.fetch(url, callback=callback)

    def _on_weibo_request(self, callback, response):
	if response.error:
	    logging.warning("Error response %s fetching %s", response.error,
			    response.request.url)
	    callback(None)
	    return
	callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
	self.require_setting("qq_consumer_key", "QQ OAuth")
	self.require_setting("qq_consumer_secret", "QQ OAuth")
	return dict(
            key=self.settings["qq_consumer_key"],                      
            secret=self.settings["qq_consumer_secret"])

    def _oauth_get_user(self, access_token, callback):
	callback = self.async_callback(self._parse_user_response, callback)
	self.weibo_request(
	    "/user/info", access_token=access_token,
	    callback=callback, format="json")

    def _parse_user_response(self, callback, user):
	callback(user)

# {{{ Renren Graph Mixin
class RenrenGraphMixin(OAuth2Mixin):
    """Renren authentication using the graph api and OAuth2."""

    _OAUTH_ACCESS_TOKEN_URL = "https://graph.renren.com/oauth/token?"
    _OAUTH_AUTHORIZE_URL = "https://graph.renren.com/oauth/authorize?"
    _OAUTH_NO_CALLBACKS = False

    def authorize_redirect(self, redirect_uri=None, client_id=None,
			   client_secret=None, extra_params=None ):
	args = {
	  "redirect_uri": redirect_uri,
	  "client_id": client_id,
	  "response_type" : "code",
	}
	if extra_params: args.update(extra_params)
	self.redirect(
		url_concat(self._OAUTH_AUTHORIZE_URL, args))

    def _oauth_request_token_url(self, redirect_uri=None, client_id=None,
				 client_secret=None, code=None,
				 grant_type=None, extra_params=None):
	url = self._OAUTH_ACCESS_TOKEN_URL
	args = dict(
	    redirect_uri=redirect_uri,
	    code=code,
	    grant_type=grant_type,
	    client_id=client_id,
	    client_secret=client_secret,
	    )
	if extra_params: args.update(extra_params)

	return url_concat(url, args)

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
			      code, callback, extra_fields=None):
      http = httpclient.AsyncHTTPClient()
      args = dict(
	redirect_uri=redirect_uri,
	code=code,
	grant_type="authorization_code",
	client_id=client_id,
	client_secret=client_secret,
      )
      fields = set(["uid", "name", "tinyurl", "headhurl"])

      http.fetch(self._oauth_request_token_url(**args),
	  self.async_callback(self._on_access_token, redirect_uri,
	      client_id, client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
			callback, fields, response):
	if response.error:
	    logging.warning('Renren auth error: %s' % str(response))
	    callback(None)
	    return
	callback(response.body)
	"""
	result = escape.json_decode(response.body)
	session = {
	    "access_token": result["access_token"],
	    "expires": result["expires_in"]
	}
	self.renren_request(
	    path="",
	    callback=self.async_callback(
		self._on_get_user_info, callback, session, fields),
	    access_token=session["access_token"],
	    fields=",".join(fields),
	    method="users.getInfo")
	"""

    def _on_get_user_info(self, callback, session, fields, user):
	if user is None:
	    callback(None)
	    return

	fieldmap = {}
	for field in fields:
	    fieldmap[field] = user.get(field)
	fieldmap.update({"access_token": session["access_token"],
			 "session_expires": session["expires"]})
	callback(fieldmap)

    def renren_request(self, path, callback, access_token=None,
			   post_args=None, **args):
	url = "http://api.renren.com/restserver.do" + path
	client_token = self._oauth_client_token()
	all_args = {"v" : "1.0", "api_key" : client_token["key"],
		    "call_id" : str(int(time.time())), "format": "JSON"}
	if access_token:
	    session_key = access_token.split("|")[-1]
	    all_args["session_key"] = session_key
	all_args.update(args)
	all_args.update(post_args or {})

	base_string = "".join(["%s=%s" % (k,v) for k, v in all_args.items()])
	base_string += client_token["secret"]

	hash = hashlib.md5()
	hash.update(base_string)
	sig = hash.hexdigest()

	all_args["sig"] = sig
	if all_args: url += "?" + urllib.urlencode(all_args)
	callback = self.async_callback(self._on_renren_request, callback)
	http = httpclient.AsyncHTTPClient()
	if post_args is not None:
	    http.fetch(url, method="POST", body=urllib.urlencode(post_args),
		       callback=callback)
	else:
	    http.fetch(url, callback=callback)

    def _on_renren_request(self, callback, response):
	if response.error:
	    logging.warning("Error response %s fetching %s", response.error,
			    response.request.url)
	    callback(None)
	    return

	callback(escape.json_decode(response.body))

    def _oauth_client_token(self):
	self.require_setting("renren_key", "Renren OAuth")
	self.require_setting("renren_secret", "Renren OAuth")
	return dict(
	    key=self.settings["renren_key"],
	    secret=self.settings["renren_secret"])

# }}}
