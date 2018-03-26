import json


def json_response(obj, app):
    j = json.dumps(obj, default=lambda obj: obj.toJSON())
    return app.response_class(j, content_type=app.config['JSONIFY_MIMETYPE'])
