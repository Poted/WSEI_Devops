from flask import Flask, jsonify
import datetime
import os
import redis

app = Flask(__name__)

try:
    cache = redis.Redis(host='redis-db', port=6379, decode_responses=True)
except Exception as e:
    cache = None

@app.route('/')
def home():
    count = "Redis connection not available"
    
    if cache:
        try:
            count = cache.incr('hits')
        except redis.exceptions.ConnectionError:
            pass

    return jsonify({
        "status": "running",
        "service": "devops-project-app",
        "timestamp": str(datetime.datetime.now()),
        "visitor_count": count
    })

@app.route('/info')
def info():
    return jsonify({
        "author": "Student",
        "environment": os.environ.get("ENV", "development")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)