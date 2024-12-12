from flask import Flask, request, jsonify
from main import process_command, add_song, get_songs
from flask_cors import CORS

app = Flask(__name__)

CORS(app,supports_credentials=True)

@app.route("/")
def hello_world():
    return "hello world"


@app.route("/addsong", methods=["POST"])
def command():
    req = request.get_json()
    if not req:
        return jsonify({"error":"no json provided {req}"}),400
    
    print(f"started asking different server")
    
    add_song(req)

    print(f"ended asking different server")

    return jsonify({"message": "Data received successfully"}), 200

@app.route('/getsongs', methods=['GET'])
def fetch_songs():
    
    return get_songs()

if __name__ == "__main__":
    import os
    # Prevent Flask from restarting unnecessarily in some IDEs
    os.environ["FLASK_ENV"] = "development"
    app.run(host='0.0.0.0', port=5000, debug=True)