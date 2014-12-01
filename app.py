from io import BytesIO
from PIL import Image
from math import cos, sin, radians

import xml.etree.cElementTree as ET
import zipfile


def main(zfile, angle):
    l = []
    theta = radians(angle)
    with zipfile.ZipFile(zfile, 'r') as z:
        root = ET.fromstring(z.read('Manifest.xml'))
        for child in root.iterfind('.//FloorUrls//Path'):
            image = Image.open(BytesIO(z.read(child.text)))
            l.append({'zipInfoObj': z.getinfo(child.text), 'size': image.size})
        for child in root.iterfind(".//FloorData//Location"):
            i = child.find('Floor').text
            width = l[i]['size'][0]
            height = l[i]['size'][1]
            x = child.find('.Position/X').text
            y = child.find('.Position/Y').text
            x_cart = x - 0.5*width
            y_cart = 0.5*height - y
            x_rotated = (x_cart*cos(theta)) - (y_cart*sin(theta))
            y_rotated = (x_cart*sin(theta)) + (y_cart*cos(theta))
            child.find('.Position/X').text = x_rotated
            child.find('.Position/Y').text = y_rotated
        with open('output.xml', 'w') as out:
            out.write(root)
