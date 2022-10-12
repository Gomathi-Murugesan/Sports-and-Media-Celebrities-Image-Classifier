from flask import Flask, request, jsonify, render_template
from api import util
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/app2/classify_image', methods = ['GET', 'POST'])
def classify_image():
    image_data = request.form['image_data']
    ## web server sends the image as base64 through request method
    response = jsonify(util.classify_image(image_data))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Celebrity Image Classification")
    util.load_saved_artifacts()
    #app.run(port=5001)
    app.run(host='0.0.0.0',port=5001)