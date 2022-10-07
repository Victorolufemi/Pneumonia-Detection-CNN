from email.mime import image
from tkinter.ttk import Style
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

