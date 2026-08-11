from flask import Flask, request, jsonify
from flask_cors import CORS

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
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    user_id = data.get("user_id")
    title = data.get("title")
    category = data.get("category")
    description = data.get("description")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    address = data.get("address")

    if not title or not category or not description:
        return jsonify({
            "success": False,
            "message": "Title, category and description are required"
        }), 400

    report_id = create_report(
        user_id=user_id,
        title=title,
        category=category,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address
    )

    if report_id is None:
        return jsonify({
            "success": False,
            "message": "Could not create report"
        }), 400

    return jsonify({
        "success": True,
        "message": "Report submitted successfully",
        "report_id": report_id
    }), 201


@app.route("/api/reports", methods=["GET"])
def fetch_reports():
    reports = get_reports()

    return jsonify({
        "success": True,
        "reports": reports
    }), 200


@app.route("/api/reports/<int:report_id>", methods=["GET"])
def fetch_single_report(report_id):
    report = get_single_report(report_id)

    if report is None:
        return jsonify({
            "success": False,
            "message": "Report not found"
        }), 404

    return jsonify({
        "success": True,
        "report": report
    }), 200


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