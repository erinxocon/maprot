# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
from math import cos, sin, radians
from werkzeug import secure_filename
from flask import Flask, request, make_response, render_template


import os
import shutil
import zipfile
import tempfile
import xml.etree.cElementTree as ET

UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = set(['cl', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '\x84f}\xeb\xe2\x9f\xf7\xb0)\x05C\xcb\xd0w\xcf\x0e\xe8\x81q\xeb\xd2\xbf\x87#'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def rotMap(zfile, angle):
    l = []
    theta = radians(angle)
    tempdir = tempfile.mkdtemp()
    tempname = os.path.join(tempdir, 'Output.cl')

    with zipfile.ZipFile(zfile, 'r') as z:
        root = ET.fromstring(z.read('Manifest.xml'))
        name = root.find('./*/Name').text+str(angle)
        root.find('./*/Name').text = name
        for child in root.iterfind('.//FloorUrls//Path'):
            image = Image.open(BytesIO(z.read(child.text)))
            l.append({'zipInfoObj': z.getinfo(child.text), 'size': image.size})

        for child in root.iterfind('.//FloorData//Location'):
            iterChild(child, l, theta)

        for child in root.iterfind('.//MapLocation'):
            iterChild(child, l, theta)

        with zipfile.ZipFile(tempname, 'w') as out:
            for i in range(len(l)):
                out.writestr(l[i]['zipInfoObj'], z.read(l[i]['zipInfoObj']))
            out.writestr('Manifest.xml', ET.tostring(root))

    resp = make_response(open(tempname).read())
    resp.headers['Content-Type'] = 'application/zip'
    resp.headers['Content-Disposition'] = 'attachment; filename='+name+'.cl'
    shutil.rmtree(tempdir)
    return resp


def iterChild(child, l, theta):
    i = int(child.find('Floor').text)
    width = l[i]['size'][0]
    height = l[i]['size'][1]
    x = int(child.find('.Position/X').text)
    y = int(child.find('.Position/Y').text)
    x_cart = x - 0.5*width
    y_cart = 0.5*height - y
    x_rotated = (x_cart*cos(theta)) - (y_cart*sin(theta))
    y_rotated = (x_cart*sin(theta)) + (y_cart*cos(theta))
    x_fin = x_rotated + 0.5*width
    y_fin = 0.5*height - y_rotated
    child.find('.Position/X').text = str(x_fin)
    child.find('.Position/Y').text = str(y_fin)


@app.route('/', methods=['GET', 'POST'])
def main_wimi():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filePath)
            angle = int(request.form['angle'])
            r = rotMap(filePath, angle)
            os.remove(filePath)
            return r
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host='127.0.0.1', port=5280)
