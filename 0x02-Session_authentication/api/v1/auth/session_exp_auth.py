#!/usr/bin/env python3
""" Module of authentication for session
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    def __init__(self):
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ creates a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return None if session_id is None
            Return None if user_id_by_session_id doesn’t contain
                any key equals to session_id
            Return the user_id key from the session dictionary
                if self.session_duration is equal or under 0
            Return None if session dictionary doesn’t contain a key created_at
            Return None if the created_at + session_duration seconds are before
                the current datetime. datetime - timedelta
            Otherwise, return user_id from the session dictionary
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        if 'created_at' not in session_dictionary.keys():
            return None

        created_at = session_dictionary.get('created_at')
        sum = created_at + timedelta(seconds=self.session_duration)
        if sum < datetime.now():
            return None

        return session_dictionary.get('user_id')
