import os

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload():
    if request.method == "OPTIONS": 
        return _build_cors_preflight_response()
    elif request.method == "POST":
        img = request.files['uploadImg']
        img.save(os.path.join(os.getcwd(), "uploads", img.filename))
        return _corsify_actual_response(jsonify({"hello": "world"}))
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))



def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)