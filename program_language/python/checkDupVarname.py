#coding:utf-8

# 功能：检查重复变量名


import sys
import os
import tempfile
import time
import re
import copy
from savReaderWriter import *



if len(sys.argv) < 2:
    print "ERROR,未指定待检查的sav文件目录！"
    error=True



meta={}
meta['more']={}
meta['branch']={}
meta['self']={}

error=False


##########################################
#定义函数：保持数据
def storeData(meta,dirname):
    fns=[]
    for fn in os.listdir(dirname):
        fn=dirname+"/"+fn
        #print fn
        if os.path.isfile(fn):
            fns.append(fn)
    #处理每个文件
    for fn in fns:
        
        #获取名称
        fname=fn.split('/')
        fname=fname[len(fname)-1]
        #print "fname:",fname
        #获取名称中的数字
        fnum=re.findall("\d+",fname)
        fnum=int(fnum[len(fnum)-1]) 
        #print "fnum:",fnum
        
        #处理sav文件
        if fn.endswith("sav"):
            
            #打开文件
            if meta.has_key(fnum):
                meta[fnum]['files'].append(fn)
            else:
                #保存元数据
                with SavHeaderReader(fn) as header:
                    mt=header.dataDictionary()
                    meta[fnum]={'files':[fn],'varNames':mt['varNames']}

if not error:

    fileDir=sys.argv[1]


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
            if '多中心' in dn:
                #处理多中心
                storeData(meta['more'],dn)
            elif '分中心' in dn:
                #处理分中心
                storeData(meta['branch'],dn)
            elif '自评' in dn:
                #处理自评
                storeData(meta["self"],dn)


    #合并
    #print meta
    info=[]
    ln=['more','branch','self']
    for i in ln:
        for j in meta[i]:
            info.append(meta[i][j])
    for i in range(len(info)):
        j=i+1
        confic=[]
        #print '与文件[',info[i]['files'],']冲突的文件有：'
        while j<len(info):
            s1=set(info[i]['varNames'])
            s2=set(info[j]['varNames'])
            interset=s1&s2
            if len(interset)>0:
                r="files: "
                for fn in info[j]['files']:
                    r+=fn+','
                r+=' varNames: '
                for var in interset:
                    r+=var+' '
                confic.append(r)
            j+=1

        if len(confic)>0:
            s='与文件 ['
            for fn in info[i]['files']:
                s+=fn+' '
            s+='] 变量名冲突的文件有：'
            print s
            for it in confic:
                print it
