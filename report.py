from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from logzero import logger
import time
import os
import config
from getdata import GetData
from filetools import *
from config import *
import json
from flask import render_template


def get_report_path(package, aab=False):
    '''
    创建报告文件夹路径
    '''

    report_folder = os.path.join(config.project_path, "Report")
    if not os.path.exists(report_folder):
        os.mkdir(report_folder)
    if aab:
        package_folder = os.path.join(report_folder, package + '_aab')
    else:
        package_folder = os.path.join(report_folder, package)
    if not os.path.exists(package_folder):
        os.mkdir(package_folder)
    reports_folder = os.path.join(package_folder, "reports")
    if not os.path.exists(reports_folder):
        os.mkdir(reports_folder)
    report_path = os.path.join(reports_folder, "report_{}.html".format(time.strftime("%Y%m%d%H%M%S")))
    logger.info('报告路径 %s' % report_path)
    return report_path, reports_folder, package_folder


def write_rsjson(package_path, context):
    """
    更新指定包文件夹下的rs.json
    :param path: 指定包报告文件夹路径
    :param context: 新生成的报告的信息 dict
    :return:
    """
    js_path = os.path.join(package_path, 'rs.json')
    if not os.path.exists(js_path):
        with open(js_path, 'w') as f:
            tmp_info = {'last': '', 'total': []}
            json.dump(tmp_info, f)
    rs_str = read_file(js_path)
    rs_json = json.loads(rs_str)
    rs_json['last'] = context
    tmp_total = rs_json['total']
    tmp_total.insert(0, context)
    rs_json['total'] = tmp_total
    rs_json.update()
    del_files(js_path)
    write_file(js_path, json.dumps(rs_json, indent=4), is_cover=True)
    return js_path


def creat_report(html_path, filename, aab=False):
    '''
    /templates/report_template.html模板，生成单次报告,并更新rs.json
    '''

    gd = GetData()
    base_info = gd.get_base()
    pkg_info = gd.get_pkg_info()
    apk_info = gd.make_entries()
    apk_detail = gd.get_html_table()
    if pkg_info['package'] in internalapp:
        if aab:
            appname = internalapp[pkg_info['package']] + '_aab'
        else:
            appname = internalapp[pkg_info['package']]
    else:
        if aab:
            appname = pkg_info['package'] + '_aab'
        else:
            appname = pkg_info['package']

    context = {
        'filename': os.path.basename(filename),
        'package': pkg_info['package'],
        'appname': appname,
        'versionName': pkg_info['versionName'],
        'apksize': base_info['apksize'],
        'minSdkVersion': pkg_info['minSdkVersion'],
        'targetSdkVersion': pkg_info['targetSdkVersion'],
        'versionCode': pkg_info['versionCode'],
        'appinfo': apk_info,
        'appdetail': apk_detail,
        'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    logger.info('生成报告：%s' % html_path)
    if aab:
        apks_info = GetData().get_apks_size_info()
        context.update(apks_info)
        with open(html_path, 'w') as f:
            html = render_template("report_template_aab.html", context=context)
            f.write(html)
            f.close()
        del_files(config.tmp_apks_path)
        pkg = context['package'] + '_aab'

    else:
        with open(html_path, 'w') as f:
            html = render_template("report_template.html", context=context)
            f.write(html)
            f.close()
            pkg = context['package']
    logger.info('报告生成完成')
    context.pop('appinfo')
    context.pop('appdetail')
    context.update({'report_path': os.path.join('./', pkg, 'reports', os.path.basename(html_path))})
    return context


def make_script_str(info_list):
    """
    组装折线图
    :param info_list:
    :return:
    """
    time_list = []
    size_list = []
    try:
        for r in reversed(info_list):
            t = "%s(%s)" % (r['create_time'], r['versionCode'])
            s = float(r['apksize'])
            # time_list += t
            time_list.append(t)
            # size_list += s
            size_list.append(s)
    except Exception as e:
        logger.error("组装资源分布异常!{}".format(e))
    finally:
        return time_list, size_list


def get_report_folders():
    if not os.path.exists(config.report_folder):
        mk_dir(config.report_folder)
        return None
    else:
        os.listdir(config.report_folder)
        packages = {}
        for i in os.listdir(config.report_folder):
            if not os.path.exists(os.path.join(config.report_folder, i, 'rs.json')):
                pass
            else:
                rs_str = read_file(os.path.join(config.report_folder, i, 'rs.json'))
                rs_json = json.loads(rs_str)
                packages.update({i: rs_json['last']})
        return packages

# def create_statistics_html(package_path, aab=False):
#     '''/templates/index.html模板 生成 tongji.html'''
#     name = os.path.join(package_path, "statistics.html")
#     reports_info = json.loads(read_file(os.path.join(package_path, 'rs.json')))
#
#     package = reports_info['last']['package']
#     report_list = reports_info['total']
#     script_list = make_script_str(report_list)
#     pacages = get_packages()
#     context = {
#         'urls': report_list,
#         'size_list': script_list[1],
#         'time_list': script_list[0],
#         'package': package,
#         'packages': pacages
#
#     }
#     logger.info('生成统计报告：%s' % name)
#     if aab:
#         with open(name, 'w', encoding="utf-8") as f:
#             html = render_template('/templates/statistics_template_aab.html', context)
#             f.write(html)
#             f.close()
#
#     else:
#         with open(name, 'w', encoding="utf-8") as f:
#             # html = render_template('/templates/statistics_template.html', context)
#             html = render_template('/templates/dashboard.html', context)
#             f.write(html)
#             f.close()
#     logger.info('统计报告生成成功')
#
#
# def _get_report_list(report_folder):
#     """
#     获取报告
#     :param report_folder:
#     :return:
#     """
#
#     report_list = []
#     for file in os.listdir(report_folder):
#         if file.split('.')[-1] == 'html':
#             report_list.append(file)
#     report_list.sort(reverse=True)
#     return report_list
#
#
# def _get_report_info(reports_path, report_name):
#     '''获取每个设备报告的参数'''
#     report = os.path.join(reports_path, report_name)
#     report_path = os.path.join('./reports', report_name)
#     result = {}
#     with open(report, 'r', encoding='utf-8') as f:
#         soup = BeautifulSoup(f, "html.parser")
#         appinfo = str(soup.find(id='appInfoDiv').get_text()).split()
#         report_time = str(soup.find('h1').get_text()).split('报告 ')
#         result["package"] = appinfo[1]
#         result["versionName"] = appinfo[3]
#         result["versionCode"] = appinfo[5]
#         result['apksize'] = appinfo[7]
#         result['create_time'] = report_time[1]
#         result['report_path'] = str(report_path)
#         f.close()
#     return result
