#!/usr/bin/python
#-*- coding: utf-8 -*-

#描述用户界面外观，调用算法
import wx
import sys
import os
import images
import webbrowser
import time
import wx.lib.mixins.listctrl as listmix
from Alg import Manager

accountdata = {
1: ("126", "asdafsdlfasdfasd","2013-10-25"),
2: ("360", "asaflsdjfalsdjfasdf","2013-10-25"),
3: ("adobe", "asjldfajsdlfas","2013-10-25"),
4: ("Amazon", "ajsdlfajdlgg","2013-10-25"),
5: ("Avast","adasdf asdfasd s","2013-10-25"),
6: ("58","ajsdfhasldgjasldf","2013-10-25")
  }

class MainFrame(wx.Frame):
    """MainFrame 是所有的控件的父亲，负责初始化各种窗口"""
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Account Protector", size = (400, 600))
        self.manager = Manager()
        self.load_UI()

    def load_UI(self):
        """加载窗口组件"""
        #创建底部状态栏，显示当前操作信息
        self.bkg = wx.Panel(self, size=(400, 600))
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu = wx.Menu()

        #创建顶部菜单栏
        item = menu.Append(-1, "&Widget Inspector\tF6", "Show the wxPython Widget Inspection Tool")
        item = menu.Append(-1, "E&xit\tCtrl-Q", "Exit demo")
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.button_quit = wx.Button(self.bkg, label="quit")
        self.notebook = Mod_Notebook(self.bkg, self.manager)

        #create layout
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.button_quit)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook,1,wx.EXPAND)
        sizer.Add(hsizer, 0)
        self.bkg.SetSizer(sizer)
        #绑定事件
        self.button_quit.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, event):
        self.manager.save_file()
        self.Close()




class Mod_Notebook(wx.Notebook):
    """Mod_Notebook 显示如同翻页一般的控件，包含SearchPanel, EditPanel"""
    def __init__(self,parent, manager):

        wx.Notebook.__init__(self,parent, id=-1,size= (21,21),style=wx.BK_DEFAULT )
        self.parent = parent
        self.manager = manager
        self.search_win = SearchPanel(self)

        self.AddPage(self.search_win,"search")

        self.edit_win = EditPanel(self)
        self.AddPage(self.edit_win, "edit")

    def turn_page(self, key=None):
        if key:
            #假如不为空，翻页需要加载数据到窗口中
            self.ChangeSelection(1)         #1.翻页 
            self.edit_win.load_account(key) #2.加载数据



class SearchPanel(wx.Panel,listmix.ColumnSorterMixin):
    """搜索页面"""
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1)
        self.parent = parent
        self.manager = self.parent.manager
        self.load_UI()


    def load_UI(self):
        #搜索框
        self.search =  wx.SearchCtrl(self, size=(200,-1),style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        self.search.SetMenu(self.MakeMenu())

        #载入图片
        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())

        #“查看全文”按钮
        self.view = wx.Button(self, label="see all")
        self.list = Mod_ListCtrl(self, wx.NewId() ,                            #搜索结果显示栏
                                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        most_recent = self.manager.most_recent()
        self.PopulateList(most_recent)   #初始化列表

        self.itemDataMap = accountdata
        #账户操作按钮（动态合成）
        box = wx.StaticBox(self, -1, "copy")
        test_button = wx.Button(self, label="password")
    
        #create LayOut
        self.bsizer = wx.StaticBoxSizer(box,wx.HORIZONTAL)
        self.bsizer.Add(test_button, 0, wx.TOP|wx.LEFT,10) 
        
        hsizer= wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.bsizer, 1, wx.EXPAND|wx.ALL, 25)
        hsizer.Add(self.view)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search,1)
        sizer.Add(self.list,1,wx.EXPAND)
        sizer.Add(hsizer)
        
        self.SetSizer(sizer)
        #关联事件
        self.Bind(wx.EVT_BUTTON, self.OnView, self.view)
        #self.Bind(wx.EVT_BUTTON, self.OnButtonClicked, self.bsizer)#账户按钮操作区点击
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)   #当列表中的选项被选中的时候
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)#搜索动作


    def OnView(self, event):
        #1.判断是否选中
        selected = self.list.GetLastSelected()
        #2.如果有效则转到另一Page
        if selected:
            text = self.list.GetItemText(selected)
            self.parent.turn_page(text)


    def OnButtonClicked(self, event):
        #1.获得相应的数据
        obj = event.GetEventObject()
        text = obj.GetLabel()
        self.button_info[text]
        #2.复制数据到clipboard中
        text_data = wx.TextDataObject(text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()


    def OnItemSelected(self, event):
        #1.获得选中门户
        currentItem = event.m_itemIndex()
        text = self.list.GetItemText(currentItem)
        #2.根据门户向manager请求数据
        self.button_info = self.manager.get_button_info(text)
        #3.构造按钮
        self.CreateDynamicButton(self.button_info)


    def OnDoSearch(self,evt):
        #1.添加菜单项到recent search
        input = self.search.GetValue()
        self.CreateMenuItem(input)
        #2.启动搜索动作
        menu = self.search.GetMenu
        if menu.IsChecked(102):  #按标题搜索
            ordered_list = self.manager.search(input, "name")
            self.PopulateList(ordered_list)
        elif menu.IsChecked(103):  #按内容搜索
            ordered_list = self.manager.search(input, "content")
            self.PopulateList(ordered_list)
        elif menu.IsChecked(104):  #谷歌搜索
            url = "https://www.google.com/search?q=%s&ie=UTF-8" % (input)
            webbrowser.open(url)
        elif menu.IsChecked(105): #百度搜索
            url ="http://www.baidu.com/s?wd=%s&ie=utf-8" % (input)
            webbrowser.open(url)


    def CreateDynamicButton(self, info):
        """根据info字典动态创建按钮"""
        #1.清空以前的按钮
        self.bsizer.Clear()
        #2.创建新的按钮添加到self.bsizer
        for b in info:
           button = wx.Button(self, label=b)
           self.bsizer.Add(button, 0 ,wx.TOP|wx.LEFT, 10)
        
        self.bsizer.Layout()


    def CreateMenuItem(self, str):
        """为recent search中添加新的菜单项"""        
        menu = self.search.GetMenu()
        item = menu.FindItemById(101)
        submenu = item.GetSubMenu()
        ID = 1011+submenu.GetMenuItemCount()
        submenu.Append(ID, str,str)
        

    def MakeMenu(self):
        """
        搜索偏好设置
        暂时想法：
        1.谷歌搜索
        2.百度搜索
        3.出现之前搜索过的关键词
        4.搜索文本
        5.搜索文件名 
        """
        #create menu/menuitem
        menu = wx.Menu()
        sub_menu = wx.Menu()
        menu.AppendMenu(101, "&Recent Search", sub_menu)

        menu.AppendSeparator()
        
        menu.Append(102, "search title", "", wx.ITEM_RADIO)
        menu.Append(103, "search content", "", wx.ITEM_RADIO)
        menu.Append(104, "search Baidu", "", wx.ITEM_RADIO)
        menu.Append(105, "search Google", "", wx.ITEM_RADIO)
        #link event
        
        return menu
    

    def PopulateList(self, list):
        """用于初始化列表"""
        #1.添加表头
        if 0:
            # for normal, simple columns, you can add them like this:
            self.list.InsertColumn(0, 'site')
            self.list.InsertColumn(1, "preview", wx.LIST_FORMAT_RIGHT)
            self.list.InsertColumn(2, "creation date")
        else:
            # but since we want images on the column header we have to do it the hard way:
            info = wx.ListItem()
            info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info.m_image = -1
            info.m_format = 0
            info.m_text = "site"
            self.list.InsertColumnInfo(0, info)

            #info.m_format = wx.LIST_FORMAT_RIGHT
            info.m_text = "preview"
            self.list.InsertColumnInfo(1, info)
            
            info.m_format = 0
            info.m_text = "last edited"
            self.list.InsertColumnInfo(2, info)

        #2.添加数据
        items = list.items()
        for key, data in items:
            index = self.list.InsertImageStringItem(sys.maxint, key, self.idx1)
            self.list.SetStringItem(index, 1, data[0])
            self.list.SetStringItem(index, 2, data[1])
            self.list.SetItemData(index, 1234)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, 100)

        # show how to select an item如何”软点击“数据
        self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # show how to change the colour of a couple items   如何设置颜色
        item = self.list.GetItem(1)
        item.SetTextColour(wx.BLUE)
        self.list.SetItem(item)   
        item = self.list.GetItem(4)
        item.SetTextColour(wx.RED)
        self.list.SetItem(item)

        
    def GetListCtrl(self):
        return accountdata
        


        
class EditPanel(wx.Panel):
    """编辑帐户页面"""
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,-1)
        self.parent = parent
        self.manager = self.parent.manager
        self.load_UI()


    def load_UI(self):
        #create controls
        text = wx.StaticText(self, -1, "filename")
        self.filename = wx.TextCtrl(self,size=(210,25))
        
        self.contents = wx.TextCtrl(self, size=(390,260),
                               style=wx.TE_MULTILINE|wx.HSCROLL)
        
        self.button_test1 = wx.Button(self,label="password")
        self.button_test2 = wx.Button(self,label="account name")
        self.button_test3 = wx.Button(self,label="email")
        
        self.import_button = wx.Button(self, label="load")
        self.save_button =wx.Button(self, label="save")
        #制作右键弹出菜单
        self.popupID = []
        self.popupID.append(wx.NewId())
        self.popupID.append(wx.NewId())
        
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.popupID[1],"One")
        bmp = images.Smiles.GetBitmap()
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        menu.Append(self.popupID[0], "load from file")
        menu.Append(self.popupID[1], "load from directory")

        #create layout
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(text)
        hsizer1.Add(self.filename, 1, wx.EXPAND)
        
        box = wx.StaticBox(self, -1, "auto add")
        bsizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        bsizer.Add(self.button_test1, 0, wx.TOP|wx.LEFT, 10)
        bsizer.Add(self.button_test2, 0, wx.TOP|wx.LEFT, 10)
        bsizer.Add(self.button_test3, 0, wx.TOP|wx.LEFT, 10)
        
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(self.import_button)
        hsizer2.Add(self.save_button)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1)
        sizer.Add(self.contents)
        sizer.Add(bsizer)
        sizer.Add(hsizer2)
        
        self.SetSizer(sizer)
        #事件绑定
        self.Bind(wx.EVT_MENU, self.OnFile, id=self.popupID[0])
        self.Bind(wx.EVT_MENU, self.OnDir, id=self.popupID[1])
        self.Bind(wx.EVT_BUTTON, self.autoadd,self.button_test1)
        self.Bind(wx.EVT_BUTTON, self.autoadd,self.button_test2)
        self.Bind(wx.EVT_BUTTON, self.autoadd,self.button_test3)
        self.Bind(wx.EVT_BUTTON, self.save_edition, self.save_button)
        self.Bind(wx.EVT_BUTTON, self.OnClickImport, self.import_button)


    def save_edition(self, event):
        title = self.filename.GetValue()
        content = self.content.GetValue()
        time = time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
        self.manager.save_edition(tile, content, time)


    def load_account(self,key):
        """根据key在文本框中加载数据"""
        info = self.manager.get_account(key)
        self.filename.ChangeValue(key)
        self.content.ChangerValue(info[0])


    def autoadd(self,event):
        """自动添加密码，账号，邮箱"""
        obj = event.GetEventObject()
        label = obj.GetLabel()
        #复制内容到文本框中
        if label == 'password':
            text = self.manager.generate_password()
            self.content.Append('\n' + 'password: '+text)
        elif label == 'account name':
            text = self.manager.generate_name()
            self.content.Append('\n' + 'account_name: '+text)
        elif label == 'email':
            text = self.manager.generate_email()
            self.content.Append('\n' + 'email: '+text)
        text_data = wx.TextDataObject(text)
        #复制内容到剪切板
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()

            
    def OnClickImport(self, event):            
        self.PopupMenu(self.popupmenu, self.import_button.GetPosition())


    def OnFile(self,event):
        """从文件中导入账户"""
        dlg = wx.FileDialog(
            self,message='chooose file',
            defaultDir=os.getcwd(),
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                self.manager.add_file(path)

        
    def OnDir(self, event):
        """从文件夹中导入"""
        dlg = wx.DirDialog(self, "choose a directory", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            self.manager.add_folder(path)


                

class Mod_ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """列表控件，以表的方式显示账户"""
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.selected = []
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemDeselected)


    def OnItemSelected(self,event):
        currentItem = event.m_itemIndex
        self.selected.append(currentItem)


    def OnItemDeselected(self, event):
        currentItem = event.m_itemIndex
        index = self.selected.index(currentItem)
        del self.selected[index]


    def GetAllSelected(self):
        return self.selected[:]


    def GetLastSelected(self):
        l = len(self.selected)
        if l:
            return self.selected[l-1]
        else:
            return None