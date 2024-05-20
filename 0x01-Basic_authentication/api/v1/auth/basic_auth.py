#!/usr/bin/env python3
""" Module of Auth views
    BasicAuth class
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ returns the user email and password from the Base64 decoded value
        """
        dec_base64_auth_header = decoded_base64_authorization_header
        if dec_base64_auth_header is None:
            return (None, None)
        if not isinstance(dec_base64_auth_header, str):
            return (None, None)
        if ':' not in dec_base64_auth_header:
            return (None, None)
        return tuple(dec_base64_auth_header.split(':'))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = []
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if users is None or len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)
