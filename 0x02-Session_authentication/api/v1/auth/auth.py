#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, TypeVar
import os


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
        for excluded_path in excluded_paths:
            if excluded_path.split('*')[0] in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request:
                Return None if request is None
                Return the value of the cookie named _my_session_id from
                    request - the name of the cookie must be defined by
                    the environment variable SESSION_NAME
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        _my_session_id = request.cookies.get(session_name)
        return _my_session_id
