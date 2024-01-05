from datetime import timedelta

from flask import (
    Blueprint, 
    jsonify,
    request
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

from app import create_app
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

# blueprint = Blueprint('user', __name__, url_prefix="/users", static_folder="../static")

# @blueprint.route('/')
# def test():
#     return jsonify('rer')