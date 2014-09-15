						      Account_Protector
总体功能：集中管理账户。提供安全保护,方便使用的功能。

具体功能：
       1.对账户信息进行加密。
	2.提供账户的检索，查看，修改，创建，导入，导出等功能。
	3.提供友好的图形用户界面。

实现概况：
	1.加密实现：对信息加密存储到硬盘中，使用时对其解密。（可以提供密码，但是为了方便，可以手动取消）
	2.提供图形界面：使用wx图形界面模块。
	3.账户编辑功能：检索，查看，修改，创建，导入，导出
实现细节：
	实现3个类型：加密，图形界面，编辑功能。
	
加密算法：
    使用base64模块进行加密，然后在对于已经加密字符串进行二次处理。 解密时逆序操作。
搜索算法：
    只需要匹配即可（想出方法计算匹配值）
设计用户界面：
    Done(加密解密的界面合二为一)
    
    
文件结构：
    main.py:负责调用全局
    Alg.py：提供算法
    Frames.py：提供图形用户界面
main.py:
  def main():

Frames.py:
  class MainFrame(wx.Frame):
    def __init__(self):
    def load_UI(self):
    def OnQuit(self, event):
  
  class Mod_Notebook(self, parent):
    def __init__(self, key==None):
    def turn_page(self, key==None):
  
  class SearchPanel(wx.Panel, listmix.ColumnSorterMix):
  “”“
  显示搜索结果的面板。每次搜索的时候面板的内容都会更新。
  ”“”
    def __init__(self, parent):
    def load_UI(self):
    def OnView(self, event):
    def OnButtonClicked(self, event):
    def OnItemSelected(self, event):
    def OnDoSearch(self, event):
    def CreateDynamicButton(self, info):
    def MakeMenu(self):
    def PopulateList(self, list):
      得到list,然后更新列表显示

    
        该表 分为3列，门户，摘要，最后修改时间。然后在接下来的行中加入每个账户。
  class EditPanel(wx.Panel):
    def __init__(self, parent):
    def load_UI(self):
    def save_edition(self, event):
    def load_account(self, key):
    def OnClickedImport(self, event):
    def OnFile(event):
    def OnDir(self, event):
    
  class Mod_ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
  “”“
  表示搜索面板中的list，每次搜索重新可以更新。
  “”“
    def OnItemSelected(self, event):
    def OnItemDeselected(self, event):
    def GetAllSelected(self):
    def GetLastSelected(self):
    

    
Alg.py:
  def generate_pass(length = 21):
  
  def check_prev_char(password, current_char_set):
  
  class Manager:
    def __init__(self):
    def most_recent(self):
      """
      返回最近使用过的一些账户。点击过，查看过，写改过都算是使用过。最多返回使用过的账户数量是20个，允许返回了0。（返回列表）
      """
    def search(self, wd, confg):
      “”“
      使用关键词wd进行查询，然后返回列表（有顺序的列表）
      ”“”
    def grasp_intro(self, key):
      “”“
      str表示一个账户索引。该方法分析该条账户的内容，首先尝试分析出其中的账户名， 邮箱等有关表示的且没有安全相关的内容。如果不成功的话，就返回最开始的5个字。
      记住在最后的地方加上“...”。
      ”“”
    def get_button_info(self, key):
      “”“
      str表示一个账户的索引。最后放回的是一个词典。代表分析出来的数据。数据类型可以有email, account, password...
      ”“”
    def save_file(self):
      """
      结束之前保存程序运行中的数据。（保存之前先进行加密）
      """
    def get_account(self, key):
      “”“
      根据key索引，返回该账户中的内容。
      ”“”
    def generate_password(self, length = 21):
    def generate_name(self):
    def generate_email(self):
    def save_edition(self, folder_path):
    def add_folder(self, folder_path):
    def add_file(self, file_path):
    
  Class File_Manager:
    def __init__(self)
    def read_init(self, file_path, confg, confg_path)
    def sava_all(self,file, file_path, confg, confg_path)
    def read_file(self,path):
    def save_file(self,dt,path):
    def read_confg(self, path):
    def sava_confg(self,confg, confg_path):
    def encrypt(self, content):
    def decrypt(self, content):
    def dismantle_data(self, data):
    def assemble_data(self, category, data):
    def add_folder(self, path):
    def add_file(self,file_path):
    
    
  Class Search_Engine:
    def __init__(self):
    def query(str, confg):
    
    

不同类别的账号加载一起

开头：列有目录，不同的名字拥有不同的


SearchCtrl:用于搜索框子使用（在Recent Additions/Updates）
TreeMixin(用于整体的框架)


显示搜索结果的panel:

目前最好ListControl

查看全部的内容：使用 treectrl


备选StaticBox

stockbutton



选中的按钮：
platebutton中的Normal w/Menu       or     Square/Small   or


安全识别方法：  

    1.使用IP地址（我的IP是固定的）
    2.上网的网卡MAC
    3.机器码决定


菜单如何不显示：statusbar主动显示的只是最上面的菜单栏目，如果需要显示就需要重新调用EVT.MENU_HIGHTLIGHT写的事件


小型修改：
   1.关于status的优化
   2.如果处理recent search 中菜单项目重复的情况

当什么都没有的时候里面时会有数据的（存储的是最经尝试后的一些账号）
   3.最经常使用的账号
   4.如何调整大小，使其固定