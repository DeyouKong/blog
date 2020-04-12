# -*- coding: utf-8 -*-

# @File: xmindToExcel
# @Author : "Sampson"
# @Detail :


from xmindparser import xmind_to_dict
import re
import xlwt

class xmind_to_xls():
    def xmind_num(self,value):
        """获取xmind标题个数"""
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def xmind_title(self,value):
        """获取xmind标题内容"""
        return value['title']

    def  xmind_cat(self,filename):
        '''调试函数，打印内容用的'''
        self.out = xmind_to_dict(filename)
        self.story = self.out[0]['topic']['topics']
        self.num=len(self.story)
        print(self.out)
        print(self.out[0]['topic']['title'])
        return self.story,self.num

    def write_excel(self,xmind_file,servicename='',editionname='',performer=''):
        '''生成excel文件函数'''
        self.f=xlwt.Workbook()
        self.sheet1 =self.f.add_sheet('sheet1',cell_overwrite_ok=True)
        self.row0 = ["storyid", '需求名称', '测试用例名称', '执行步骤', '预期结果', '服务名称', '版本', '执行人员']
        #生成第一行
        for i in range(0,len(self.row0)):
            self.sheet1.write(0,i,self.row0[i])
        self.out = xmind_to_dict(xmind_file)
        self.xls_name=self.out[0]['topic']['title']
        self.story = self.out[0]['topic']['topics']
        self.storynum = len(self.story)
        j=1 #用例计算器
        z = 0  # 用例结果数计数器
        for i in range(0, self.storynum):
            self.storyname = self.story[i]['title']
            print(self.storyname)
            self.regex_str = ".*[\[【](.+?)[\]】].*"
            self.storyid_reg = re.match(self.regex_str, self.storyname)
            if self.storyid_reg:
                self.storyid=self.storyid_reg.group(1)#正则取出用例编号
                #print(self.storyid_reg.group(1))
            self.testcase_num=self.xmind_num(self.story[i]['topics'][0])
            for k in range(0,self.testcase_num):
                self.testcase=self.story[i]['topics'][0]['topics'][k]
                self.testcase_name =self.xmind_title(self.testcase)
                self.testcase_stepnum=self.xmind_num(self.testcase) #每个用例的步骤数量
                self.sheet1.write(k + i + z + j, 2, self.testcase_name)
                self.sheet1.write(k + i + z + j, 0, self.storyid)
                self.sheet1.write(k + i + z + j, 1, self.storyname)
                self.sheet1.write(k + i + z + j, 5, servicename)
                self.sheet1.write(k + i + z + j, 6, editionname)
                self.sheet1.write(k + i + z + j, 7, performer)
                for x  in range(0,self.testcase_stepnum):
                    self.testcase_step=self.testcase['topics'][x]
                    self.teststep_title=self.xmind_title(self.testcase_step) #用例步骤名称
                    self.teststep_num=self.xmind_num(self.testcase_step) #用例步骤个数
                    if self.teststep_num != 0:
                        for y in range(0,self.teststep_num):
                            self.test_results=self.testcase_step['topics'][y]
                            self.test_result=self.xmind_title(self.test_results)#用例结果
                            self.sheet1.write(k + i + z + j+y+1, 3, self.teststep_title)
                            self.sheet1.write(k + i + z + j + y+1, 4, self.test_result)
                        z = z + y+1
                    else:
                        self.test_result=' '
                        self.sheet1.write(k + i + z + j+1  , 3, self.teststep_title)
                        self.sheet1.write(k + i + z + j+1 , 4, self.test_result)
                        z = z + 1
            j=j+k
        self.f.save(self.xls_name+'.xls') #xls名称取xmind主题名称

if __name__ == '__main__':
     xmind_file = "C:\\Users\\Administrator\\Desktop\\版本测试.xmind"  # xmind文件
     servicename='aa'
     editionname='bb'
     performer='cc'
     #xmind_to_xls().write_excel(xmind_file,servicename,editionname,performer)
     xmind_to_xls().xmind_cat(xmind_file)
