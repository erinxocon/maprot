from io import BytesIO
from PIL import Image
from math import cos, sin, radians

import os
import zipfile
import shutil
import tempfile
import xml.etree.cElementTree as ET


def main(zfile, angle):
    l = []
    theta = radians(angle)
    tempdir = tempfile.mkdtemp()
    tempname = os.path.join(tempdir, 'Output.cl')
    finzip = os.path.join('/Users/mike/repos/mapRotater/', zfile[:-3]+str(angle)+zfile[-3:])
    with zipfile.ZipFile(zfile, 'r') as z:
        root = ET.fromstring(z.read('Manifest.xml'))
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
    shutil.move(tempname, finzip)
    shutil.rmtree(tempdir)


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
