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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def rotMap(zfile, angle):
    print('main function invoked')
    l = []
    try:
        theta = radians(int(angle))
    except ValueError as e:
        print(e)
        theta = angle

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
            print l
            for i in range(len(l)):
                out.writestr(l[i]['zipInfoObj'], z.read(l[i]['zipInfoObj']))
                print('wrote image to zip')
            out.writestr('Manifest.xml', ET.tostring(root))

    with open(tempname, 'rb') as f:
        resp = make_response(f.read())
    resp.headers['Content-Type'] = 'application/zip'
    resp.headers['Content-Disposition'] = 'attachment; filename='+name+'.cl'
    shutil.rmtree(tempdir)
    return resp


def iterChild(child, l, theta):
    print('starting to iter child')
    i = int(child.find('Floor').text)
    width = l[i]['size'][0]
    height = l[i]['size'][1]
    x = float(child.find('.Position/X').text)
    y = float(child.find('.Position/Y').text)
    x_cart = x - 0.5*width
    y_cart = 0.5*height - y
    if theta == 'mirror_x':
        x_rotated = -x_cart
        y_rotated = y_cart
    elif theta == 'mirror_y':
        x_rotated = x_cart
        y_rotated = -y_cart
    else:
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
            angle = request.form['angle']
            r = rotMap(filePath, angle)
            #os.remove(filePath)
            return r
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5280)
