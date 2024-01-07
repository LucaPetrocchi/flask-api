from datetime import timedelta
import json
from flask import (
    Blueprint, 
    jsonify,
    request,
    current_app,
)
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    verify_jwt_in_request,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from extensions import db
from models.models import (
    User,
    Post,
    Tag,
    Reply
)
from schemas.schemas import (
    UserSchema,
    UserAdminSchema,
    TagSchema,
    PostSchema,
    ReplySchema,
)
from error_handlers import (
    UnauthorizedError,
    APIAuthError,
    NotFoundError,
    ConflictError,
)

def get_permissions():
    try:
        verify_jwt_in_request()
        additional_info = get_jwt()
        return additional_info['is_admin']
    except:
        raise UnauthorizedError('Incorrect token, or token was not provided')
    
def validate_permissions(errmsg):
    try:
        assert get_permissions()
    except:
        raise UnauthorizedError(f'Permission denied for this action: {errmsg}')

def id_provided_is_none(id):
    if id is None:
        raise APIAuthError('ID was not provided')

userbp = Blueprint('api', __name__, static_folder="../static")

# @blueprint.route('/')
# def test():
#     return jsonify('rer')

class UserAPI(MethodView):
    def get(self, user_id=None):

        if user_id == None:
            users = User.query.all()
            users_schema = UserAdminSchema().dump(users, many=True)

        elif user_id is not None:
            users = User.get_by_id(user_id)
            users_schema = UserAdminSchema().dump(users)

        if not users_schema:
            raise NotFoundError('User not found')

        return jsonify(users_schema), 200
    
    def post(self):
        try:
            user_json = UserAdminSchema().load(request.json)
        except:
            raise APIAuthError('Failed to validate new user data')
    
        name = user_json.get('name')
        email = user_json.get('email')
        plain_password = user_json.get('password')
        password = generate_password_hash(
            plain_password, method='pbkdf2', salt_length=16
        )
        is_admin = user_json.get('is_admin')

        already_exists = User.query.filter_by(name=name).first()

        if already_exists:
            raise ConflictError('Name already in use')
        
        try:
            User.create(
                name = name,
                email = email,
                password = password,
                is_admin = is_admin,
            )
        except SQLAlchemyError as err:
            msg = str(err.orig)
            raise ConflictError(msg)
        
        return jsonify({'Success': UserSchema().dump(user_json)}), 200

    def put(self, user_id=None):
        id_provided_is_none(user_id)

        user = User.get_by_id(user_id)

        if not user:
            raise NotFoundError('User not found')

        try:
            user_json = UserAdminSchema().load(request.json)
        except:
            raise APIAuthError('Failed to validate')
        
        name = user_json.get('name')
        email = user_json.get('email')
        password = user_json.get('password')
        is_admin = user_json.get('is_admin')

        if password is not None:
            password = generate_password_hash(
                password, method='pbkdf2', salt_length=16
            )

        try:
            user.update(
                name = name,
                email = email,
                password = password,
                is_admin = is_admin,
            )
        except SQLAlchemyError as err:
            msg = str(err.orig)
            raise ConflictError(msg)
    
        return jsonify({'Success': UserAdminSchema().dump(user)}), 200

    def delete(self, user_id=None):
        id_provided_is_none(user_id)

        user = User.get_by_id(user_id)

        if not user:
            raise NotFoundError('User not found')

        dump = UserAdminSchema().dump(user)

        try:
            user.delete()
        except SQLAlchemyError as err:
            msg = str(err.orig)
            raise ConflictError(msg)

        return jsonify({'Deleted': dump}), 410

userbp.add_url_rule(
    '/user',
    view_func=UserAPI.as_view('user'),
)
userbp.add_url_rule(
    '/user/<user_id>',
    view_func=UserAPI.as_view('user_by_id')
)