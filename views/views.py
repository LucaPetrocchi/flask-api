from datetime import timedelta

from flask import (
    Blueprint, 
    jsonify,
    request,
    current_app,
)
from flask.views import MethodView
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
    APIAuthError
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
            users = User.query.get(user_id)
            users_schema = UserAdminSchema().dump(users)

        return jsonify(users_schema), 200
    
userbp.add_url_rule(
    '/user',
    view_func=UserAPI.as_view('user'),
    methods=['GET']
)
userbp.add_url_rule(
    '/user/<user_id>',
    view_func=UserAPI.as_view('user_by_id')
)