#coding=utf-8

# 程序说明：
# sav文件合并器
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
print "  使用说明：\n  功能：合并指定目录下的所有sav文件到一个结果文件中。\n  命令格式：python programName.py filekDirectory"

print "开始合并..."
error=False

#记录当前时间
curTime=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
print curTime

if len(sys.argv) < 2:
    print "ERROR,未指定待合并的sav文件目录！"
    error=True



#元信息数组
#多v1-v7：分v1-v7：自评v1-v7

meta={}
meta['more']={}
meta['branch']={}
meta['self']={}


#数据

data={}
data['more']={}
data['branch']={}
data['self']={}


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



#定义函数：保持数据
def storeData(data,meta,dirname):
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
        if len(fnum)>0:
            fnum=int(fnum[len(fnum)-1]) 
        else:
            return
        #print "fnum:",fnum
        
        #处理sav文件
        if fn.endswith("sav"):
            
            #打开文件
            if data.has_key(fnum):
                #合并数据(由于没有重复数据，直接追加，无需去重)
                with SavReader(fn, returnHeader=False) as reader: # 不带行头
                    r=reader.all()
                    #recode(r,srcCode,'utf-8')
                    #去重
                    r=deDup(r)
                    data[fnum].append(r)

            else:
                #保存元数据和数据
                with SavHeaderReader(fn) as header:
                    mt=header.dataDictionary()
                    meta[fnum]=mt
                #添加数据
                with SavReader(fn, returnHeader=True) as reader: # 带行头
                    r=reader.all()
                    #recode(r,srcCode,'utf-8')
                    #去重
                    r=deDup(r)
                    data[fnum]=r
 
    
# 定义函数：join操作，合并两个文件，模拟merge join
# 注意不能和空表join,忽略空表
# return A|B(-id列)
def joinSavById(A,B):

    if not A or len(A)==0:
        return B
    elif not B or len(B)==0:
        return A

    #print 'a',A
    #print 'b',B
    sa=sorted(A[1:],key=lambda row:row[0]) #按每行的第一个元素(id)排序
    sb=sorted(B[1:],key=lambda row:row[0]) #按每行的第一个元素(id)排序
    
    #补空(去除id列)
    ea=[ None for n in range(len(A[0])-1)]
    eb=[ None for n in range(len(B[0])-1)]
    #print ea
    #print eb
    result=[]
    result.append([])
    result[0].extend(A[0])
    result[0].extend(B[0][1:])

    i=0
    j=0
    #正常合并行数
    count=0
    while i < len(sa) and j < len(sb):
        l=[]
        eq=False
        #fl=False
        #if sa[i][0]==330020 or sb[j][0]==330020:
        #    print 'a:',sa[i]
        #    print 'b:',sb[j]
        #    fl=True
        if sa[i][0]==sb[j][0]:
            print 'key eq:',sa[i][0],' ',sb[j][0]
            l.extend(sa[i])
            l.extend(sb[j][1:])

            # merge join
            #li=i
            #lj=j
            #while li < len(sa):
            #    lj=j
            #    while lj <len(sb):
            #        if sa[li][0]==sb[lj][0]:
            #            l=[]
            #            print 'key eq:',sa[li][0],' ',sb[lj][0]
            #            l.extend(sa[li])
            #            l.extend(sb[lj][1:])
            #            count+=1
            #            result.append(l)
            #        else:
            #            break
            #        lj+=1
            #    li+=1
            #    if li <len(sa) and sa[li][0]!=sb[j]:
            #        break
            #i=li
            #j=lj

            i+=1
            j+=1
            count+=1
        elif sa[i][0]<sb[j][0]:
            print 'key lt:',sa[i][0],' ',sb[j][0]
            l.extend(sa[i])
            l.extend(eb)
            i+=1
        else:
            print 'key gt:',sa[i][0],' ',sb[j][0]
            l.append(sb[j][0])
            l.extend(ea)
            l.extend(sb[j][1:])
            j+=1
        if len(l)+1!=len(ea)+len(eb)+2:
            print "exception!,row length error"
            print 'row l:',l
            error=True
        #if fl:    
        #   print l 
        #if not eq:
        #
        result.append(l)

    #补上右边
    while i<len(sa):
        l=[]
        l.extend(sa[i])
        l.extend(eb)
        i+=1
        result.append(l)
    #补上左边
    while j<len(sb):
        l=[]
        l.append(sb[j][0])
        l.extend(ea)
        l.extend(sb[j][1:])
        j+=1
        result.append(l)

    print "A len:",len(A)
    print "B len:",len(B)
    print "merge stat:"
    print "\tid equal line number:",count
    print "\tresult len:",len(result)
    print "\tnormal result line numuber range:",max(len(A),len(B)),'-',(len(A)+len(B)-1)
    #print "\tnormal result line numuber range:",max(len(A),len(B)),'-',(len(A)-1)*(len(B)-1)+1

    
    #检查merge结果正确性
    if len(result) < max(len(A),len(B)) \
        or len(result) >(len(A)+len(B)-1) \
        or len(result)+count+1 != len(A)+len(B):
        error=True
        print "\tERROR,join两个sav文件结果集行数不对！"
    else:
        print "\t合并正确！"
    #for line in result:
    #    print line
    return result

#合并一个大模块(如多中心、分中心，自评)
def mergeOneModule(data,mdname):
    keys=data[mdname].keys()
    print "合并",mdname,"的共",len(keys),"个sav数据文件"
    keys.sort()
    if len(keys)==0:
        return None
    result=data[mdname][keys[0]]
    for key in keys[1:]:
        result=joinSavById(result,data[mdname][key])   
    return result

# 合并所有的sav文件
def mergeALL(data):
    print "合并各子模块的文件"
    # 合并多中心
    md=mergeOneModule(data,"more")
    # 合并分中心
    bd=mergeOneModule(data,"branch")
    # 合并自评
    sd=mergeOneModule(data,"self")

    print "模块间合并"
    #合并多|分
    result=joinSavById(md,bd)
    result=joinSavById(result,sd)

    print "最终合并完的行数:",len(result)
    return result
    

# 根据id删除元信息
def delMetaById(meta):
    #获取id key
    result=copy.deepcopy(meta)

    keys=meta.keys()
    delId=meta['varNames'][0]
    for key in keys:
        d=result[key]
        if type(d)==dict:
            if d.has_key(delId):
                dv=d.pop(delId)
                print "delete key:",delId,"value:",dv
        elif type(d)==list:
            d.remove(delId)
            print "remove key",delId
        else:
            pass
    return result

#合并两个文件的元信息
def mergeFileMeta(MA,MetaB):
   

    if not MA:
        return MetaB
    if not MetaB:
        return MA


    keys=MA.keys()
    result=copy.deepcopy(MA)  #深拷贝
    MB=delMetaById(MetaB) # 移除id项元信息

    for key in keys:
        #print "key:",key
        d=MB[key]
        if type(d)==dict:
            #遍历字典，并合并
            for k in d:
                if not result[key].has_key(k):
                    result[key][k]=d[k]
        elif type(d)==list:
            #合并list
            result[key].extend(d)
        elif type(d)==str:
            if d !='' and not d:
                result[key]=d
        else:
            print "ERROR,非法的数据类型!",type(d),"value:",d
    print "meta merge stat:"
    print "\tMA var num:",len(MA['varNames'])
    print "\tMB var num:",len(MB['varNames'])
    print "\tresult var num:",len(result['varNames'])
    if len(MA['varNames'])+len(MB['varNames']) != len(result['varNames']):
        print "\tERROR,合并元信息结果不对"
        error=True
    else:
        print '\t合并元信息成功'

    #print 'need delete:',MetaB['varNames'][0]

    return result

#合并一个大模块内的元信息
def mergeOneModuleMeta(meta,mdname):
    keys=meta[mdname].keys()
    keys.sort()
    if len(keys)==0:
        return None
    #print "meta len",len(keys)
    #print "keys:",keys
    result=meta[mdname][keys[0]]
    for key in keys[1:]:
        result=mergeFileMeta(result,meta[mdname][key])   
    return result

# 合并所有元信息
def mergeAllMeta(meta):
    print "合并元信息"
    mm=mergeOneModuleMeta(meta,"more")
    bm=mergeOneModuleMeta(meta,"branch")
    sm=mergeOneModuleMeta(meta,"self")

    result=mergeFileMeta(mm,bm)
    result=mergeFileMeta(result,sm)

    print "元信息合并完成"
    print "共有变量:",len(result['varNames'])
    return result



############################


def dateFormat(l,idxs):
    for idx in idxs:
        tmp=l[idx]
        #print tmp
        if tmp  is None:
            pass
        else:
            #tmp=tmp.split('-')
            #tmp=tmp[1]+'/'+tmp[2]+'/'+tmp[0]
            #tmp=tmp[1]+'-'+tmp[2]+'-'+tmp[0]
            #tmp=tmp[2]+'-'+tmp[1]+'-'+tmp[0]
            tmp= writer.spssDateTime(tmp, '%Y-%m-%d')
            l[idx]=tmp
            #print l[idx]
    
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
    #fileDir=unicode(fileDir,'utf-8')
    outFileName=fileDir+"_merge_result_"+curTime+".sav"
    # 切换到实际的目录 
    fileDir=os.getcwd()+"/"+fileDir
    
    
    print "输出文件",outFileName

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
                storeData(data['more'],meta['more'],dn)
            elif '分中心' in dn:
                #处理分中心
                storeData(data['branch'],meta['branch'],dn)
            elif '自评' in dn:
                #处理自评
                storeData(data['self'],meta["self"],dn)

    #合并数据文件，按id进行join操作
    outData=mergeALL(data)
    vndest=outData[0]

    #合并meta文件
    outMeta=mergeAllMeta(meta)
    vnsrc=outMeta['varNames']

    print "src",len(vnsrc),len(set(vnsrc))
    print 'dest',len(vndest),len(set(vndest))
    #vndel=set(vnsrc)-set(vndest)

    #vnd2=set(vndest)-set(vnsrc)
    #print "dest-src",len(vnd2),"\n",vnd2

    #print "dest var len:",len(vndest)
    #print 'src var len:',len(vnsrc)
    print 'src varnames:',vnsrc
    #print 'del len:',len(vndel)
    #print "del varnames:",vndel

    #for line in outData:
    #    print 'data row len:',len(line),' ',
    print '-2line:',len(outData[-2]),outData[-2]
    #print '-1line:',len(outData[-1]),outData[-1]

    # modify ADATE10 -> EDATE
   
    dateCols=[]
    M=outMeta['formats']
    for key in  M:
        if type(M[key])==str and M[key].upper()=='ADATE10':
            #M[key]='EDATE10'
            dateCols.append(key)
    print 'date cols:',dateCols
    dateColIdxs=[]
    for col in dateCols:
        dateColIdxs.append(outMeta['varNames'].index(col))
    print "cols idx:",dateColIdxs

    
    #print 'meta.keys:',outMeta.keys()
    #print 'format:',outMeta['formats']
    
    varIdxs=findVarchar(outData[0],outMeta['formats'])
    

    #outMeta['ioLocale']='zh_CN.GBK'
    outMeta['ioLocale']='zh_CN.UTF-8'
    if error:
        pass
    else:
        # 保持到本地文件
        #lastline=[]
        tmplines=[]
        with SavWriter(outFileName, **outMeta) as writer:
            for line in outData[1:]:
                line=dateFormat(line,dateColIdxs)
                #print line
                #print 'len',len(line)
                recode(line,'gbk','utf-8')
                #print line
                #if line[0]==330020:
                #    print 'xx:',line
                setEmptyString(varIdxs,line)
                if not checkSame(tmplines,line):
                    writer.writerow(line)
                 
                tmplines.append(line)
                #lastline=line

            #writer.writerows(outData[1:])
    



if not error:
    print "合并完成！"
else:
    print "抱歉，合并失败！请检查错误信息，目录、文件格式或联系作者。"





