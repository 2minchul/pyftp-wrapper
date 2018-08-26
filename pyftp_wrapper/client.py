# coding=utf-8
import os
import io
import ftplib

import pyftp


class FTP(ftplib.FTP):

    def __init__(self, host='', user='', passwd='', acct='',
                 timeout=ftplib._GLOBAL_DEFAULT_TIMEOUT, port=None, source_address=None):
        self.source_address = source_address
        self.timeout = timeout
        if host:
            if port:
                self.connect(host, port)
            else:
                self.connect(host)
            if user:
                self.login(user, passwd, acct)


class PyFTP(pyftp.PyFTP):

    def __init__(self, host, username='', password='', port=None):
        self.host, self.port, self.type = pyftp.ftp_host(host, port)
        self.user, self.pswd = username, password
        self.ftp = FTP(self.host, port=self.port)
        self._conn = False
        self.connect()

    def listdir(self, pathname=None):
        """get files/dirs under path

        :param str|None pathname
            dir path name
        :return list
            return stat list of specified pathname
        """
        with self.cd(pathname or '.'):
            d_list = self.ftp.nlst()

        return d_list

    def isfile(self, pathname):
        """check is file or not"""
        if self.isdir(pathname):
            return False
        else:
            if self.exists(pathname):
                return True
            return False

    def exists(self, pathname):
        """check if file or folder exist"""
        return os.path.basename(pathname) in self.listdir(os.path.dirname(pathname))

    def get_r(self, remotedir, localdir, preserve_mtime=False):
        """recursively copy remotedir structure to localdir

        :param str remotedir: the remote directory to copy from
        :param str localdir: the local directory to copy to
        :param bool preserve_mtime: *Default: False* -
            preserve modification time on files

        :returns: list
            (dirs_cnt, files_cnt)
        :raises:
            IOError if path not exist
        """
        if not os.path.exists(localdir):
            os.makedirs(localdir, exist_ok=True)

        return super(self.__class__, self).get_r(remotedir, localdir, preserve_mtime)

    def put_fp(self, fp, remotepath=None):
        """Copies a file between the local host and the remote host.

        :param fp: A file-like object with a read(num_bytes) method.
        :param str remotepath:
            the remote path, else the remote :attr:`.pwd` and filename is used.

        :raises IOError:
            if epath doesn't exist
        """
        self.ftp.storbinary('STOR %s' % remotepath, fp)

    def put(self, local, remotepath=None):
        """Copies a file between the local host and the remote host.

        :param str|object local: the local path and filename string or file-like object
        :param str remotepath:
            the remote path, else the remote :attr:`.pwd` and filename is used.

        :raises IOError:
            if epath doesn't exist
        """
        if isinstance(local, str):
            return self.put_by_path(local, remotepath)
        elif isinstance(local, bytes):
            fp = io.BytesIO(local)
            return self.put_fp(fp, remotepath)
        elif hasattr(local, 'raw'):
            return self.put_fp(local.raw, remotepath)
        elif hasattr(local, 'read'):
            return self.put_fp(local, remotepath)

    def get_by_path(self, remotepath, localpath=None, preserve_mtime=False):
        return super(self.__class__, self).get(remotepath, localpath, preserve_mtime)

    def put_by_path(self, localpath, remotepath=None, preserve_mtime=False):
        return super(self.__class__, self).put(localpath, remotepath, preserve_mtime)
