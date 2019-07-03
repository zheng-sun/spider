import requests

class Request(object):

    # 发送请求
    def send_request(self, url, callback):
        print('send_request')
        print(url)
        print(callback)
        response = requests.get(url=url)
        callback(response)