#!/usr/bin/env python3
""" Module of Auth views
    BasicAuth class
"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header for a BasicAuth
        """
        auth_header = authorization_header
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if auth_header[:6] != 'Basic ':
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ returns the decoded value of a Base64 string
        """
        base64_auth_header = base64_authorization_header
        if base64_auth_header is None:
            return None
        if not isinstance(base64_auth_header, str):
            return None
        try:
            return base64.b64decode(base64_auth_header).decode('utf-8')
        except Exception:
            return None
