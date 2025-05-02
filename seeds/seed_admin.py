import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.users.users_model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, DataError

def seed_admin(reset_existing=False):
    app = create_app()
    with app.app_context():  # Ensure app context is active
        try:
            # Fetch admin credentials from environment variables or use defaults
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com').strip()
            admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123')

            # Validate email
            if not admin_email or '@' not in admin_email:
                raise ValueError(f"Invalid email address: {admin_email}")

            # Validate password
            if not admin_password or len(admin_password) < 6:
                raise ValueError(f"Invalid password: Password must be at least 6 characters long")

            # Check for existing user
            print(f"Checking for existing user with email: {admin_email}")
            existing_admin = User.query.filter_by(email=admin_email).first()
            if existing_admin:
                if reset_existing:
                    print(f"Found existing user with email {admin_email}. Deleting to reset.")
                    db.session.delete(existing_admin)
                    db.session.commit()
                    print(f"Existing user {admin_email} deleted.")
                else:
                    print(f"Admin user with email {admin_email} already exists.")
                    print(f"Existing user details: name={existing_admin.name}, user_type={existing_admin.user_type}, password_hash={existing_admin.password[:30]}...")
                    return

            # Generate password hash with pbkdf2:sha256
            print(f"Generating password hash for user: {admin_email}")
            try:
                hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
                if not hashed_password:
                    raise ValueError("Failed to generate password hash")
                print(f"Generated hash: {hashed_password[:30]}...")
            except Exception as e:
                raise ValueError(f"Password hashing error: {str(e)}")

            # Create new admin user
            print(f"Creating new admin user: {admin_email}")
            admin_user = User(
                name='Admin User',
                email=admin_email,
                contact='1234567890',
                password=hashed_password,
                user_type='admin',
                notes='Default admin account created via seeder'
            )

            # Add user to session
            db.session.add(admin_user)

            # Commit to database
            print("Attempting to commit user to database")
            db.session.commit()
            print(f"Admin user {admin_email} created successfully.")
            print(f"User details: email={admin_user.email}, user_type={admin_user.user_type}, password_hash={admin_user.password[:30]}...")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Database integrity error: {str(e)}")
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                print(f"Error: Email {admin_email} is already in use by another user.")
            else:
                print(f"Other integrity error: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")

        except DataError as e:
            db.session.rollback()
            print(f"Database data error: {str(e)}")
            print(f"Possible cause: Invalid data format for email or other fields.")
            print(f"Full traceback: {traceback.format_exc()}")

        except ValueError as e:
            db.session.rollback()
            print(f"Validation error: {str(e)}")
            # Ascertain whether the error is email-related or password-related
            if "email" in str(e).lower():
             if "email" in str(e).lower():
                print(f"Error related to email: {admin_email}")
            elif "password" in str(e).lower():
                print(f"Error related to password: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")

        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error creating admin user: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    seed_admin(reset_existing=True)  # Set to True to delete existing user