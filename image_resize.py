__author__ = 'keqiao'
import numpy as np
from PIL import Image
import sys

def pix_middle(pix):
    x,y,z,h=0,0,0,0
    n = len(pix[0])
    if n == 3:
        for p in pix:
            x = x+p[0]
            y = y+p[1]
            z = z+p[2]
        pix = [int(x/len(pix)),int(y/len(pix)),int(z/len(pix))]
    elif n == 4:
        for p in pix:
            x = x+p[0]
            y = y+p[1]
            z = z+p[2]
            h = h+p[3]
        pix = [int(x/len(pix)),int(y/len(pix)),int(z/len(pix)),int(h/len(pix))]
    return pix
def image_optimize(image):
    im = Image.open(image)
    x0 = im.size[0]
    
    y0 = im.size[1]
    data = im.getdata()
    cl_format = len(data[0])
    data = np.array(data)
    data.shape = y0,x0,cl_format
    return data,x0,y0,cl_format

def tiwce(image):
    data,x0,y0,cl_format = image_optimize(image)
    new_data = np.arange(x0*y0*4*cl_format)
    new_data.shape = x0*2,y0*2,cl_format
    for i in range(0,x0):
        for j in range(0,y0):
            new_data[i*2,j*2] = data[j,i]
    for m in range(0,x0*2,2):
        for n in range(1,(y0-1)*2,2):
            if cl_format == 1:
                new_data[m,n] = (new_data[m,n+1]+new_data[m,n-1])/2
            elif cl_format in (3,4):
                new_data[m,n] = pix_middle((new_data[m,n+1],new_data[m,n-1]))
    for m in range(1,(x0-1)*2,2):
        for n in range(0,2*y0,2):
            if cl_format == 1:
                new_data[m,n] = (new_data[m+1,n]+new_data[m-1,n])/2
            elif cl_format in (3,4):
                new_data[m,n] = pix_middle((new_data[m+1,n],new_data[m-1,n]))
    for i in range(2*x0):
        new_data[i,y0*2-1] = new_data[i,y0*2-2]
    for j in range(2*y0):
        new_data[x0*2-1,j] = new_data[x0*2-2,j]
    for m in range(1,(x0-1)*2,2):
        for n in range(1,(y0-1)*2,2):
            if cl_format == 1:
                new_data[m,n] = (new_data[m+1,n]+new_data[m-1,n]+new_data[m,n-1]+new_data[m,n+1])/4
            elif cl_format in (3,4):
                new_data[m,n] = pix_middle((new_data[m+1,n],new_data[m,n-1],new_data[m+1,n],new_data[m-1,n]))
    print (new_data[0,0])
    if cl_format == 1:
        new = Image.new('L',(x0*2,y0*2))
    elif cl_format == 3:
        new = Image.new('RGB',(x0*2,y0*2))
    elif cl_format == 4:
        new = Image.new('RGBA',(x0*2,y0*2))
    for i in range(x0*2):
        for j in range(y0*2):
            new.putpixel([i,j],tuple(new_data[i,j]))
    new.save('new1.png')

if len(sys.argv) == 2:
    image_name = sys.argv[1]
    tiwce(str(image_name))

else:
    print (u'Usage:\n--Image name')