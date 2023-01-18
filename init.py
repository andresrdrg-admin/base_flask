"""The flask application"""
#!/usr/bin/env python3

from flask import Flask, Response  # pylint: disable=import-error

from routes.example_routes import RoutesExample

app = Flask(__name__)

@app.route("/", methods=['GET'])

def main():
    return Response("Connected")

RoutesExample(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
