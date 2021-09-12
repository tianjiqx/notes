
#coding:utf-8
import datetime
import time
import commands

#########################################
#配置项
loop=10

#table
table_idx1=[2]
table_idx2=[3,4]
table_idx3=[1,2,3,4]
table_idx4_max=[9,7]


sqls=[\
'select count(*) from (select c2,c3 from t_4_1_1_1);',\
'select count(*) from (select c2,c3 from t_4_1_1_2);',\
'select count(*) from (select c2,c3 from t_4_1_1_3);',\
'select count(*) from (select c2,c3 from t_4_1_1_4);',\
'select count(*) from (select c2,c3 from t_4_1_1_5);',\
'select count(*) from (select c2,c3 from t_4_1_1_6);',\
'select count(*) from (select c2,c3 from t_4_1_1_7);',\
'select count(*) from (select c2,c3 from t_4_1_1_8);',\
'select count(*) from (select c2,c3 from t_4_1_1_9);',\
'select count(*) from (select c2,c3 from t_4_1_2_1);',\
'select count(*) from (select c2,c3 from t_4_1_2_2);',\
'select count(*) from (select c2,c3 from t_4_1_2_3);',\
'select count(*) from (select c2,c3 from t_4_1_2_4);',\
'select count(*) from (select c2,c3 from t_4_1_2_5);',\
'select count(*) from (select c2,c3 from t_4_1_2_6);',\
'select count(*) from (select c2,c3 from t_4_1_2_7);',\
'select count(*) from (select c2,c3 from t_4_1_2_8);',\
'select count(*) from (select c2,c3 from t_4_1_2_9);',\
'select count(*) from (select c2,c3 from t_4_2_1_1);',\
'select count(*) from (select c2,c3 from t_4_2_1_2);',\
'select count(*) from (select c2,c3 from t_4_2_1_3);',\
'select count(*) from (select c2,c3 from t_4_2_1_4);',\
'select count(*) from (select c2,c3 from t_4_2_1_5);',\
'select count(*) from (select c2,c3 from t_4_2_1_6);',\
'select count(*) from (select c2,c3 from t_4_2_1_7);',\
'select count(*) from (select c2,c3 from t_4_2_1_8);',\
'select count(*) from (select c2,c3 from t_4_2_1_9);',\
"select count(*) from (select/*+index(t_4_2_1_1 idx_c2_t_4_2_1_1)*/ c2,c3 from t_4_2_1_1 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_2 idx_c2_t_4_2_1_2)*/ c2,c3 from t_4_2_1_2 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_3 idx_c2_t_4_2_1_3)*/ c2,c3 from t_4_2_1_3 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_4 idx_c2_t_4_2_1_4)*/ c2,c3 from t_4_2_1_4 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_5 idx_c2_t_4_2_1_5)*/ c2,c3 from t_4_2_1_5 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_6 idx_c2_t_4_2_1_6)*/ c2,c3 from t_4_2_1_6 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_7 idx_c2_t_4_2_1_7)*/ c2,c3 from t_4_2_1_7 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_8 idx_c2_t_4_2_1_8)*/ c2,c3 from t_4_2_1_8 where c2 < 'BBCD00000026297');",\
"select count(*) from (select/*+index(t_4_2_1_9 idx_c2_t_4_2_1_9)*/ c2,c3 from t_4_2_1_9 where c2 < 'BBCD00000026297');",\
'select count(*) from (select c2,c3 from t_4_3_1_1);',\
'select count(*) from (select c2,c3 from t_4_3_1_2);',\
'select count(*) from (select c2,c3 from t_4_3_1_3);',\
'select count(*) from (select c2,c3 from t_4_3_1_4);',\
'select count(*) from (select c2,c3 from t_4_3_1_5);',\
'select count(*) from (select c2,c3 from t_4_3_1_6);',\
'select count(*) from (select c2,c3 from t_4_3_2_1);',\
'select count(*) from (select c2,c3 from t_4_3_2_2);',\
'select count(*) from (select c2,c3 from t_4_3_2_3);',\
'select count(*) from (select c2,c3 from t_4_3_2_4);',\
'select count(*) from (select c2,c3 from t_4_3_2_5);',\
'select count(*) from (select c2,c3 from t_4_3_2_6);',\
'select count(*) from (select * from t_4_3_1_1);',\
'select count(*) from (select * from t_4_3_1_2);',\
'select count(*) from (select * from t_4_3_1_3);',\
'select count(*) from (select * from t_4_3_1_4);',\
'select count(*) from (select * from t_4_3_1_5);',\
'select count(*) from (select * from t_4_3_1_6);',\
'select count(*) from (select * from t_4_3_2_1);',\
'select count(*) from (select * from t_4_3_2_2);',\
'select count(*) from (select * from t_4_3_2_3);',\
'select count(*) from (select * from t_4_3_2_4);',\
'select count(*) from (select * from t_4_3_2_5);',\
'select count(*) from (select * from t_4_3_2_6);'\
]

#column 
col_name='c2'

dbname='testdb'

ms_ip='182.119.80.58'
ms_port='40880'

mslog='~/oceanbase_1.2.2/log/mergeserver.log'

keywords='STD_TEST::ObTableRpcScan'

cur=datetime.datetime.now()
tt=cur.strftime('%Y%m%d_%H%M%S')
outfile='testdb.time.log.'+tt
of=open(outfile,'w+')
s=0;
avgts=[]


for ii in range(len(sqls)):
  avgts.append(0)


for ii in range(loop):
  jj=0
  for sql in sqls:
        print sql
        #获取当前日期，过滤之前的日志
        #datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #清理ms日志
        cmd1=' >   '+ mslog
        # 执行
        (status,output)=commands.getstatusoutput(""+cmd1+"")
        time.sleep(1)  # watie 1s
        cmd1=" mysql -h"+ms_ip+" -P"+ms_port+" -uadmin -padmin -e  \""+sql+"\" " +dbname +" -c "
        print cmd1
        #for i in range(loop):
        (status,output)=commands.getstatusoutput(""+cmd1+"")
        time.sleep(1)  # watie 1s
        #计算平均执行时间
        cmd1='grep "'+keywords+'"  '+mslog
        (status,output)=commands.getstatusoutput(""+cmd1+"")
        
        count=0
        output=output.split('\n')
        tmp=[]
        for line in output:
          line=line.strip('\n').strip()
          if line =='':
            continue
          #print line
          t=line.split('=')[1]
          #sum+=int(t)
          tmp.append(int(t))
          count+=1
        tmp.sort(reverse=True)  # desc
        #tmp=tmp[:2*loop]
        #print tmp
        if count !=0:
          tmp=tmp[:2]
          print tmp
          sumtime=sum(tmp)
          avgts[jj] += (sumtime/len(tmp))
        else:
          avgts[jj]+=0
        print 'loop time :',ii
        jj+=1


s=0
tstr=""
for i in range(len(sqls)):
  s+=1
  tstr+=str(avgts[i]/loop)+'\t'
  if s%6==0 or s==len(sqls):
    tstr+='\n'
    
of.write(tstr)
of.flush()
of.close()
