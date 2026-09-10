from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import os
import uuid
from werkzeug.utils import secure_filename

from database import create_tables
from auth import register_user, login_user
from reports import create_report, get_reports, get_single_report
from admin import (
    get_admin_reports,
    get_admin_report,
    change_report_status
)


# Create Flask application
app = Flask(__name__)

# Allow frontend to communicate with Flask
CORS(app)
# Upload folder for complaint images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create database tables when the application starts
create_tables()


# ---------------------------------------------------
# HOME / HEALTH CHECK
# ---------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "LokSahay backend is running"
    })


# ---------------------------------------------------
# AUTHENTICATION APIs
# ---------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Name, email and password are required"
        }), 400

    user_id = register_user(name, email, password)

    if user_id is None:
        return jsonify({
            "success": False,
            "message": "Email is already registered"
        }), 409

    return jsonify({
        "success": True,
        "message": "Registration successful",
        "user_id": user_id
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    user = login_user(email, password)

    if user is None:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": user
    }), 200


# ---------------------------------------------------
# CIVIC REPORT APIs
# ---------------------------------------------------

@app.route("/api/reports", methods=["POST"])
def submit_report():
    # Get text fields from multipart/form-data
    user_id = request.form.get("user_id")
    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    address = request.form.get("address")

    # Validate required fields
    if not title or not category or not description:
        return jsonify({
            "success": False,
            "message": "Title, category and description are required"
        }), 400

    # Handle image upload
    image_filename = None
    image = request.files.get("issueImage")

    if image and image.filename:

        # Allowed image types
        allowed_extensions = {
            "jpg",
            "jpeg",
            "png",
            "webp"
        }

        original_filename = secure_filename(image.filename)

        if "." not in original_filename:
            return jsonify({
                "success": False,
                "message": "Invalid image file"
            }), 400

        extension = original_filename.rsplit(".", 1)[1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "success": False,
                "message": "Only JPG, JPEG, PNG and WEBP images are allowed"
            }), 400

        # Create a unique filename
        image_filename = f"{uuid.uuid4().hex}.{extension}"

        # Save image
        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                image_filename
            )
        )

    # Create report
    report_id = create_report(
        user_id=user_id,
        title=title,
        category=category,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address,
        image_filename=image_filename
    )

    if report_id is None:
        return jsonify({
            "success": False,
            "message": "Failed to submit report"
        }), 500

    return jsonify({
        "success": True,
        "message": "Report submitted successfully",
        "report_id": report_id
    }), 201

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ---------------------------------------------------
# ADMIN APIs
# ---------------------------------------------------

@app.route("/api/admin/reports", methods=["GET"])
def fetch_admin_reports():
    reports = get_admin_reports()

    return jsonify({
        "success": True,
        "reports": reports
    }), 200


@app.route("/api/admin/reports/<int:report_id>", methods=["GET"])
def fetch_admin_report(report_id):
    report = get_admin_report(report_id)

    if report is None:
        return jsonify({
            "success": False,
            "message": "Report not found"
        }), 404

    return jsonify({
        "success": True,
        "report": report
    }), 200


@app.route("/api/admin/reports/<int:report_id>/status", methods=["PUT"])
def update_status(report_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    status = data.get("status")

    if not status:
        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    updated = change_report_status(report_id, status)

    if not updated:
        return jsonify({
            "success": False,
            "message": "Invalid status or report not found"
        }), 400

    return jsonify({
        "success": True,
        "message": "Report status updated successfully",
        "report_id": report_id,
        "status": status
    }), 200


# ---------------------------------------------------
# RUN FLASK SERVER
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)