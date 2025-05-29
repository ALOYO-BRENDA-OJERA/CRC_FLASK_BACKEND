# from flask import Blueprint, request, jsonify, send_from_directory, send_file, Response
# from app.models.Surmon.videos_model import VideoSermon
# from app.extensions import db
# from werkzeug.utils import secure_filename
# import os
# from datetime import datetime

# # Create Blueprint for Video Sermon routes
# video_sermons_bp = Blueprint('video_sermons', __name__, url_prefix='/api/v1/video_sermon')

# # Define the upload folders (relative to the project root)
# VIDEO_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads', 'video_sermons')
# THUMBNAIL_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads', 'thumbnails')

# # Create directories if they don't exist
# os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(THUMBNAIL_UPLOAD_FOLDER, exist_ok=True)

# ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
# ALLOWED_THUMBNAIL_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# def allowed_file(filename, allowed_extensions):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# # Serve thumbnail images
# @video_sermons_bp.route('/thumbnails/<filename>', methods=['GET'])
# def serve_thumbnail(filename):
#     return send_from_directory(THUMBNAIL_UPLOAD_FOLDER, filename)

# # Stream a video file
# @video_sermons_bp.route('/stream_video/<int:id>', methods=['GET'])
# def stream_video(id):
#     try:
#         sermon = VideoSermon.query.get(id)
#         if not sermon or not os.path.exists(sermon.file_path):
#             return jsonify({"message": "Video sermon not found or file missing"}), 404
        
#         # Determine video file type for correct mimetype
#         file_extension = os.path.splitext(sermon.file_path)[1].lower().lstrip('.')
#         mimetype = f'video/{file_extension}'
#         if file_extension == 'mkv':
#             mimetype = 'video/x-matroska'
        
#         # Stream the file in chunks to handle large files efficiently
#         def generate():
#             with open(sermon.file_path, 'rb') as video_file:
#                 chunk_size = 1024 * 1024  # 1MB chunks
#                 while True:
#                     chunk = video_file.read(chunk_size)
#                     if not chunk:
#                         break
#                     yield chunk
        
#         return Response(
#             generate(), 
#             mimetype=mimetype,
#             headers={
#                 'Accept-Ranges': 'bytes',
#                 'Content-Disposition': f'inline; filename="{os.path.basename(sermon.file_path)}"'
#             }
#         )
#     except Exception as e:
#         print(f"Error streaming video: {str(e)}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # Create a new video sermon
# @video_sermons_bp.route('/create_video_sermons', methods=['POST'])
# def create_video_sermon():
#     try:
#         data = request.form
#         video_file = request.files.get('file')
#         thumbnail_file = request.files.get('thumbnail')

#         # Validate the input
#         if 'title' not in data or 'preacher' not in data:
#             return jsonify({"message": "Missing required fields"}), 400
#         if not video_file or not allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
#             return jsonify({"message": "Invalid video file or no video file uploaded"}), 400
#         if thumbnail_file and not allowed_file(thumbnail_file.filename, ALLOWED_THUMBNAIL_EXTENSIONS):
#             return jsonify({"message": "Invalid thumbnail file format"}), 400

#         # Process video file
#         video_filename = secure_filename(video_file.filename)
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         video_filename = f"{timestamp}_{video_filename}"
#         video_path = os.path.join(VIDEO_UPLOAD_FOLDER, video_filename)
#         video_file.save(video_path)

#         # Process thumbnail if provided
#         thumbnail_filename = None
#         if thumbnail_file:
#             thumbnail_filename = secure_filename(thumbnail_file.filename)
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
#             thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename)
#             thumbnail_file.save(thumbnail_path)

#         # Create the video sermon entry in the database
#         video_sermon = VideoSermon(
#             title=data['title'],
#             description=data.get('description', ''),
#             file_path=video_path,
#             preacher=data['preacher'],
#             thumbnail_path=thumbnail_filename  # Store just the filename
#         )
        
#         db.session.add(video_sermon)
#         db.session.commit()

#         # Prepare response with full URLs
#         thumbnail_url = f"/api/v1/video_sermon/thumbnails/{thumbnail_filename}" if thumbnail_filename else None
#         video_url = f"/api/v1/video_sermon/stream_video/{video_sermon.id}"

#         return jsonify({
#             "message": "Video sermon created successfully",
#             "sermon_id": video_sermon.id,
#             "sermon": {
#                 "id": video_sermon.id,
#                 "title": video_sermon.title,
#                 "description": video_sermon.description,
#                 "file_path": video_url,  # Return streaming URL
#                 "thumbnail": thumbnail_url,
#                 "uploaded_at": video_sermon.uploaded_at.isoformat() if video_sermon.uploaded_at else None,
#                 "preacher": video_sermon.preacher
#             }
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # Get all video sermons
# @video_sermons_bp.route('/list_video_sermons', methods=['GET'])
# def list_video_sermons():
#     try:
#         sermons = VideoSermon.query.all()
#         return jsonify([{
#             "id": sermon.id,
#             "title": sermon.title,
#             "description": sermon.description,
#             "file_path": f"/api/v1/video_sermon/stream_video/{sermon.id}",
#             "thumbnail": f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None,
#             "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
#             "preacher": sermon.preacher
#         } for sermon in sermons])
#     except Exception as e:
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # Get a video sermon by id
# @video_sermons_bp.route('/get_video_sermons/<int:id>', methods=['GET'])
# def get_video_sermon(id):
#     try:
#         sermon = VideoSermon.query.get(id)
#         if sermon:
#             thumbnail_url = f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None
#             video_url = f"/api/v1/video_sermon/stream_video/{sermon.id}"
#             return jsonify({
#                 "id": sermon.id,
#                 "title": sermon.title,
#                 "description": sermon.description,
#                 "file_path": video_url,
#                 "thumbnail": thumbnail_url,
#                 "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
#                 "preacher": sermon.preacher
#             })
#         else:
#             return jsonify({"message": "Video sermon not found"}), 404
#     except Exception as e:
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # Update a video sermon by id
# @video_sermons_bp.route('/update_video_sermons/<int:id>', methods=['PUT'])
# def update_video_sermon(id):
#     try:
#         data = request.form
#         sermon = VideoSermon.query.get(id)

#         if not sermon:
#             return jsonify({"message": "Video sermon not found"}), 404

#         # Update fields
#         sermon.title = data.get('title', sermon.title)
#         sermon.description = data.get('description', sermon.description)
#         sermon.preacher = data.get('preacher', sermon.preacher)

#         # Handle video file upload if a new video file is provided
#         video_file = request.files.get('file')
#         if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
#             # Delete the old file if it exists
#             if os.path.exists(sermon.file_path):
#                 try:
#                     os.remove(sermon.file_path)
#                 except Exception as e:
#                     print(f"Error deleting old video file: {e}")
            
#             # Save new video file
#             video_filename = secure_filename(video_file.filename)
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             video_filename = f"{timestamp}_{video_filename}"
#             video_path = os.path.join(VIDEO_UPLOAD_FOLDER, video_filename)
#             video_file.save(video_path)
#             sermon.file_path = video_path

#         # Handle thumbnail file upload if a new thumbnail file is provided
#         thumbnail_file = request.files.get('thumbnail')
#         if thumbnail_file and allowed_file(thumbnail_file.filename, ALLOWED_THUMBNAIL_EXTENSIONS):
#             # Delete the old thumbnail if it exists
#             if sermon.thumbnail_path:
#                 old_thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail_path)
#                 if os.path.exists(old_thumbnail_path):
#                     try:
#                         os.remove(old_thumbnail_path)
#                     except Exception as e:
#                         print(f"Error deleting old thumbnail: {e}")
            
#             # Save new thumbnail
#             thumbnail_filename = secure_filename(thumbnail_file.filename)
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
#             thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename)
#             thumbnail_file.save(thumbnail_path)
#             sermon.thumbnail_path = thumbnail_filename

#         db.session.commit()

#         # Prepare response with full URLs
#         thumbnail_url = f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None
#         video_url = f"/api/v1/video_sermon/stream_video/{sermon.id}"

#         return jsonify({
#             "message": "Video sermon updated successfully",
#             "sermon": {
#                 "id": sermon.id,
#                 "title": sermon.title,
#                 "description": sermon.description,
#                 "file_path": video_url,
#                 "thumbnail": thumbnail_url,
#                 "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
#                 "preacher": sermon.preacher
#             }
#         })

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # Delete a video sermon by id
# @video_sermons_bp.route('/delete_video_sermons/<int:id>', methods=['DELETE'])
# def delete_video_sermon(id):
#     try:
#         sermon = VideoSermon.query.get(id)
#         if not sermon:
#             return jsonify({"message": "Video sermon not found"}), 404

#         # Delete the video file from the server
#         if os.path.exists(sermon.file_path):
#             try:
#                 os.remove(sermon.file_path)
#             except Exception as e:
#                 print(f"Error deleting video file: {e}")

#         # Delete the thumbnail if it exists
#         if sermon.thumbnail_path:
#             thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail_path)
#             if os.path.exists(thumbnail_path):
#                 try:
#                     os.remove(thumbnail_path)
#                 except Exception as e:
#                     print(f"Error deleting thumbnail: {e}")

#         db.session.delete(sermon)
#         db.session.commit()

#         return jsonify({"message": "Video sermon deleted successfully"})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500




from flask import Blueprint, request, jsonify, send_from_directory, send_file, Response, render_template
from app.models.Surmon.videos_model import VideoSermon
from app.extensions import db
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create Blueprint for Video Sermon routes
video_sermons_bp = Blueprint('video_sermons', __name__, url_prefix='/api/v1/video_sermon')

# Define the upload folders (relative to the project root)
VIDEO_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Uploads', 'video_sermons')
THUMBNAIL_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Uploads', 'thumbnails')

# Create directories if they don't exist
os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_UPLOAD_FOLDER, exist_ok=True)

ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
ALLOWED_THUMBNAIL_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# YouTube API configuration
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
API_KEY = os.environ.get('YOUTUBE_API_KEY')
CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')

def get_youtube_videos():
    try:
        logger.debug(f"Using API key: {API_KEY}")
        logger.debug(f"Fetching videos for channel ID: {CHANNEL_ID}")
        
        if not API_KEY:
            raise ValueError("YouTube API key not set")
        if not CHANNEL_ID:
            raise ValueError("YouTube channel ID not set")

        # Initialize YouTube API client with API key
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

        # Get the channel's uploads playlist ID
        request = youtube.channels().list(part='contentDetails', id=CHANNEL_ID)
        response = request.execute()

        if not response.get('items'):
            logger.warning(f"No channel found for ID: {CHANNEL_ID}")
            return []

        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Fetch videos from the uploads playlist
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=10  # Adjust as needed
        )
        playlist_response = playlist_request.execute()

        videos = []
        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail = item['snippet']['thumbnails'].get('medium', {}).get('url', '')
            embed_url = f'https://www.youtube.com/embed/{video_id}'
            videos.append({
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'embed_url': embed_url,
                'published_at': item['snippet']['publishedAt']
            })

        logger.debug(f"Fetched {len(videos)} videos")
        return videos

    except Exception as e:
        logger.error(f"Error fetching YouTube videos: {e}", exc_info=True)
        return []

# Serve thumbnail images
@video_sermons_bp.route('/thumbnails/<filename>', methods=['GET'])
def serve_thumbnail(filename):
    return send_from_directory(THUMBNAIL_UPLOAD_FOLDER, filename)

# Stream a video file
@video_sermons_bp.route('/stream_video/<int:id>', methods=['GET'])
def stream_video(id):
    try:
        sermon = VideoSermon.query.get(id)
        if not sermon or not os.path.exists(sermon.file_path):
            return jsonify({"message": "Video sermon not found or file missing"}), 404
        
        # Determine video file type for correct mimetype
        file_extension = os.path.splitext(sermon.file_path)[1].lower().lstrip('.')
        mimetype = f'video/{file_extension}'
        if file_extension == 'mkv':
            mimetype = 'video/x-matroska'
        
        # Stream the file in chunks to handle large files efficiently
        def generate():
            with open(sermon.file_path, 'rb') as video_file:
                chunk_size = 1024 * 1024  # 1MB chunks
                while True:
                    chunk = video_file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        
        return Response(
            generate(), 
            mimetype=mimetype,
            headers={
                'Accept-Ranges': 'bytes',
                'Content-Disposition': f'inline; filename="{os.path.basename(sermon.file_path)}"'
            }
        )
    except Exception as e:
        logger.error(f"Error streaming video: {str(e)}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Create a new video sermon
@video_sermons_bp.route('/create_video_sermons', methods=['POST'])
def create_video_sermon():
    try:
        data = request.form
        video_file = request.files.get('file')
        thumbnail_file = request.files.get('thumbnail')

        # Validate the input
        if 'title' not in data or 'preacher' not in data:
            return jsonify({"message": "Missing required fields"}), 400
        if not video_file or not allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({"message": "Invalid video file or no video file uploaded"}), 400
        if thumbnail_file and not allowed_file(thumbnail_file.filename, ALLOWED_THUMBNAIL_EXTENSIONS):
            return jsonify({"message": "Invalid thumbnail file format"}), 400

        # Process video file
        video_filename = secure_filename(video_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        video_filename = f"{timestamp}_{video_filename}"
        video_path = os.path.join(VIDEO_UPLOAD_FOLDER, video_filename)
        video_file.save(video_path)

        # Process thumbnail if provided
        thumbnail_filename = None
        if thumbnail_file:
            thumbnail_filename = secure_filename(thumbnail_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
            thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename)
            thumbnail_file.save(thumbnail_path)

        # Create the video sermon entry in the database
        video_sermon = VideoSermon(
            title=data['title'],
            description=data.get('description', ''),
            file_path=video_path,
            preacher=data['preacher'],
            thumbnail_path=thumbnail_filename  # Store just the filename
        )
        
        db.session.add(video_sermon)
        db.session.commit()

        # Prepare response with full URLs
        thumbnail_url = f"/api/v1/video_sermon/thumbnails/{thumbnail_filename}" if thumbnail_filename else None
        video_url = f"/api/v1/video_sermon/stream_video/{video_sermon.id}"

        return jsonify({
            "message": "Video sermon created successfully",
            "sermon_id": video_sermon.id,
            "sermon": {
                "id": video_sermon.id,
                "title": video_sermon.title,
                "description": video_sermon.description,
                "file_path": video_url,  # Return streaming URL
                "thumbnail": thumbnail_url,
                "uploaded_at": video_sermon.uploaded_at.isoformat() if video_sermon.uploaded_at else None,
                "preacher": video_sermon.preacher
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating video sermon: {e}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get all video sermons
@video_sermons_bp.route('/list_video_sermons', methods=['GET'])
def list_video_sermons():
    try:
        sermons = VideoSermon.query.all()
        return jsonify([{
            "id": sermon.id,
            "title": sermon.title,
            "description": sermon.description,
            "file_path": f"/api/v1/video_sermon/stream_video/{sermon.id}",
            "thumbnail": f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None,
            "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
            "preacher": sermon.preacher
        } for sermon in sermons])
    except Exception as e:
        logger.error(f"Error listing video sermons: {e}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a video sermon by id
@video_sermons_bp.route('/get_video_sermons/<int:id>', methods=['GET'])
def get_video_sermon(id):
    try:
        sermon = VideoSermon.query.get(id)
        if sermon:
            thumbnail_url = f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None
            video_url = f"/api/v1/video_sermon/stream_video/{sermon.id}"
            return jsonify({
                "id": sermon.id,
                "title": sermon.title,
                "description": sermon.description,
                "file_path": video_url,
                "thumbnail": thumbnail_url,
                "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
                "preacher": sermon.preacher
            })
        else:
            return jsonify({"message": "Video sermon not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching video sermon: {e}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a video sermon by id
@video_sermons_bp.route('/update_video_sermons/<int:id>', methods=['PUT'])
def update_video_sermon(id):
    try:
        data = request.form
        sermon = VideoSermon.query.get(id)

        if not sermon:
            return jsonify({"message": "Video sermon not found"}), 404

        # Update fields
        sermon.title = data.get('title', sermon.title)
        sermon.description = data.get('description', sermon.description)
        sermon.preacher = data.get('preacher', sermon.preacher)

        # Handle video file upload if a new video file is provided
        video_file = request.files.get('file')
        if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
            # Delete the old file if it exists
            if os.path.exists(sermon.file_path):
                try:
                    os.remove(sermon.file_path)
                except Exception as e:
                    logger.error(f"Error deleting old video file: {e}", exc_info=True)
            
            # Save new video file
            video_filename = secure_filename(video_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            video_filename = f"{timestamp}_{video_filename}"
            video_path = os.path.join(VIDEO_UPLOAD_FOLDER, video_filename)
            video_file.save(video_path)
            sermon.file_path = video_path

        # Handle thumbnail file upload if a new thumbnail file is provided
        thumbnail_file = request.files.get('thumbnail')
        if thumbnail_file and allowed_file(thumbnail_file.filename, ALLOWED_THUMBNAIL_EXTENSIONS):
            # Delete the old thumbnail if it exists
            if sermon.thumbnail_path:
                old_thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail_path)
                if os.path.exists(old_thumbnail_path):
                    try:
                        os.remove(old_thumbnail_path)
                    except Exception as e:
                        logger.error(f"Error deleting old thumbnail: {e}", exc_info=True)
            
            # Save new thumbnail
            thumbnail_filename = secure_filename(thumbnail_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
            thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename)
            thumbnail_file.save(thumbnail_path)
            sermon.thumbnail_path = thumbnail_filename

        db.session.commit()

        # Prepare response with full URLs
        thumbnail_url = f"/api/v1/video_sermon/thumbnails/{sermon.thumbnail_path}" if sermon.thumbnail_path else None
        video_url = f"/api/v1/video_sermon/stream_video/{sermon.id}"

        return jsonify({
            "message": "Video sermon updated successfully",
            "sermon": {
                "id": sermon.id,
                "title": sermon.title,
                "description": sermon.description,
                "file_path": video_url,
                "thumbnail": thumbnail_url,
                "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
                "preacher": sermon.preacher
            }
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating video sermon: {e}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a video sermon by id
@video_sermons_bp.route('/delete_video_sermons/<int:id>', methods=['DELETE'])
def delete_video_sermon(id):
    try:
        sermon = VideoSermon.query.get(id)
        if not sermon:
            return jsonify({"message": "Video sermon not found"}), 404

        # Delete the video file from the server
        if os.path.exists(sermon.file_path):
            try:
                os.remove(sermon.file_path)
            except Exception as e:
                logger.error(f"Error deleting video file: {e}", exc_info=True)

        # Delete the thumbnail if it exists
        if sermon.thumbnail_path:
            thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail_path)
            if os.path.exists(thumbnail_path):
                try:
                    os.remove(thumbnail_path)
                except Exception as e:
                    logger.error(f"Error deleting thumbnail: {e}", exc_info=True)

        db.session.delete(sermon)
        db.session.commit()

        return jsonify({"message": "Video sermon deleted successfully"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting video sermon: {e}", exc_info=True)
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Fetch YouTube videos dynamically
@video_sermons_bp.route('/youtube_videos', methods=['GET'])
def get_youtube_videos_route():
    try:
        videos = get_youtube_videos()
        return jsonify({"videos": videos}), 200
    except Exception as e:
        logger.error(f"Error in youtube_videos route: {e}", exc_info=True)
        return jsonify({"message": "Unable to fetch YouTube videos", "error": str(e)}), 500