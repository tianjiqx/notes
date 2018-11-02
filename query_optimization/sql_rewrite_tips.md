
## SQL重写技巧


- 分页：
  - 例子： select * from t1 where c2=100  limit 100000,100;改写利用索引,建立索引index(c2,c1)，select t1.\* from A.* form t1 A,(select c1 from t1 where c2=100 limit 100000,100) B where A.c1=B.c1; 



