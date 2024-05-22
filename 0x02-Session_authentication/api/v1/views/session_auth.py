#!/usr/bin/env python3
""" Module of auth views
    that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """  Session authentication handler
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            # not on top of the file (can generate circular import -
            #  and break first tasks of this project)
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = make_response(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return response

    return jsonify({"error": "wrong password"}), 401
