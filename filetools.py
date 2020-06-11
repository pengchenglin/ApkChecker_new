#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 常用操作类
"""

import os, re, time, subprocess, sys
import config
from logzero import logger

sys.path.append('..')


def write_file(filename, content, is_cover=False):
    '''
    写入文件 覆盖写入
    :param filename:
    :param content:
    :param is_cover:是否覆盖写入
    :return:
    '''
    try:
        newstr = ""
        if isinstance(content, list or tuple):
            for str in content:
                newstr = newstr + str + "\n"
        else:
            newstr = content
        if is_cover == True:
            file_mode = "wb"
        else:
            file_mode = "ab"
        with open(filename, file_mode) as f_w:
            f_w.write(newstr.encode())
            logger.info('写{}文件完成'.format(filename))
    except Exception as e:
        logger.info('{}写入异常!{}'.format(filename, e))


def del_files(filename):
    '''删除文件'''
    try:
        if os.path.exists(filename):
            subprocess.call("rm -rf {}".format(filename), shell=True)
            logger.info('删除{}完成!'.format(filename))
    except Exception as e:
        logger.info('删除{}异常!{}'.format(filename, e))


def mk_dir(foldername):
    '''
    创建文件目录
    :return:
    '''
    try:
        if not os.path.exists(foldername):
            subprocess.call("mkdir {}".format(foldername), shell=True)
            logger.info('创建{}完成!'.format(foldername))
    except Exception as e:
        logger.info('创建{}异常!'.format(foldername, e))


def read_file(filename):
    '''
    读取文件
    :return:
    '''
    result = ''
    try:
        with open(filename, "r") as f_r:
            result = f_r.read()
    except Exception as e:
        logger.info('{}读取异常!{}'.format(filename, e))
    finally:
        return result


def get_size(org):
    '''
    计算apk大小
    :return:
    '''
    new = str(round(float(org) / (1024 * 1024), 2))
    return new


def build_apks(bundle_path, tmp_apks_path):
    code = 'java -jar %s build-apks  --bundle=%s --output=%s --overwrite' % \
           (config.bundle_tool_path, bundle_path, tmp_apks_path)
    return subprocess.check_output(code, shell=True)


def get_apks_size(apks_path):
    code = 'java -jar %s get-size total --apks=%s' % (config.bundle_tool_path, apks_path)
    size = subprocess.check_output(code, shell=True)
    return size


def get_file_list(folder, key='apk'):
    """
    获取报告
    :param report_folder:
    :return:
    """

    report_list = []
    for file in os.listdir(folder):
        if file.split('.')[-1] == key:
            report_list.append(file)
    report_list.sort()
    return report_list


if __name__ == '__main__':
    # print(get_apks_size('/Users/linpengcheng/Desktop/install_for_mac/apk/tmp.apks'))
    # print(get_apks_size('/Users/linpengcheng/Desktop/install_for_mac/apk/tmp.apks'))

    print(get_size('39995932'))
    print(get_size('40956975'))
