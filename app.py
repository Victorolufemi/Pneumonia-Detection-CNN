from keras.models import load_model
from keras.models import model_from_json
from flask import Flask,url_for,render_template,redirect,session,Response
import os
import cv2
from flask import Flask, request, render_template
from keras.models import load_model
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = True
# load json and create model
json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("models/model.h5")

def output_string(classification):
    if classification == 0:
        return 'The Patient has no Pneumonia Disease'
    else:
        return 'The Patient has a pneumonia Disease, Kindly go the nearest Hospital for checkup'

@app.route('/')
def home():
    return render_template('index.html')
img_size= 150
def predict(sample, model):
    # Some preprocessing
    img = cv2.imread(sample)
    img = cv2.resize(img,(img_size, img_size))
    #img =img.reshape(-1, img_size, img_size, 1)
    img = img.reshape(-1, img_size, img_size, 1)
    predicts = (model.predict(img)> 0.5).astype("int32")
    prediction = predicts.reshape(1,-1)[0]
# this will be an array with one element
    return prediction[0]
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        render_template('index.html')
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['pneumonia']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path)
        local_file_path = '/static/uploads/' + f.filename;
        prediction = predict(file_path, loaded_model)
        classification = ""
        if prediction == 0:
            classification = 'The Patient has no Pneumonia Disease'
        else:
            classification = 'The Patient has a pneumonia Disease, Kindly go the nearest Hospital for checkup'

        return render_template('index.html',classification=classification, file=local_file_path)
port = int(os.environ.get('PORT'))

if __name__== '__main__':
    app.run(host='0.0.0.0', port=port)
