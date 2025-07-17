import os
from backend_ML.BackEnd import main
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload():
    if request.method == "OPTIONS": 
        return _build_cors_preflight_response()
    elif request.method == "POST":
        img = request.files['uploadImg']
        path = os.path.join(os.getcwd(), 'uploads', img.filename)
        if not os.path.exists(path):  #? Check if the image doesn't already exist
            print(path)
            forward_slash_path = path.replace('\\', '/')
            img.save(forward_slash_path)
            res = main(forward_slash_path)

            print(_corsify_actual_response(jsonify({"message": res})))  
            return _corsify_actual_response(jsonify({"message": res}))
        else:
            return _corsify_actual_response(jsonify({"message": "Image already exists"}))
    else:
        raise RuntimeError("Internal Error: {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)