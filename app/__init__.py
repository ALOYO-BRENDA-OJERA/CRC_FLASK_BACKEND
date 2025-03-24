# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, cors, jwt, scheduler

from app.controllers.users.user_controller import users_bp
from app.controllers.surmon.audio_controller import audio_sermons_bp
from app.controllers.surmon.video_controller import video_sermons_bp
from app.controllers.ministry.ministry_controller import ministries_bp
from app.controllers.home.trending_controller import trending_now_bp
from app.controllers.home.testimonies_controller import testimony_bp
from app.controllers.home.events_controller import event_bp
from app.controllers.home.cornet_controller import daily_devotion_bp
from app.controllers.home.blogs_controller import rhema_blog_bp
from app.controllers.home.word_of_the_month_controller import word_of_month_bp
from flask_swagger_ui import get_swaggerui_blueprint
from app.controllers.home.pray_with_controller import pray_with_bp

def create_app():
    app = Flask(__name__)
    
    

    # Configuration (you can load this from config.py or directly here)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/CRC_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    # Initialize extensions
    db.init_app(app)  # Use the db initialized in extensions
    migrate.init_app(app, db)  # Use the migrate initialized in extensions
    cors.init_app(app)
    jwt.init_app(app)
    scheduler.init_app(app)
    
    app.register_blueprint
    app.register_blueprint(users_bp)
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
    
    # Swagger UI setup
    SWAGGER_URL = '/swagger'  # The URL to access the Swagger UI
    API_URL = '/static/swagger.json'  # Path to the swagger.json file

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "CRC System API"}
    )

    # Register the Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    
    
    @app.route('/')
    def home():
        return "CRC SYSTEM", 200

    return app
