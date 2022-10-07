from crypt import methods
from email.mime import image
from tkinter import image_names
from tkinter.ttk import Style
from unittest import result
from keras.models import load_model
from keras.models import model_from_json
from flask import Flask,url_for,render_template,redirect,session,Response
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from flask_wtf.file import file_allowed,file_required
from werkzeug.utils import secure_filename
import cv2
import numpy
import os

app = Flask(__name__)

class Detect_form(FlaskForm):
    style={'class': 'form-control'}
    image = FileField("",validators=[file_required(), file_allowed(['jpg','png','jpeg'],'Images Only!')],render_kw=style)
    submit = SubmitField("Analyze", render_kw={'class': 'btn btn-######'})



# load json and create model
json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model/model.h5")

#Create the predict function
img_size = 150
def predict(model,sample):
    img = cv2.imread(sample)
    img = cv2.resize(img,(img_size, img_size))
    predicts = (model.predict(img)> 0.5).astype("int32")
    predictions = predicts.reshape(1,-1)[0]
    return predictions


def classify(value):
    if value==0:
        return 'The Patient has no Pneumonia Disease'
    elif value==1:
        return 'The Patient has a pneumonia Disease, Kindly go the nearest Hospital for checkup'


x=0

@app.route('/', methods=['GET','POST'])

def index():
    form = Detect_form()

    if form.validate_on_submit():

        assets_dir = './static'
        imgs =form.image.data
        img_name = secure_filename(imgs.filename)

        img.save(os.path.join(assets_dir,img_name))
        global x
        x = os.path.join(assets_dir, img_name)

        return redirect(url_for('prediction'))
    return render_template('home.html', form=form)

@app.route('/result')
def prediction():

    pred_val = predict(loaded_model, x)
    result = classify(pred_val)
    os.remove(x)
    return render_template('prediction.html', result=result)


if __name__== '__main__':
    app.run()

