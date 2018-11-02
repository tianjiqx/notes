
## SQL重写技巧


- 分页：
  - 例子： select \* from t1 where c2=100  limit 100000,100;改写利用索引,建立索引index(c2,c1)，select t1.\* form t1 A,(select c1 from t1 where c2=100 limit 100000,100) B where A.c1=B.c1; 

  
- having：
  - ；例子：select \* from t1 group by c1,c2,c3 having c1 <10 and c2 <10 and c3<10 and c4<10 ,将having上group by列的条件下推，select \* from t1 where c1 <10 and c2 <10 and c3<10 group by c1,c2,c3 having c4<10;



