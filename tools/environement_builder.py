#!/usr/bin/python3
"""environment_builder.py

This script downloads and unpacks programs from crackmes.one websites.
Command example : python3 environment_builder.py <configure file>
Author : Jim00000
"""

import configparser
import logging
import os
import os.path
import pathlib
import re
import stat
import sys
import traceback
import urllib.request
import zipfile

from threading import Lock
from threading import Thread
from time import sleep


class MyTimer(Thread):
    def __init__(self, event, interval: float = 1.0):
        Thread.__init__(self)
        self.handler = event
        self.interval = interval
        self.__terminate = False
        self.__lock = Lock()

    def run(self):
        while self.terminate() is False:
            sleep(self.interval)
            self.handler()

    def terminate(self):
        self.__lock.acquire(True)
        _terminate = self.__terminate
        self.__lock.release()
        return _terminate

    def end(self):
        self.__lock.acquire(True)
        self.__terminate = True
        self.__lock.release()
        self.join()


def absPath(file) -> str:
    return pathlib.Path(file).absolute()


def getSuffix(file) -> str:
    return pathlib.Path(file).suffix


def getDownloadFileNameFromURL(url) -> str:
    result = re.match(r'.*/(\w+\.zip)', url)
    return result.group(1)


def printDownloadTick():
    print('.', end='', flush=True)


def main(argc, argv):
    logging.info(
        'You are using environment builder script to build the environment')

    if argc <= 1:
        logging.critical('Lack of the parameter : config file (.ini)')
        raise Exception

    configName = argv[1]
    logging.info('configName = {arg}'.format(arg=absPath(configName)))

    if not os.path.isfile(configName):
        logging.error("Can not read {conf}".format(conf=configName))
        raise Exception

    if getSuffix(configName) != '.ini':
        logging.error("{conf} is not a .ini file".format(conf=configName))
        raise Exception

    conf = configparser.ConfigParser()
    conf.read(configName)

    url = conf['crackmes.one']['URL']
    logging.info('url = %s' % url)

    zipfilename = getDownloadFileNameFromURL(url)
    logging.info('zipfilename = %s' % zipfilename)

    # Download that zip
    logging.info('Start to download %s' % zipfilename)
    print('Download %s' % zipfilename, end='', flush=True)
    timer = MyTimer(printDownloadTick, 0.5)
    timer.start()
    urllib.request.urlretrieve(url, zipfilename)
    timer.end()
    print('complete')
    logging.info('%s has been downloaded' % zipfilename)

    zippwd = conf['crackmes.one']['ZipPwd']
    logging.info('zip password = %s' % zippwd)
    bin = conf['crackmes.one']['Bin']
    logging.info('target binary = %s' % bin)

    # Unzip that file
    logging.info('unzip %s', zipfilename)
    with zipfile.ZipFile(zipfilename, 'r') as zip:
        zip.setpassword(pwd=zippwd.encode('ascii'))
        currentPath = pathlib.Path().absolute()
        zip.extract(bin, currentPath)
        logging.info('{bin} has been extracted to {path}'.format(
            bin=bin, path=currentPath))

    # Change the mode of that binary to be executable
    os.chmod(bin, os.stat(bin).st_mode | stat.S_IEXEC)

    logging.info('Done. Environment building process terminates.')


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    try:
        if sys.version_info[0] != 3:
            logging.critical('This script needs python3 to work')
            raise Exception
        main(len(sys.argv), sys.argv)
    except Exception as e:
        logging.critical(
            'Exception occurs ! this program terminates accidentally!')
        logging.debug(traceback.format_exc())
