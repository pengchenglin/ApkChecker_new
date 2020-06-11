#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from filetools import *
from config import *
import zipfile
from logzero import logger
import shutil


class CheckApp:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.result_path = out_name

    def write_config(self, pak_path):
        '''修改配置文件'''
        if os.path.exists(out_path):
            shutil.rmtree(out_path)
        os.mkdir(out_path)
        config_str = read_file(config_path)
        config_json = json.loads(config_str)
        config_json['--apk'] = pak_path
        config_json['--output'] = self.result_path
        config_json.update()
        del_files(config_path)
        write_file(config_path, json.dumps(config_json, indent=4), is_cover=True)

    def update_config(self, aab=False):
        '''判断是否为aab 后修改配置文件'''
        if aab:
            self.build_apks(self.apk_path, config.tmp_apks_path)
            apk = self.get_base_master_apk(config.tmp_apks_path)
            self.write_config(apk)
        else:
            self.write_config(self.apk_path)

    def check_app(self, aab=False):
        '''执行脚本 运行matrix'''
        if aab:
            self.build_apks(self.apk_path, config.tmp_apks_path)
            apk = self.get_base_master_apk(config.tmp_apks_path)
            self.write_config(apk)
            try:
                logger.info("开始matrix检查app")
                cmd = "java -jar {} --config {}".format(matrix_path, config_path)
                logger.info(cmd)
                subprocess.call(cmd, shell=True)
                del_files(apk)
                logger.info("检查app完成!")
            except Exception as e:
                logger.error("检查app异常!{}".format(e))
        else:
            self.write_config(self.apk_path)
            try:
                logger.info("开始matrix检查app")
                cmd = "java -jar {} --config {}".format(matrix_path, config_path)
                logger.info(cmd)
                subprocess.call(cmd, shell=True)
                logger.info("检查app完成!")
            except Exception as e:
                logger.error("检查app异常!{}".format(e))

    def build_apks(self, bundle_path, tmp_apks_path):
        '''aab生成apks'''
        logger.info('开始使用bundletool build apks')
        code = 'java -jar %s build-apks  --bundle=%s --output=%s --overwrite' % \
               (config.bundle_tool_path, bundle_path, tmp_apks_path)
        subprocess.check_output(code, shell=True)

    def get_base_master_apk(self, apks_path):
        '''从apks 解压master_apk'''
        logger.info('从apks 解压master_apk')
        apks = zipfile.ZipFile(apks_path, 'r')
        print(apks.namelist())
        # print(apks.infolist()[0].file_size)
        for f in apks.namelist():
            if 'base-master.apk' in f:
                apks.extract(f, config.project_path)
                master_apk_path = os.path.join(config.project_path, f)
                return master_apk_path
        else:
            logger.error('apks %s 没有找到base-master.apk' % apks_path)

