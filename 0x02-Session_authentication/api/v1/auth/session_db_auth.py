#!/usr/bin/env python3
""" Module of authentication for session
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """ Creates and stores new instance of UserSession and
            returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID by requesting UserSession in the database
            on the session_id
        """
        if session_id is None:
            return None

        users = UserSession.search({'session_id': session_id})
        if users == []:
            return None

        return users[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the UserSession based on the Session ID from the request
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        users = UserSession.search({'session_id': session_id})
        if users == []:
            return False

        for user in users:
            user.remove()

        return True
