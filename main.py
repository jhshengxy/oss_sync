#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 15:21
# @Author  : Shengxy
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from os import listdir
from os.path import isfile, join
import time
import logging
import oss2

FILE_PATH = 'E:\\Website\\UploadFiles\\'
SLEEP_TIME = 60
file_name_set = set()

OSS_ACCESS_KEY_ID = ''
OSS_ACCESS_KEY_SECRET = ''
OSS_BUCKET_NAME = ''
OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'

Prefix = 'media/'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='sync.log',
                    filemode='w')


def upload_to_oss(file):
    '''
    上传文件至阿里云
    :param file:
    :return:
    '''

    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
    print(file)
    aliyun_path = "{}{}".format(Prefix, file.replace(FILE_PATH, '')).replace('\\', '/')
    print(aliyun_path)
    try:
        with open(file, 'rb') as fileobj:
            result = bucket.put_object(aliyun_path, fileobj)
        if result.status == 200:
            return True
        else:
            return False
    except  Exception as e:
        logging.error(e)
        return False


def scan_file(scan_path, is_init=False, is_upload=False):
    '''
    扫描文件夹方法
    :param scan_path:
    :param is_init:
    :param is_upload:
    :return:
    '''
    for f in listdir(scan_path):
        if isfile(join(scan_path, f)):
            file_name = join(scan_path, f)
            if is_init:
                file_name_set.add(file_name)
                continue

            if is_upload:
                if file_name in file_name_set:
                    continue
                else:
                    is_success = upload_to_oss(file_name)
                    if is_success:
                        file_name_set.add(file_name)
                        log_str = "file :{} have been uploaded...".format(file_name)
                        print(log_str)
                        logging.info(log_str)

        else:
            scan_file(join(scan_path, f), is_init=is_init, is_upload=is_upload)


def init_set(scan_path):
    '''
    初始化set，把现有的文件都加入到set中
    :param scan_path:
    :return:
    '''
    scan_file(scan_path, is_init=True, is_upload=False)
    log_str = "init set finished,{} files have been add to set".format(len(file_name_set))
    print(log_str)
    logging.info(log_str)


if __name__ == '__main__':
    while (True):
        if len(file_name_set) <= 0:
            init_set(FILE_PATH)

        scan_file(FILE_PATH, is_init=False, is_upload=True)

        log_str = 'scan finished sleep {} seconds'.format(SLEEP_TIME)
        print(log_str)
        logging.info(log_str)
        time.sleep(SLEEP_TIME)
