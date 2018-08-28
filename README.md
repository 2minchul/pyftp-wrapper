# pyftp-wrapper
More high level ftp client wrapper based on [pyftp](https://github.com/adyzng/pyftp).

Based on Python 3

## What's different?

- 생성자에서 port를 받을 수 있습니다.
- 파일 업로드시 여러가지 타입을 지원합니다.
  - path string
  - file-like object
  - bytes
  - [requests](https://github.com/requests/requests) object
- `pyftp`의 몇몇 오류가 수정 되었습니다.
- 추후 여러가지 사소하지만 편리한 기능을 추가 할 계획입니다.

## How to use

See `example.py`

```python
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

```

기본적인 기능은 [pyftp](https://github.com/adyzng/pyftp)의 문서를 참고해 주세요.
