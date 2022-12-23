## ubuntu16.04 编译安装 python3.9



由于16.04 deadsnakes 源已经不维护，需要手动编译安装python3。

需要openssl 版本是1.1.1 以上，否则按照参考升级环境open ssl版本，并指定在./configure 添加 --with-openssl=/usr/local/openssl

```
apt-get update && \
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev && \
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz && \
tar -xf Python-3.9.0.tgz && \
cd Python-3.9.0 && \
./configure --enable-optimizations && \ 
make -j 12 && \
make altinstall && \
python3.9 --version && \
ln -s /usr/local/bin/python3.9 /usr/local/bin/python3 && \
ln -s /usr/local/bin/python3.9 /usr/local/bin/python && \
ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip3 && \
ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip 
```



```
wget https://www.openssl.org/source/openssl-1.1.1d.tar.gz 
tar -zxf openssl-1.1.1d.tar.gz 
cd openssl-1.1.1d/ 
./config --prefix=/usr/local/openssl  # 指定安装路径
make && sudo make install
```





## REF

- [Ubuntu16.04源码安装Python3.8及Pip3.8](https://www.v2fun.net/200.html)