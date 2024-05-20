#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
            returns True if the path is not in the
            list of strings excluded_paths
        """
        if path is None or excluded_paths is None or excluded_paths == '':
            return True
        if path[len(path) - 1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None
