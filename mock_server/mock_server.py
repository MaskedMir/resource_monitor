from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/api/<int:server_id>')
def stats(server_id):
    return jsonify({
        "cpu": random.randint(10, 95),
        "mem": f"{random.randint(20, 90)}%",
        "disk": f"{random.randint(30, 80)}%",
        "uptime": f"{random.randint(1, 30)}d {random.randint(0, 23)}h {random.randint(0, 59)}m"
    })

if __name__ == '__main__':
    app.run(port=5000)