#!/usr/bin/env python3
""" Module of Auth views
    BasicAuth class
"""
from .auth import Auth


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
