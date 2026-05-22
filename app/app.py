from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/process", methods=["POST"])
def process():
    if not request.is_json:
        return jsonify({"error": "Only JSON allowed"}), 400

    data = request.get_json()

    required = ["shipment_id", "destination", "status"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = {
        "shipment_id": str(data["shipment_id"]),
        "destination": str(data["destination"]),
        "status": str(data["status"])
    }

    return jsonify({"status": "processed", "result": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
