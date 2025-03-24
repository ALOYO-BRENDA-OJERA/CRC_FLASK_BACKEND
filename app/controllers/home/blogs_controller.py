from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.models.home.rhema_blogs_model import RhemaBlog
from app.extensions import db

# Create Blueprint for RhemaBlog routes
rhema_blog_bp = Blueprint('rhema_blog', __name__, url_prefix='/api/v1/blogs')

UPLOAD_FOLDER = r'C:\rhema\blogs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rhema_blog_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Create a new blog
@rhema_blog_bp.route('/rhema_blog', methods=['POST'])
def create_blog():
    try:
        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with file upload
            title = request.form.get('title')
            description = request.form.get('description')
            date_published = request.form.get('date_published')
            
            if not title or not description:
                return jsonify({"message": "Title and description are required"}), 400
            
            # Handle image upload if present
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    image_filename = filename
            
            # Create a new RhemaBlog instance
            blog = RhemaBlog(
                title=title,
                description=description,
                image_url=image_filename,  # Store just the filename
                date_published=date_published  # Optional; defaults to today's date
            )
        else:
            # Handle JSON data without file
            data = request.get_json()
            
            # Create a new RhemaBlog instance
            blog = RhemaBlog(
                title=data.get('title'),
                description=data.get('description'),
                image_url=data.get('image_url'),  # This would be a URL, not a file
                date_published=data.get('date_published')  # Optional; defaults to today's date
            )

        # Add to the session and commit to save it
        db.session.add(blog)
        db.session.commit()

        return jsonify({
            "message": "Blog created successfully", 
            "id": blog.id,
            "image_url": blog.image_url
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get all blogs
@rhema_blog_bp.route('/rhema_blogs', methods=['GET'])
def get_blogs():
    try:
        blogs = RhemaBlog.query.order_by(RhemaBlog.created_at.desc()).all()

        if blogs:
            result = []
            for blog in blogs:
                result.append({
                    "id": blog.id,
                    "title": blog.title,
                    "description": blog.description,
                    "image_url": blog.image_url,  # Just return the filename
                    "date_published": blog.date_published,
                    "created_at": blog.created_at,
                    "updated_at": blog.updated_at
                })

            return jsonify(result)

        return jsonify([])  # Return empty array instead of 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a specific blog by ID
@rhema_blog_bp.route('/rhema_blog/<int:id>', methods=['GET'])
def get_blog(id):
    try:
        blog = RhemaBlog.query.get(id)

        if blog:
            return jsonify({
                "id": blog.id,
                "title": blog.title,
                "description": blog.description,
                "image_url": blog.image_url,  # Just return the filename
                "date_published": blog.date_published,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at
            })

        return jsonify({"message": "Blog not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a blog by ID
@rhema_blog_bp.route('/rhema_blog/<int:id>', methods=['PUT'])
def update_blog(id):
    try:
        blog = RhemaBlog.query.get(id)

        if not blog:
            return jsonify({"message": "Blog not found"}), 404

        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with possible file upload
            if 'title' in request.form:
                blog.title = request.form.get('title')
            if 'description' in request.form:
                blog.description = request.form.get('description')
            if 'date_published' in request.form:
                blog.date_published = request.form.get('date_published')
            
            # Handle image upload if present
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    # Delete old image if it exists
                    if blog.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, blog.image_url)):
                        os.remove(os.path.join(UPLOAD_FOLDER, blog.image_url))
                    
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    blog.image_url = filename
        else:
            # Handle JSON data without file
            data = request.get_json()
            
            # Update fields with provided data
            blog.title = data.get('title', blog.title)
            blog.description = data.get('description', blog.description)
            blog.image_url = data.get('image_url', blog.image_url)
            blog.date_published = data.get('date_published', blog.date_published)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Blog updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a blog by ID
@rhema_blog_bp.route('/rhema_blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    try:
        blog = RhemaBlog.query.get(id)

        if not blog:
            return jsonify({"message": "Blog not found"}), 404

        # Delete the image file if it exists
        if blog.image_url:
            file_path = os.path.join(UPLOAD_FOLDER, blog.image_url)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Delete the blog
        db.session.delete(blog)
        db.session.commit()

        return jsonify({"message": "Blog deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
