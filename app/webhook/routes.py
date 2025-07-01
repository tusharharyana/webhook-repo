from flask import Blueprint, request, jsonify
from datetime import datetime
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if not data or not event_type:
        return jsonify({"error": "Missing data or event type"}), 400

    try:
        action = event_type.upper()

        event = {
            "request_id": None,
            "author": None,
            "action": action,
            "from_branch": None,
            "to_branch": None,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

        if action == "PUSH":
            event["request_id"] = data.get("after")  # commit hash
            event["author"] = data.get("pusher", {}).get("name")
            event["to_branch"] = data.get("ref", "").split("/")[-1]

        elif action == "PULL_REQUEST":
            event["request_id"] = str(data.get("number"))  # PR ID
            event["author"] = data.get("sender", {}).get("login")
            event["from_branch"] = data.get("pull_request", {}).get("head", {}).get("ref")
            event["to_branch"] = data.get("pull_request", {}).get("base", {}).get("ref")

        elif action == "MERGE":
            pass

        else:
            return jsonify({"message": f"Unhandled event type: {action}"}), 400

        mongo.db.events.insert_one(event)
        return jsonify({"message": "Event stored successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
