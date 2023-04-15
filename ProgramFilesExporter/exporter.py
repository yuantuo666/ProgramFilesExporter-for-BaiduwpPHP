from json import load as loadJSON
from json import dumps as dumpsJSON
import os
import re
import shutil
import sys
import zipfile
from os import path


def uploadLanzou(name='ProgramFiles.zip'):
    shutil.copy('../ProgramFiles/ProgramFiles.zip', name)
    from lanzou.api import LanZouCloud

    def show_progress(file_name, total_size, now_size):
        """显示进度的回调函数"""
        percent = now_size / total_size
        bar_len = 40  # 进度条长总度
        bar_str = '>' * round(bar_len * percent) + \
            '=' * round(bar_len * (1 - percent))
        print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
            percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
        if total_size == now_size:
            print('')  # 下载完成换行

    def handler(fid, is_file):
        if is_file:
            info = lzy.get_share_info(fid)
            print('下载链接：', info.url)

    lzy = LanZouCloud()
    cookie = {'ylogin': os.getenv("YLOGIN"), 'phpdisk_info': os.getenv("PHPDISK_INFO")}
    if (lzy.login_by_cookie(cookie) != 0):
        print('登录失败！')
        return False
    print('登录成功！')

    if lzy.upload_file(name, 7438632, callback=show_progress, uploaded_handler=handler) != 0:
        print('上传失败！')
        return False

    print('上传成功！')


try:  # 尝试读取排除规则列表
    with open('./exclude-list.json', encoding="utf-8") as f:
        excludeList = loadJSON(f)
except Exception as e:  # 若读取失败
    print('读取排除规则列表失败！')
    print(e)
    sys.exit(1)


files = []

try:  # 尝试获取文件列表
    for name in os.listdir("../"):
        flag = False  # 是否匹配到排除规则
        for i in excludeList:  # 获取排除列表
            if re.search(i, name) != None:  # 若匹配到排除规则
                flag = True
                break
        # 若未匹配到排除规则则添加到文件列表
        files.append('../' + name) if flag == False else None
except Exception as e:  # 若获取失败
    print('获取文件列表失败！')
    print(e)
    sys.exit(1)


if files == []:
    print('没有文件需要导出！')
    sys.exit(0)


try:  # 尝试复制文件
    if not path.exists('../ProgramFiles/'):  # 若文件夹不存在则创建
        os.mkdir('../ProgramFiles/')
    for root, dirs, subFiles in os.walk('../ProgramFiles/', topdown=False):  # 清空文件夹
        for name in subFiles:
            os.remove(path.join(root, name))
        for name in dirs:
            os.rmdir(path.join(root, name))
    for name in files:  # 复制文件和文件夹
        shutil.copytree(name, '../ProgramFiles/' + name[3:]) if path.isdir(
            name) else shutil.copy(name, '../ProgramFiles/')
    print('导出成功！')
    print('-' * 20)
    print('正在压缩中……')
    try:  # 压缩
        # 提前获取 walk 结果，防止把在压缩过程中把不完整的压缩包一并压入压缩包
        walkResult = tuple(os.walk('../ProgramFiles/'))
        f = zipfile.ZipFile('../ProgramFiles/ProgramFiles.zip',
                            'w', zipfile.ZIP_DEFLATED)  # 创建压缩包
        try:
            for root, dirs, subFiles in walkResult:  # 压缩文件
                for name in subFiles:
                    f.write(path.join(root, name), '%s/%s' %
                            (root.replace('../ProgramFiles/', ''), name), compresslevel=9)
            print('压缩成功！')
        except Exception as e:
            print('压缩失败！')
            print(e)
            sys.exit(1)
        finally:
            f.close()
    except Exception as e:
        print('压缩失败！')
        print(e)
        sys.exit(1)

except Exception as e:
    print('复制文件失败！')
    print(e)
    print('您可以自行复制这些文件：')
    print(dumpsJSON(files))
    sys.exit(1)


if uploadLanzou(os.getenv("FILE_NAME")) == False:
    sys.exit(1)
