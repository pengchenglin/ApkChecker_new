from report import *
import checkapp
import filetools
from flask import Flask

def run(file):
    '''生成详情html报告，并更新rs.json'''
    check = checkapp.CheckApp(file)
    if os.path.splitext(file)[-1][1:] == 'aab':
        check.check_app(True)
        package = GetData().get_pkg_info()['package']
        paths = get_report_path(package, True)
        info = creat_report(paths[0],file, aab=True)
        write_rsjson(paths[2], info)
    else:
        check.check_app(False)
        package = GetData().get_pkg_info()['package']
        paths = get_report_path(package, False)
        info = creat_report(paths[0], file)
        write_rsjson(paths[2], info)
    filetools.del_files(file)
    return info


if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    def test():
        folder = '/Users/linpengcheng/Downloads/1.4.0/vc_gp'
        file_list = filetools.get_file_list(folder, key='aab')
        print(file_list)
        for file in file_list:
            file_name = os.path.join(folder, file)
            run(file_name)

        # apk = '/Users/linpengcheng/Downloads/XiaoYing_V8.1.0_8-Domestic-Bv8.1.0_fix-xiaoyingtest-20200413_163627.apk'
        # run(apk)

    app.run(host='0.0.0.0', port=9876, debug=True)
