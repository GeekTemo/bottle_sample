__author__ = 'gongxingfa'

import random
import requests
from datetime import datetime


def test_request():
    url = 'http://127.0.0.1:8000/image/?'
    start = datetime.now()
    for i in range(1000):
        url += 's=' + str(random.randint(1, 1000)) + "&upper1=" + str(random.randint(1, 1000))
        requests.get(url)
    end = datetime.now()
    print 'Time:'+str(end - start)


if __name__ == '__main__':
    test_request()