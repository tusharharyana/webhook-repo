from flask import Blueprint, jsonify
from app.extensions import mongo

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/events', methods=['GET'])
def get_events():
    # Fetch last 10 events from MongoDB
    events = mongo.db.events.find().sort('timestamp', -1).limit(10)

    formatted = []
    for e in events:
        author = e.get("author")
        action = e.get("action")
        from_branch = e.get("from_branch")
        to_branch = e.get("to_branch")
        raw_ts = e.get("timestamp")
        if isinstance(raw_ts, dict) and "$date" in raw_ts:
            timestamp = raw_ts["$date"]
        elif hasattr(raw_ts, "isoformat"):
            timestamp = raw_ts.isoformat() + " UTC"
        else:
            timestamp = str(raw_ts)

        request_id = e.get("request_id")

        # Format message
        if action == "PUSH":
            message = f'{author} pushed to {to_branch} on {timestamp}'
        elif action == "PULL_REQUEST":
            message = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}'
        elif action == "MERGE":
            message = f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
        else:
            message = f'{author} performed {action} on {timestamp}'

        formatted.append({
            "message": message,
            "timestamp": timestamp,
            "action": action,
            "author": author,
            "request_id": request_id
        })

    return jsonify(formatted)
