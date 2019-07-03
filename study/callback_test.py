
def hello(host):
    print('hello:%s' % host)

def callback_test(host, callback):
    callback(host)

def main():
    callback_test('http://www.baidu.com/', callback=hello)

if __name__ == '__main__':
    main()