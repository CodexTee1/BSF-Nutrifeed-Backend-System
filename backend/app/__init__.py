from flask import Flask, jsonify

from .config import Config
from .extensions import db, jwt, migrate
from .routes.auth import auth_bp
from .routes.feed import feed_bp
from .routes.farms import farms_bp
from .routes.monitoring import monitoring_bp
from .routes.users import users_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    @app.get("/")
    def home():
        return (
            jsonify(
                {
                    "message": "Welcome to the BSF-Nutrifeed backend",
                    "health_check": "/health",
                    "docs": "/docs",
                }
            ),
            200,
        )

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok", "message": "BSF-Nutrifeed backend is running"}), 200

    @app.get("/docs")
    def docs():
        return (
            jsonify(
                {
                    "project": "BSF-Nutrifeed Backend",
                    "quick_start": [
                        "Create an admin account",
                        "Log in to get a JWT token",
                        "Create a farm",
                        "Register a farmer with that farm_id",
                        "Create feed batches and monitoring records",
                    ],
                    "endpoints": {
                        "GET /": "Simple home response",
                        "GET /health": "Health check",
                        "POST /api/auth/register": "Register a user",
                        "POST /api/auth/login": "Log in and get access token",
                        "GET /api/auth/me": "Get current user details",
                        "POST /api/farms": "Create a farm as admin",
                        "GET /api/farms": "List farms",
                        "GET /api/users": "List users as admin",
                        "POST /api/feed-batches": "Create a feed batch as admin",
                        "GET /api/feed-batches": "List feed batches",
                        "PATCH /api/feed-batches/<id>/status": "Update batch status as admin",
                        "POST /api/monitoring": "Create a monitoring record",
                        "GET /api/monitoring": "List monitoring records",
                    },
                }
            ),
            200,
        )

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(farms_bp, url_prefix="/api/farms")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(feed_bp, url_prefix="/api/feed-batches")
    app.register_blueprint(monitoring_bp, url_prefix="/api/monitoring")


def register_error_handlers(app):
    @jwt.unauthorized_loader
    def unauthorized(_reason):
        return jsonify({"error": "Authorization token is required"}), 401

    @jwt.invalid_token_loader
    def invalid_token(_reason):
        return jsonify({"error": "Invalid authentication token"}), 422

    @jwt.expired_token_loader
    def expired_token(_jwt_header, _jwt_payload):
        return jsonify({"error": "Authentication token has expired"}), 401

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "Internal server error"}), 500
