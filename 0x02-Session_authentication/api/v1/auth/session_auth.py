#!/usr/bin/env python3
""" Module of authentication for session
"""
from .auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ that returns a User ID based on a Session ID:
                Return None if session_id is None
                Return None if session_id is not a string
                Return the value (the User ID) for the key session_id
                    in the dictionary user_id_by_session_id.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns a User instance based on a cookie value:
                it uses self.session_cookie(...) and
                    self.user_id_for_session_id(...) to
                    return the User ID based on the cookie _my_session_id
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes the user session / logout:
                If the request is equal to None, return False
                If the request doesn’t contain the Session ID cookie,
                    return False
                If the Session ID of the request is not linked to any User ID,
                    return False
                Otherwise, delete in self.user_id_by_session_id the Session ID
                    (as key of this dictionary) and return True
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        self.user_id_by_session_id.pop(session_id)
        return True
