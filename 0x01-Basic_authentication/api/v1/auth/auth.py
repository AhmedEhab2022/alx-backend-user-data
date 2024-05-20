#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
            returns False - path and excluded_paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None
