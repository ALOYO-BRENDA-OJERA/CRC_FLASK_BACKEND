from flask import Flask
from app.extensions import db, migrate, cors, jwt, scheduler
from app.controllers.users.user_controller import users_bp
from app.controllers.users.subscribers_controller import subscribers_bp
from app.controllers.surmon.audio_controller import audio_sermons_bp
from app.controllers.surmon.video_controller import video_sermons_bp
from app.controllers.ministry.ministry_controller import ministries_bp
from app.controllers.home.trending_controller import trending_now_bp
from app.controllers.home.testimonies_controller import testimony_bp
from app.controllers.home.events_controller import event_bp
from app.controllers.home.cornet_controller import daily_devotion_bp
from app.controllers.home.blogs_controller import rhema_blog_bp
from app.controllers.home.word_of_the_month_controller import word_of_month_bp
from app.controllers.home.pray_with_controller import pray_with_bp
from app.controllers.about.branch_event_controller import branch_event_bp
from app.controllers.users.feedback_controller import feedback_bp
from app.controllers.rhema.application_controller import application_bp
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    app = Flask(__name__)

    # Flask and database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/CRC_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    # Configure JWT to read from cookies
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'  # Correct key for access token cookie
    app.config['JWT_COOKIE_SECURE'] = False  # Set to False for local development (HTTP)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disabled for simplicity; enable in production
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'  # Restrict cookie to same-site requests

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/v1/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    jwt.init_app(app)
    scheduler.init_app(app)
    # Note: Uncomment scheduler.start() in production, avoid in debug mode to prevent duplicate runs

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(subscribers_bp)
    app.register_blueprint(audio_sermons_bp)
    app.register_blueprint(video_sermons_bp)
    app.register_blueprint(ministries_bp)
    app.register_blueprint(trending_now_bp)
    app.register_blueprint(testimony_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(daily_devotion_bp)
    app.register_blueprint(rhema_blog_bp)
    app.register_blueprint(word_of_month_bp)
    app.register_blueprint(pray_with_bp)
    app.register_blueprint(branch_event_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(application_bp)

    # Swagger UI setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "CRC System API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Define routes
    @app.route('/')
    def home():
        return "CRC SYSTEM", 200

    # CLI command for seeding admin user
    @app.cli.command("seed-admin")
    def seed_admin_command():
        from seeds.seed_admin import seed_admin
        seed_admin()
        
          # Add security headers to every response
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'  # Prevent clickjacking
        response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME sniffing
        response.headers['Referrer-Policy'] = 'no-referrer'  # No referrer info shared
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'  # Force HTTPS
        return response

    return app