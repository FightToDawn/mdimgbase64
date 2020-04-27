import base64
import sys
import re
import win32con
import win32clipboard as w 
from PIL import ImageGrab
#import pyperclip
import time
import os

recent_value = ""
recent_im = None

print('Markdown截图自动转base64到剪贴板服务已开启...    [ctrl+c]停止')
while True:
    #tmp_value = pyperclip.paste() 			# 读取剪切板复制的内容
    try:
        #if tmp_value != recent_value:				 #如果检测到剪切板内容有改动
            #recent_value = tmp_value
            # 读取剪贴板中的位图 保存为文件
        tmp_im = ImageGrab.grabclipboard()
        if tmp_im != None:
            if recent_im == None or (tmp_im.width != recent_im.width and tmp_im.height != recent_im.height):
                recent_im = tmp_im

                file_path = '截图' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.png'
                tmp_im.save(file_path)

                # 读入图片数据 然后base64后复制到剪贴板
                f=open(file_path,'rb') #二进制方式打开图文件
                ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
                f.close()

                #删除文件
                os.remove(file_path)

                str_base64 = str(ls_f, encoding = "utf-8")
                #print(str_base64)

                #添加markdown图片头 [图片名]:data:image/png;base64,
                #image_name = re.search(r'\\.*\\(.*?)\.',file_path, re.M|re.I)
                image_name = re.search(r'([^<>/\\\|:""\*\?]+)\.\w+$',file_path, re.M|re.I).group(1)
                str_base64 = '[' + image_name + ']:data:image/png;base64,' + str_base64

                # 复制到剪贴板
                w.OpenClipboard()
                w.SetClipboardData(win32con.CF_UNICODETEXT,str_base64)
                w.CloseClipboard()
                print('图片[' + image_name + ']base64编码已复制到剪贴板中！')

        time.sleep(0.1)
    except KeyboardInterrupt:  # 如果有ctrl+c，那么就退出这个程序。  （不过好像并没有用。无伤大雅）
        break




# w.OpenClipboard()
# b = w.GetClipboardData(win32con.BS_BITMAP)
# print(b)
# w.CloseClipboard()

# if len(sys.argv) == 1:
#     file_path = input("\n\n请输入要base64的图片文件路径：")
# else:
#     file_path = sys.argv[1]

