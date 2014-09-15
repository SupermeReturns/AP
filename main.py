#!/usr/bin/python
#-*- coding: utf-8 -*-

#启动文件，在启动用户界面
import wx
import os
import sys
import Frames

#改变环境变量，今后加载文件方便
dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
os.chdir(dir)

def main():
    app = wx.App(redirect = False)
    frame = Frames.MainFrame()
    frame.Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()


