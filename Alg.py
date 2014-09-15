#!/usr/bin/python
#-*- coding: utf-8 -*-

#描述程序算法，供其他模块调用
import os
import time
import ConfigParser
import base64
from os import urandom
from random import choice
from string import maketrans

Accout_name_kw = []
Email_name_kw = []

char_set = {
    'small': 'abcdefghijklmnopqrstuvwxyz',
    'nums': '0123456789',
    'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'special': '^!\$%&/()=?{[]}+~#-_.:,;<>|\\'
}


def generate_pass(length=21):
    """Function to generate a password"""
    password = []
    while len(password) < length:
        key = choice(char_set.keys())
        a_char = urandom(1)
        if a_char in char_set[key]:
            if check_prev_char(password, char_set[key]):
                continue
            else:
                password.append(a_char)
    return ''.join(password)


def check_prev_char(password, current_char_set):
    """Function to ensure that there are no consecutive 
    UPPERCASE/lowercase/numbers/special-characters."""
    index = len(password)
    if index == 0:
        return False
    else:
        prev_char = password[index - 1]
        if prev_char in current_char_set:
            return True
        else:
            return False


class Manager:
    """
    负责调配File_Manager与Search_Engine
    """
    def __init__(self):
        self.f_m = File_Manager()
        self.s_e = Search_Engine()
        
        self.file_path = "data/Info.dat"
        self.confg_path = 'data/Confg.dat'
        self.category ,self.data,self.confg = self.f_m.read_init(self.file_path,self.confg_path)  #data中储存所有的账户信息


    def most_recent(self):
        """
        返回最近使用过的账号的列表
        """
        return self.data


    def search(self, wd, confg):
        def count_similarity(str1,str2):
            """计算相似度，并且返回"""
            gauge = 100/len(str1)
            hits = 0
            score = 0
            digit_num = range(len(str1))
            digit_num.reverse()
            for j in digit_num:
                full_hits = len(str1)-j
                for k in range(len(str1)-j):
                    if str[k:k+j+1] in str2:
                        hits +=1
                if hits != 0:
                    score = 100 - gauge*(full_hits-1) - gauge/full_hits * (full_hits - hits)
                    break
            return score
        
        result = {}
        num = 1
        if confg=='name':  #按照文件名搜索
            similarity = {}
            #计算各项相似度
            for key in self.data.keys():
                similarity[key] = count_similarity(key)
            #排序选出前二十名
            scores = similarity.values()
            scores.sort()
            scores.reverse()
            if len(scores)>20 :
                scores = scores[:20]
            scores = {}.fromkeys(scores).keys()    #去除重复
            scores.sort()   #由于去除重复之后会变序，所以重排序
            #返回字典
            for score in scores:
                for k, s in similarity:
                    if s == score:
                        info = self.data[k]
                        intro = self.grasp_intro(k)
                        result[num] = [k, intro , s, info[1]]
                        num +=1
            return result
        elif confg=='content':  #按照内容搜索
            similarity = {}
            #计算各项相似度
            for key,info in  self.data:
                similarity[key]  = count_similarity(info[0])
            #排序选出前二十名
            scores = similarity.values()
            scores.sort()
            scores.reverse()
            if len(scores)>20 :
                scores = scores[:20]
            scores = {}.fromkeys(scores).keys()    #去除重复
            scores.sort()   #由于去除重复之后会变序，所以重排序
            #返回字典
            for score in scores:
                for k, s in similarity:
                    if s == score:
                        info = self.data[k]
                        intro = self.grasp_intro(k)
                        result[num] = [k, intro, s, info[1]]   #[文件名，简介，相似度+'%'，创建时间]
                        num +=1
            return result


    def grasp_intro(self, key):
        str = ''
        #1.分析出各种基本信息
        info = self.button_info[key]
        #2.从基本信息分析出账户名，邮箱信息，如果找不到，那么返回他的前五个字
        for a in Accout_name_kw:
            if a in info:
                str += a+ info[a]+ '  '
                break
        for e in Email_name_kw:
            if e in info:
                str += e + info[e]
                break
        if  not str:
            str = self.data[key][0:10]
        return str


    def get_button_info(self, str):
        """
        param:  str: 文件名
        value:  分析数据然后拆分出密码，账户，等其他信息
        """
        button_info = {}
        info = self.data[str]
        text = info[0]
        #1：寻找"："
        lines = text.split('\n')
        for line in lines:
            if ':' in line:
                title, content = line.split(':')
                button_info[title] = content
            elif u'：' in line:
                title, content = line.split(':')
                button_info[title] = content
        return button_info


    def save_file(self):
        self.f_m.save_all((self.category,self.data),self.file_path, self.confg, self.confg_path)

        
    def get_account(self,key):
        """根据key返回相应的账户信息"""
        return self.data[key][:]


    def generate_password(self, length= 21):
        def strong_pass(length=21):
            return generate_pass(length)

        def easy_pass(self):
            p = self.confg['password_easy']
            num = int(p[0])
            length = len(p)-1
            if num == length:
                num = 1
            else:
                num +=1
            password = p[num]
            p[0] = str(num)                    
            return password

        if self.config['info']['password_property'] == 'strong':
            return generata_pass(length)
        else:
            return easy_pass(self) 


    def generate_name(self):
        """返回合成的用户名"""
        name = self.confg['name'][:]
        num = int(name[-3:])
        num +=1
        name = name[:-3] + num
        self.confg['name'] = name[:]
        return name

    
    def generate_email(self):
        """返回邮箱"""
        e = self.confg['email_address']
        num = int(e[0])
        length = len(e)-1
        if num == length:
            num = 1
        else:
            num +=1
        email = e[num]
        e[0] = str(num)
                    
        return email


    def save_edition(self, title, content, time):
        if title in  self.data:
            self.data[title] = (content,time)
        else:
            self.data[title] = (content, time)
            self.category['normal'].append(title)


    def add_folder(self,folder_path):
        info = self.f_m.add_folder(folder_path)
        
        for key ,item in info:
            if type(info[key]) is list:
                if key not in self.data:
                    self.category['normal'].append(key)
                    self.data[key] = info[key]
                else:
                    self.data[key] = info[key]
            else:
                if key in self.category:
                    for key2,item2 in info[key]:
                        self.category[key].append(key2)
                        self.data[key2] = item2
                else:
                    self.category[key] = {}
                    for key2 , in item2 in info[key]:
                        self.category[key].append(key2)
                        self.data[key2] = item2

                        
    def add_file(self,file_path):
      """
      """
      #1.分离出门户名(去除了文件的后缀名)
      filename = os.path.base(file_path)
      if '.' in filename:
          suffix = filename.split('.')[-1]
          length = len(suffix)+1
          filename = filename[:-length]
      #2.读入文件
      data = self.f_m.read_file(file_path)
      #3.写入数据库
      if filename not in self.data:
          self.category['normal'].append(filename)
          self.data[filename] = data
      else:
          self.data[filename] = data
        

class File_Manager:
    """
    负责文件的读/写:
    """
    def read_init(self, file_path, confg_path):
        file = self.read_file(file_path)
        confg = self.read_confg(confg_path)
        return (file[0], file[1],confg)
    
    def save_all(self,file, file_path, confg, confg_path):
        self.save_file(file, file_path)
        self.save_confg(confg, confg_path)

    def read_file(self,path):
        """初始化读入所有的信息"""
        #1.读取原始加密数据
        f = open(path, 'r')
        raw_data = f.read() 
        f.close()
        #2.解密数据
        raw_data = self.decrypt(raw_data)
        #3.处理数据并返回
        data = self.dismantle_data(raw_data)
        return data

    def save_file(self,dt,path):
        """在程序的最后保存数据"""
        #1.组装为初始数据
        category , data = dt
        raw_data = self.dismantle(category, data)
        #2.加密初始数据
        raw_data = self.encrypt(raw_data)
        #3.向文件中写入加密数据
        f = open(path,'w')
        f.write(raw_data)
        f.close()

    def read_confg(self, path):
        """读取软件设置，返回字典"""
        cf = ConfigParser.ConfigParser()
        cf.read(path)
        status = {}
        s = cf.sections()
        for section in s:
            tmp = {}
            o = cf.options(section)
            for option in o :
                tmp[option] = cf.get(section, option)
            status[section] = tmp
        return status

    def save_confg(self,confg, confg_path):
        """保存软件设置"""
        cf = ConfigParser.ConfigParser()
        cf.read(confg_path)
        for section in confg.keys():
            for option in confg[section].keys():
                cf.set(section, option, confg[section][option])
        cf.write(open(confg_path, "w"))    

    def encrypt(self, content):
        """加密字符串"""
	EncryptedData = base64.encodestring(content)
	before = char_set['small']+char_set['big']+char_set['nums']
	after = char_set['big']+char_set['small']+'9876543210'
	table = maketrans(before, after)
	EncryptedData.translate(table)
        return  EncryptedData

    def decrypt(self, content):
        """解密字符串"""
        DecryptedData = content
	before = char_set['big']+char_set['small']+'9876543210'
	after = char_set['small']+char_set['big']+char_set['nums']
	table = maketrans(before, after)
	DecryptedData.translate(table)
	DecryptedData = base64.decodestring(DecryptedData)
        return DecryptedData

    def dismantle_data(self, data):
        """拆解raw_data为字典数据"""
        def split_chomp(str):
            """拆分并去掉行末换行符"""
            sr = {}
            for s in str.split('#!#')[1:]:
                if s.endswith('\n'):
                    s = s[:-2]
                s = s.split('|')
                sr[s[0]] = s[1:]
            return sr
        
        category,data = data.split("@@@\n")
        return (split_chomp(category), split_chomp(data))
        
    def assemble_data(self, category, data):
        """组装数据"""
        def joins(str):    
            str1 = []
            for key,value in category:
                tmp = [key].extend(value)
                str1.append('|'.join(tmp))
            str2 = '\n#!#'.join(str)
            str2 = '#!#' + str2 + '\n'
            return str2
        #1.处理category
        c_str = joins(category)
        #2.处理data
        d_str = joins(data)
        
        return '@@@'.join(c_str, d_str)

    def add_folder(self, path):
        """
        添加path路径中所有的账号，返回一个字典
        规则：如果出现文件夹，则单独记录到一个类别中，一层文件夹下的所有账号密码都记录在
        同一个类别
        """
        def search_sub_folder(dic,path):        
            files = os.listdir(path)
            for file in files:
                if os.isfile(file):
                    f = open(path.os.sep+file, r)
                    content = f.read()
                    time = time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
                    dic[file] = [content, time]
                else:
                    search_folder(dic,path+os.sep+file)
    
        data = {}
        #1.扫描到path中所有文件/文件夹的名称，添加到列表
        files = os.listdir(path)
        #2.逐个读取文件，文件夹，按照规则添加到数据文件中
        for file in files:
            if os.isfile(file):
                f = open(path+os.sep+file,r)
                content = f.read()
                time = time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
                data[file] = [content, time]
            else:
                #假如是文件夹
                data[file] = {}
                search_sub_folder(data[file],path+os.sep+fil)
        return data


    def add_file(self,file_path):
        """添加账号到数据库中"""
        f= open(file_path,'r')
        data = f.read()
        f.close()
        time = time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
        return (data, time)



    
class Search_Engine:
    """
    负责搜索动作
    """
    def __init__(self):
        """
        需要从data中读入所有的信息，做成一个特殊的词典,索引为ID号码，值为一个列表，列表 为【文件名，内容】
        """
        pass


    def query(str,confg):
        """
        param:
            str 需要搜的字符串
            confg 搜索的配置，有两种情况：content/name  (表示搜索标题或内容)
        return :
            一个列表，包含拍好顺序的ID号码
        """
        pass

