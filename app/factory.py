from flask import g, request

from app.extensions.login import generate_jwt, parse_jwt
from app.main import app
from app.models import User


@app.before_request
def before_request():
    if request.cookies.get('access_token'):
        user_hashed_id = parse_jwt(request.cookies['access_token'])
        current_user = User.query.get(User.id_for_hash(user_hashed_id))
        if current_user:
            g.current_user = current_user


@app.after_request
def after_request(response):
    had_cookie = request.cookies.get('access_token')
    if hasattr(g, 'current_user') and g.current_user and not had_cookie:
        jwt = generate_jwt(g.current_user)
        response.set_cookie('access_token', jwt)

    elif hasattr(g, 'current_user') and not g.current_user and had_cookie:
        response.set_cookie('access_token', '', expires=0)

    return response
