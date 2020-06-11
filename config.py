#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

internalapp = {"com.videoeditorcn.android": "videoleap视频剪辑",
               "com.videoeditorpro.android": "VivaCut GP",
               "video.star.videoeditor": "VivaCut国内",
               "video.editor.videoeditor.musicvideoeditor": "VMix GP",
               "com.vivashow.share.video.chat": "VidStatus",
               "com.quvideo.xiaoying": "小影APP",
               "com.quvideo.lite.huawei": "小影华为 Lite",
               "com.quvideo.vivavideo.lite": "小影Google lite",
               "com.quvideo.xiaoying.pro": "小影Google Pro",
               "com.quvideo.slideplus": "SlidePlus(简拍)",
               "com.quvideo.vivamini": "趣影App",
               "com.tempo.video.edit": "Tempo",
               "com.quvideo.xiaoying.vivasetting": "小影切区工具"}

project_path = os.path.abspath(os.path.dirname(__file__))
out_path = os.path.join(project_path, "out")
out_name = os.path.join(out_path, "check")
config_path = os.path.join(project_path, "check.json")
matrix_path = os.path.join(project_path, "matrix-apk-canary-0.6.5.jar")
out_json_path = os.path.join(out_path, "check.json")
out_html_path = os.path.join(out_path, "check.html")
report_folder = os.path.join(project_path, "Report")
bundle_tool_path = os.path.join(project_path, 'bundletool-all.jar')
tmp_apks_path = os.path.join(project_path, 'tmp.apks')
tmp_upload_path = os.path.join(project_path, 'upload')

taskDescription = "Unzip the apk file to dest path."
zn_taskDescription = u"解压文件信息"

taskDescription1 = "Read package info from the AndroidManifest.xml."
zn_taskDescription1 = u"AndroidManifest.xml文件信息"

taskDescription2 = "Find out the non-alpha png-format files whose size exceed limit size in desc order."
zn_taskDescription2 = u"大小超过限制大小的非alpha png格式文件"

taskDescription3 = "Show uncompressed file types."
zn_taskDescription3 = u"未压缩的文件类型"

taskDescription4 = "Find out the duplicated files."
zn_taskDescription4 = u"重复的文件"

taskDescription5 = "Find out the unused assets."
zn_taskDescription5 = u"未使用的资产"

taskDescription6 = "Show files whose size exceed limit size in order."
zn_taskDescription6 = u"按顺序显示大小超过限制大小的文件"

taskDescription7 = "Count methods in dex file, output results group by class name or package name."
zn_taskDescription7 = "计算dex文件中的方法，按类名或包名输出结果"

taskDescription8 = "Check if there are more than one library dir in the 'lib'."
zn_taskDescription8 = u"检查'lib'中是否有多个库目录"

taskDescription9 = "Count the R class."
zn_taskDescription9 = u"统计R class"

taskDescription10 = "Check if the apk handled by resguard."
zn_taskDescription10 = u"apk是否由resguard处理"
