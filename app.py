import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST


from resources.item import blp as item_blueprint
from resources.store import blp as store_blueprint
from resources.tag import blp as tag_blueprint
from resources.user import blp as user_blueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "jose123"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header, jwt_payload):
        return jsonify({"description": "token has been revoked", "error": "token_revoked"})

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"description": "the tojeb is not fresh", "error": "fresh_token_required"})

    @jwt.expired_token_loader
    def expired_token_loader(jwt_header, jwt_payload):
        return jsonify({"message": "the token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_loader(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def unauthorized_loader():
        return jsonify({"description": "Request doesnt contain a access token",
                        "error": "authorization_required"}), 401

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(item_blueprint)
    api.register_blueprint(store_blueprint)
    api.register_blueprint(tag_blueprint)
    api.register_blueprint(user_blueprint)

    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, port=5000)
