__author__ = 'gongxingfa'

import urllib2
from meinheld import server
import redis

r = redis.StrictRedis(host='localhost', port=6379)

backed_image_url = 'http://tucoo.com/logo_class/telecom_logo04/images/Geek.png'


def images(environ, start_response):
    query_string = environ['QUERY_STRING']
    params = {parm.split('=')[0]: parm.split('=')[1] for parm in query_string.split('&')}
    s = params['s']
    upper = params['upper1']
    key = s + ':' + upper
    img_data = r.get(key)
    if not img_data:
        img_data = urllib2.urlopen(backed_image_url).read()
        r.set(key, img_data)
    rsp = img_data
    status = '200 OK'
    response_headers = [
        ('Content-type', 'image/png'),
        ('Content-Length', str(len(rsp)))]
    start_response(status, response_headers)
    return [rsp]


server.listen(("0.0.0.0", 8000))
server.run(images)