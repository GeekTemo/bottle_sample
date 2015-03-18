__author__ = 'gongxingfa'

from meinheld import patch

patch.patch_all()

from meinheld import server
from bottle import Bottle, request, Response, response, static_file

import redis

images_root = '/Users/gongxingfa/PycharmProjects/bottle_sample/sample/images'
app = Bottle()

backed_image_url = 'http://tucoo.com/logo_class/telecom_logo04/images/Geek.png'

import urllib2
r = redis.StrictRedis(host='localhost', port=6379)

# /image/?s=A02-B05-C02-H04&upper1=AH5
@app.route('/image/', method='GET')
def cache_image():
    params = request.params
    s = params['s']
    upper = params['upper1']
    key = s + ':' + upper
    img_data = r.get(key)
    if not img_data:
        img_data = urllib2.urlopen(backed_image_url).read()
        r.set(key, img_data)
    response.set_header('Content-Type', 'image/png')
    return img_data
