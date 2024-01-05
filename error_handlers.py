from abc import ABCMeta, abstractmethod

from flask import jsonify
from app import create_app

class ClientError(Exception, metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def code(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass


class UnauthorizedError(ClientError):
    code = 401
    description = 'Unauthorized'

class APIAuthError(ClientError):
    code = 403
    description = 'Authentication Error'

class NotFoundError(ClientError):
    code = 404
    description = 'Not Found'

class ConflictError(ClientError):
    code = 409
    description = 'Sent data cannot be accepted due to conflict'

def server_error(err):
    return 'Page does not exist'

def client_error(err: ClientError):
    response = {
        'error': err.description
    }

    if err.args:
        response["message"] = err.args[0]

    return jsonify(response), err.code