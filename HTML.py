#coding=utf-8
import os
import sys
import re
import collections
import shutil
from os.path import join
import time
from pyh import *
import cPickle as pickle
import config
from platform import system
# from  ExcelAccessor import *
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('log')
RECORD_TITLE = '测试'

class Html:
    def __init__(self, recordFileName):
        #print type(recordFileName)
        self.recordFileName = recordFileName
        timestr = time.strftime('%Y-%m-%d %H:%M')
        self.page = PyH(timestr+RECORD_TITLE)
        self.page << h1(timestr+RECORD_TITLE, align='center')
        self.page.addJS('mode.js')
        self.page.addCSS("http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css")
        self.page.addJS('http://libs.baidu.com/jquery/2.0.0/jquery.min.js')
        self.page.addJS('http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js')
        self.page.addCSS('mode.css')
        self.versionNumber=0
        self.passcase_num, self.failcase_num = 0, 0
        self.r = self.page << div(cl="panel panel-default")
        self.r << div(h2("测试概况", align='left'),cl="panel - heading")
        self.r = self.r << div(cl="panel-body")
        self.t = table(cl="table",body={"width": "80%", "margin": "auto"})
        self.t << tr(td('执行轮数',align="right",width="5%")+td('测试用例组名称',align="left",width="35%")+td('测试总数',align="left",width="10%")+td('成功',align="left",width="10%")+td('失败',align="left",width="10%")+td('执行记录',align="left",width="10%"),id="header_row")
        self.write_page()
        self.page << self.t
        #print type(self.page)

    def write_page(self):
        f = open("cpickle.db", "wb")
        pickle.dump(self.t, f)
        f.close()

    def read_page(self):
        f = open("cpickle.db", "rb")
        self.t = pickle.load(f)

    def add_result(self, resultlist):
        self.r << p("总共执行用例: %d  | 通过:%d  | 失败（测试预期结果不对）: %d" %(resultlist[0]+resultlist[1],resultlist[0],resultlist[1]))
        self.r << p("用例通过率：{:.2f}%".format(float(resultlist[0])/float((resultlist[0]+resultlist[1]))*100))

    def add_table(self, name, passValue, failValue):
        #self.r=self.page << table(caption="chen",border="1",cl="table1",cellpadding="0",cellspacing="0",align='center',width=1200)
        self.i = self.page << table(cl="table table-bordered",body={"width": "80%", "margin": "auto"})
        #self.r << colgroup()
        #self.r<<colgroup(col(align="left",width="50%")+col(align="right",width="10%")+col(align="right",width="10%")+col(align="right",width="10%")+col(align="right",width="10%"))
        if failValue:
            self.i << tr(td("",align="right",width="5%") + td(name,align="left",width="35%") + td(str(passValue+failValue),align="left",width="10%") + td(str(passValue),align="left",width="10%") + td(str(failValue),align="left",width="10%") + td(a("查看详情",href="javascript:void(0)",onclick="showClassDetail(this.parentNode.parentNode)"),align="left",width="10%"),cl="testclass failClass")
        else:
            self.i << tr(td("",align="right",width="5%") + td(name, align="left", width="35%") + td(str(passValue+failValue),align="left",width="10%") + td(str(passValue),align="left",width="10%") + td(str(failValue),align="left",width="10%") + td(a("查看详情",href="javascript:void(0)",onclick="showClassDetail(this.parentNode.parentNode)"),align="left",width="10%"),cl="testclass passClass")

    def add_tr(self, isPass, name, round, row_list):
        self.read_page()
        if isPass == "FAIL":
            self.i << tr(td(round) + td(name, cl="failCase") + td(a("FAIL", cl="popup_link", onfocus="this.blur();", href="javascript:showTestDetail('div_caseRun.%s')" % (name))+div(div(a("[x]",onfocus="this.blur();",onclick="document.getElementById('div_caseRun.%s').style.display = 'none'" %(name)),style="text-align: right; color:red; cursor:pointer;")+p(row_list), id="div_caseRun.%s" %(name), cl='popup_window',style="display: none;")), cl="testcase", id="caseRun.%s" %(name))
        else:
            self.i << tr(td(round) + td(name, cl="passCase") + td(a("PASS", cl="popup_link", onfocus="this.blur();", href="javascript:showTestDetail('div_caseRun.%s')" % (name))+div(div(a("[x]",onfocus="this.blur();",onclick="document.getElementById('div_caseRun.%s').style.display = 'none'" %(name)),style="text-align: right; color:red; cursor:pointer;")+p(row_list), id="div_caseRun.%s" %(name), cl='popup_window',style="display: none;")), cl="testcase", id="caseRun.%s" %(name))
        #self.page << self.r

    def createhtml(self):
        #self.page<<self.t
        print "html path:[%s]" % (self.record_path + self.recordFileName+'.html')
        self.recordFileName = self.recordFileName.decode('gbk').encode('utf-8')+".html" if system() == 'Linux' else self.recordFileName + ".html"
        print self.record_path+self.recordFileName
        self.page.printOut(self.record_path+self.recordFileName)
        self.page = None
        self.page = PyH(RECORD_TITLE)
        self.page << h1(RECORD_TITLE, align='center')

    def timespace(self,start,end):
        day_s=start.split("-")[0]
        time_s=start.split("-")[1]

        day_e=end.split("-")[0]
        time_e=end.split("-")[1]

        #print day_s,time_s,day_e,time_e
        [hour_s, minu_s, sec_s] = time_s.split('_')
        [hour_e, minu_e, sec_e] = time_e.split('_')
        if day_s == day_e:
            spacetime=int(hour_e)*3600+int(minu_e)*60+int(sec_e)-(int(hour_s)*3600+int(minu_s)*60+int(sec_s))
            # print spacetime
        else:
            day_s=day_s.split('-')[-1]
            day_e = day_e.split('-')[-1]
            spacetime = int(hour_e) * 3600 + int(minu_e) * 60 + int(sec_e) + 3600*24 - (int(hour_s) * 3600 + int(minu_s) * 60 + int(sec_s))
        return spacetime

    def parse_entitylog(self,entitylog):

        result = 1 if entitylog.find(":Pass") != -1 else 0
        if result:
            self.passcase_num += 1
        else:
            self.failcase_num += 1
        index = entitylog.find("this case spend")
        index_end = entitylog[index+17:].find('s')
        time = '%.3f' % (float(entitylog[index+17:][:index_end]))
        time = str(float(time)*1000)+"毫秒"
        #print 'time=',time.decode('gbk').encode('utf-8')
        return result, time

    def add_cssjs_to_html(self):
        htmlfile = self.record_path + self.recordFileName
        jsfile = 'mode.js'
        cssfile = 'mode.css'
        csstext = open(cssfile, 'r').read()
        jstext = open(jsfile, 'r').read()
        #print type(jstext)
        #print type(csstext)
        line = True
        #with open(htmlfile, "r", encoding="utf-8") as f1, open("%s.bk" % htmlfile, "w", encoding="utf-8") as f2:
        with open(htmlfile, "r") as f1, open("%s.bak"  % htmlfile, "w") as f2:
            f2.write(r'<meta http-equiv="Content-Type" content="text/html;charset=utf-8">')
            for line in f1.readlines():
                if 'src="mode.js"' in line:
                    line = line.replace('src="mode.js"', '')
                    line = line.replace('type="text/javascript">', 'type="text/javascript">'+jstext)
                    #print line
                elif 'href="mode.css"' in line:
                    line = '<style type="text/css" media="screen">' + csstext + '</style>'
                    #print line
                f2.write(line)
            f1.close()
            f2.close()
            os.remove(htmlfile)
            os.rename("%s.bak" % htmlfile, htmlfile)

    def parse_logfile(self, logcol):
        __FORMAT = '%Y-%m-%d %H:%M:%S'
        casedict = collections.OrderedDict()
        result_dict = {}
        for logfile in logcol:
            print logfile
            round = []
            postmsg, recvmsg = "", ""
            caseflag, postflag, recvflag = 0, 0, 0
            entitydict = None
            symbol = os.sep
            self.record_path = os.path.join(sys.path[0], "log") + symbol
            casemodule = logfile.split(symbol)[-2]
            with open(logfile) as lf:
                for line in lf:
                    if casemodule in casedict:
                        entitydict = casedict[casemodule]
                    else:
                        entitydict = collections.OrderedDict()
                    if "Test Round" in line:
                        round.append(line.strip('\r\n').split(':')[-1])
                    if "post to" in line or "get from" in line:
                        postmsg = line.strip('\r\n').split('- INFO -')[-1]
                        postflag = 1
                    elif "recv :" in line:
                        recvmsg = line.strip('\r\n').split('- INFO -')[-1]
                    elif "DEBUG" in line and postflag == 1:
                        conc = line.strip('\r\n').split("- DEBUG -")[-1]
                        result, casename = tuple(conc.split()[1:3])
                        logdetail = postmsg + '<p>' + recvmsg + '<p>' + conc
                        entitylist = [round[-1], result, logdetail]
                        entitydict[casename + round[-1]] = entitylist
                        casedict[casemodule] = entitydict
            pass_num = 0
            fail_num = 0
            for casename, entitylist in casedict[casemodule].items():
                if entitylist[1] == "PASS":
                    pass_num += 1
                    self.passcase_num += 1
                else:
                    fail_num += 1
                    self.failcase_num += 1
                result = 1 if fail_num == 0 else 0
                result_dict[casemodule] = {"result": result, "info": [pass_num, fail_num]}
        self.add_result([self.passcase_num, self.failcase_num])
        for resultcase, resultitem in result_dict.items():
            if not resultitem["result"]:
                self.add_table(resultcase, resultitem["info"][0], resultitem["info"][1])
                for entitynameitem, entityrstitem in casedict[resultcase].items():
                    if "FAIL" not in entityrstitem:
                        self.add_tr(entityrstitem[1], entitynameitem, entityrstitem[0], entityrstitem[2])
                for entitynameitem, entityrstitem in casedict[resultcase].items():
                    if "FAIL" in entityrstitem:
                        self.add_tr(entityrstitem[1], entitynameitem, entityrstitem[0], entityrstitem[2])
        for resultcase, resultitem in result_dict.items():
            if resultitem["result"]:
                self.add_table(resultcase, resultitem["info"][0], resultitem["info"][1])
                for entitynameitem, entityrstitem in casedict[resultcase].items():
                    self.add_tr(entityrstitem[1], entitynameitem, entityrstitem[0], entityrstitem[2])
        self.createhtml()
        self.add_cssjs_to_html()



    def find_new_file(self, dir):
        file_lists = os.listdir(dir)
        file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn)
                if not os.path.isdir(dir + "\\" + fn) else 0)
        file = os.path.join(dir, file_lists[-1])
        return file


def make_html():
    obj = Html("result")
    loglist = []
    for module in config.test_module:
        logfile = obj.find_new_file(os.path.join(sys.path[0], "log", module))
        loglist.append(logfile)
    obj.parse_logfile(loglist)


if __name__ == "__main__":
    make_html()
