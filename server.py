# -*- coding: utf-8 -*-

import os, re, time, subprocess, sys, json
# from ..loggers import JFMlogging
# logger = JFMlogging().getloger()
from flask import Flask, request
from flask import render_template, send_file, jsonify
from flask_paginate import Pagination, get_page_args
import config
from filetools import read_file
from report import get_report_folders, make_script_str
from run import run
from filetools import mk_dir
from logzero import logger, logfile

app = Flask(__name__)


def get_users(users,offset=0, per_page=10):
    return users[offset: offset + per_page]


@app.route('/')
@app.route('/<package>')
def statistics(package=None):
    '''模板生成统计报告'''
    folders = get_report_folders()
    if folders:
        if not package:
            package = list(folders.keys())[0]
        else:
            pass
        if not os.path.exists(os.path.join(config.report_folder, package, 'rs.json')):
            pass
        else:
            reports_info = json.loads(read_file(os.path.join(config.report_folder, package, 'rs.json')))
            reports_info['last']['package'] = package
            report_list = reports_info['total']
            script_list = make_script_str(report_list)

            page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
            pagination_users = get_users(report_list, offset=offset, per_page=per_page)
            pagination = Pagination(
                page=page,
                per_page=per_page,
                total=len(report_list),
                record_name="users",
                css_framework="bootstrap4"
            )

            context = {
                'urls': pagination_users,
                'size_list': script_list[1],
                'time_list': script_list[0],
                'package': package,
                'folders': folders,
                'appname': reports_info['last']['appname']
            }

            if 'aab' in package:
                return render_template("dashboard_aab.html", context=context, per_page=per_page, pagination=pagination)
            else:
                return render_template("dashboard.html", context=context, per_page=per_page, pagination=pagination)
    else:
        return render_template("home.html")


@app.route('/<package>/reports/<report_path>')
def report_info(package, report_path):
    '''跳转详情报告页面'''
    file = os.path.join(config.report_folder, package, 'reports', report_path)
    return send_file(file)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''上传apk、aab文件'''
    if request.method == 'GET':
        return "is upload file ... "
    else:
        path = request.form.get('upload_path')
        file = request.files['upload_file']
        file_name = file.filename

        if os.path.splitext(file_name)[-1][1:] not in ['APK', 'apk', 'aab']:
            return jsonify({"code": 200, "info": "文件：%s 不是apk or aab，请重试" % file_name})
        else:
            base_dir = config.tmp_upload_path
            if not os.path.exists(base_dir):
                mk_dir(base_dir)
            base_dir = config.tmp_upload_path
            file.save(os.path.join(base_dir, path, file_name))
            logger.info('上传%s' % file_name)
            report_info = run(os.path.join(base_dir, path, file_name))
            return jsonify({"code": 200, "info": "%s报告生成成功，即将跳转%s" % (file_name, report_info['report_path']),
                            'report_info': report_info})


if __name__ == '__main__':
    logfile('logfile.log', mode='w')
    app.run(host='0.0.0.0', port=9877, debug=True)

