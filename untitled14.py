#!/usr/bin/python3
from flask import render_template, request, redirect, url_for, Flask,send_from_directory
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json

from matrix_apply import apply_output_order
#Flask object initialization
#app flask object has to be created before importing views below
#because it calls "import app from app"
UPLOAD_FOLDER = 'static\\uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
COLORS = {'green' : (0,255,0.4*255), 'blue' : (0,0.39*255,255), 'red' : (255,0,0), 'purple' : (0.8*255,0,1*255), 'yellow' : (0.8*255,255,0)}

def init_app(app):
    "Initialize app object. Create upload folder if it does not exist."
    if not os.path.isabs(app.config['UPLOAD_FOLDER']):
        folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
        app.config['UPLOAD_FOLDER'] = folder
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
init_app(app)


#File extension checking
def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submitted_file = request.files['file']
        path = os.path.join(os.getcwd(),os.path.join('uploads','hello.jpg'))
        submitted_file.save(path)
        return json.dumps(parsePhoto(path))

    return app.send_static_file('index.html')


def avg(arr):
    return round(sum(arr) / len(arr))


def getColor(c, data):
    loss = np.apply_along_axis(lambda x: np.dot(c - x, c - x), 2, data)
    min_loss = min(loss.reshape(-1))
    max_loss = max(loss.reshape(-1))
    loss = (loss - min_loss) / max_loss
    plt.imshow(loss, cmap='gray')
    y, x = np.where(loss < 0.07)
    return average(x), average(y)

def average(arr):
    return round(sum(arr) / len(arr))

def parsePhoto(filename):
    size = 128, 128
    img = Image.open(filename)
    img.load()
    img.thumbnail(size, Image.ANTIALIAS)
    data = np.asarray(img, dtype="int32")
    points = {key : getColor(value, data) for key, value in COLORS.items()}

    plt.imshow(img) #, cmap='gray')
    for x,y in points.values():
        plt.scatter(x,y,s=40)

    apply_output_order()
    plt.show()
    return sortArrayByX(points)


def sortArrayByX(d):
    toStr = lambda v: ','.join(map(str, v))
    dupside = {toStr(v): k for k, v in d.items()}
    arr = sorted(d.values(), key=lambda x: x[0])
    return list(map(lambda x: (dupside[toStr(x)], x), arr))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
