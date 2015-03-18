__author__ = 'gongxingfa'

from gevent import monkey;

monkey.patch_all()

from bottle import run, route, request, response, static_file
from PIL import Image
import urllib2
import StringIO
import os
import redis

backed_image_url = 'http://tucoo.com/logo_class/telecom_logo04/images/Geek.png'
images_root = '/Users/gongxingfa/PycharmProjects/bottle_sample/sample/images'

r = redis.StrictRedis(host='localhost', port=6379)

# /image/?s=A02-B05-C02-H04&upper1=AH5
@route('/image/')
def images():
    params = request.params
    s = params['s']
    upper = params['upper']
    key = s + '-' + upper
    image_path = r.get(key)
    if not image_path:
        img_data = urllib2.urlopen(backed_image_url).read()
        img_buffer = StringIO.StringIO(img_data)
        img = Image.open(img_buffer)
        image_path = key + ".png"
        img.save(os.path.join(images_root, image_path))
        img.close()
        r.set(key, image_path)
    return static_file(image_path, images_root)

run(host='0.0.0.0', port=8080, server='gevent')