#coding=utf-8

# 程序说明：
# 检查重复的id文件和内容
#
# 程序环境支持：
# python2.6
# savReaderWriter包
# 
# 作者：tianjiqx
# 时间：2018年12月16日22:22:35
# 联系方式：tianjiqx@126.com



import sys
import os
import tempfile
import time
import re
import copy
#import savReaderWriter as sav
from savReaderWriter import *



print "欢迎使用该脚本！"
print "  使用说明：\n  功能：显示文件中重复id的结果。\n  命令格式：python programName.py filekDirectory"

print "开始检查..."
error=False

#记录当前时间
curTime=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
print curTime

if len(sys.argv) < 2:
    print "ERROR,未指定待检查的sav文件目录！"
    error=True




srcCode='ASCII'
##########################################


# 将list中每个元素重新编码
def recode(l,srccode,descode):
    for i in range(len(l)):
        if type(l[i])==list:
            recode(l[i],srccode,descode)
            pass
        elif type(l[i])==str:
            #print i,' ',l[i]
            l[i]=l[i].decode(srccode).encode(descode)
            pass



#定义函数：处理
def handDir(dirname):
    fns=[]
    for fn in os.listdir(dirname):
        fn=dirname+"/"+fn
        if os.path.isfile(fn):
            fns.append(fn)
    #处理每个文件
    for fn in fns:
        #处理sav文件
        if fn.endswith("sav"):
            #打开文件
                with SavReader(fn, returnHeader=True) as reader: # 带行头
                    r=reader.all()
                    for line in r:
                        recode(line,'gbk','utf-8')
                    #去重
                    r=deDup(r)
                    if showDupResult(r):
                        print '在文件',fn,'中'


# 检查文件内的结果是否存在重复id
def showDupResult(lines):
    if len(lines)>1:
        head=lines[0]

        tmplines=lines[1:]
        tmplines=sorted(tmplines,key=lambda row:row[0])
        last=tmplines[0]        
        fl=False
        for line in tmplines[1:]:
            if line[0]==last[0]:
                fl=True
                print 'same id:',line[0]
                showDiff(last,line,head)
            last=line
        return fl
# find different columns
def showDiff(l1,l2,tys):
    if len(l1)==len(l2):
        for i in range(1,len(l1)):
            if l1[i]!=l2[i]:
                print '\tdiff col [',tys[i],']',l1[i],'|',l2[i]



############################


def dateFormat(l,idxs):
    for idx in idxs:
        tmp=l[idx]
        #print tmp
        if tmp  is None:
            pass
        else:
            tmp= writer.spssDateTime(tmp, '%Y-%m-%d')
            l[idx]=tmp
    
    return line 


# find varchar idxs
def findVarchar(vns,fs):
    i=0
    result=[]
    for it in vns:
        if re.search('A\d+',fs[it]) != None:
            #print fs[it]
            result.append(i)
        i+=1

    return result
#varcahr类型设置为空
def setEmptyString(idxs,line):
    for i in idxs:
        if line[i]==None:
            line[i]=''


#比较2line的内容是否一致
def cmp(l1,l2):
    ret=True
    if len(l1)==len(l2):
        for i in range(len(l1)):
            if l1[i]!=l2[i]:
                ret=False
                break
    else:
        ret=False
    return ret

# 检查line在是否在list中
def checkSame(tmplines,line):
    fl=False
    for l in tmplines:
        if cmp(l,line):
            fl=True
            break;
    return fl

# 去重
def deDup(ls):
    l=[]
    for line in ls:
        if not checkSame(l,line):
            l.append(line)
    return l

############################
if not error:
    fileDir=sys.argv[1]
    # 切换到实际的目录 
    fileDir=os.getcwd()+"/"+fileDir

    #获取目录名（采集人员）
    persons=[]
    for fn in os.listdir(fileDir):
        fn=fileDir+"/"+fn
        #print fn
        if os.path.isdir(fn):
            persons.append(fn)
    #print persons
    #依次各个人的获取数据和元数据
    for p in persons:
        #获取子目录
        subdir=[]
        for dn in os.listdir(p):
            dn=p+'/'+dn
            #print dn
            if os.path.isdir(dn):
                subdir.append(dn)
        for dn in subdir:
           handDir(dn) 



if not error:
    print "检查完成！"
else:
    print "抱歉，检查失败！请检查错误信息，目录、文件格式或联系作者。"





