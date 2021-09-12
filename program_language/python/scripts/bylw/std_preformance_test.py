
#coding:utf-8
import datetime
import time
import commands

#########################################
#配置项
loop=10

#table
table_idx1=[2]
table_idx2=[1,2]
table_idx3=[1,2,3,4]
table_idx4_max=8

#column 
col_name='c2'

dbname='testdb'

ms_ip='182.119.80.58'
ms_port='40880'

mslog='~/oceanbase_1.2.2/log/mergeserver.log'

keywords='STD_TEST::ObSort sort'

cur=datetime.datetime.now()
tt=cur.strftime('%Y%m%d_%H%M%S')
outfile='testdb.time.log.'+tt
of=open(outfile,'w+')

for idx1 in range(len(table_idx1)):
  pre1='t_'+str(table_idx1[idx1])+'_'
  for idx2 in range(len(table_idx2)):
    pre2=pre1+str(table_idx2[idx2])+'_'
    for idx3 in range(len(table_idx3)):
      pre3=pre2+str(table_idx3[idx3])+'_'
      avgts=[]
      for idx4 in range(table_idx4_max):
        table_name=pre3+str(idx4+1)
        sql='select count(*) from ( select c2 from '+table_name+' order by c2);'
        print sql
        #获取当前日期，过滤之前的日志
        #datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #清理ms日志
        cmd1=' >   '+ mslog
        # 执行
        (status,output)=commands.getstatusoutput(""+cmd1+"")
        time.sleep(1)  # watie 1s
        cmd1=" mysql -h"+ms_ip+" -P"+ms_port+" -uadmin -padmin -e  '"+sql+"' " +dbname
        for i in range(loop):
          (status,output)=commands.getstatusoutput(""+cmd1+"")
          time.sleep(1)  # watie 1s
        #计算平均执行时间
        cmd1='grep "'+keywords+'"  '+mslog
        (status,output)=commands.getstatusoutput(""+cmd1+"")
        sum=0
        count=0
        output=output.split('\n')
        for line in output:
          line=line.strip('\n').strip()
          if line =='':
            continue
          #print line
          t=line.split('=')[1]
          sum+=int(t)
          count+=1
        if count !=0:
          avgt=sum/count
        else:
          avgt=0
        avgts.append(avgt)
      #打印时间
      print 'count ',len(avgts)
      tstr=pre3+'x time \n '
      for t in avgts:
        tstr+=str(t)+'\t'
      print tstr
      
      of.write(tstr+"\n")
      of.flush()
of.close()
