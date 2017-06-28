from flask import current_app as app, request




def log_request(message=''):
    with app.app_context():
        request_message = '[' + request.remote_addr + ']' + '[' + request.method + ']' + '[' + request.url + ']'
        app.logger.debug(request_message + message)

def log_debug(message=''):
    with app.app_context():
        app.logger.debug()

def log_info(message=''):
    with app.app_context():
        app.logger.info()

def log_error(message=''):
    with app.app_context():
        app.logger.error()
