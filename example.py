# coding=utf-8

from pyftp_wrapper import PyFTP

if __name__ == '__main__':
    import requests

    with PyFTP('localhost', 'user', 'password') as ftp:
        print(ftp.listdir())  # print list of file and directory

        # 1. upload file by requests object
        with requests.get('http://httpbin.org/image/jpeg', stream=True) as response:
            ftp.put(response, 'image.jpg')

        # 2. download file from remote
        ftp.get('image.jpg', 'image.jpg')

        # 3. make dirs and change directory
        ftp.mkdir('images')
        with ftp.cd('images'):
            print(ftp.getcwd())  # /images
            ftp.mkdir('copy')
            ftp.put('image.jpg', 'copy/image.jpg')  # upload file by local path
        print(ftp.getcwd())  # /

        # 4. check is file or directory
        print(ftp.isfile('images'))  # False
        print(ftp.isdir('images'))  # True

        # 5. recursively copy remote dir structure to local
        ftp.get_r('images', 'images')
