---
sort: 2
---
# 配置项描述

<a id="baseconfig"></a>
## 基本配置项
不管部署到什么平台，都先要正确配置config.py，这一节描述几个简单的配置项，其他配置项在下面章节详细描述。    

| 配置项              |    含义                                                  |
| ------------------- | -------------------------------------------------------- |
| APP_ID              | 应用标识符，gae平台为应用ID，其他平台用于标识数据库等资源    |
| APP_DOMAIN          | 应用部署后的域名                                          |
| KE_TEMP_DIR         | 制作电子书时的临时目录，为空则使用内存保存临时文件           |
| EBOOK_SAVE_DIR      | 如果需要在线阅读功能，配置此目录用于保存电子书              |
| DOWNLOAD_THREAD_NUM | 下载网页的线程数量，需要目标平台支持多线程，最大值为5        |
| ALLOW_SIGNUP        | 是否允许用户注册，"yes"-用户可以自主注册（可以通过邀请码限制），"no"- 只有管理员能创建其他账号。|
| SECRET_KEY          | 浏览器session的加密密钥，建议修改，任意字符串即可           |
| ADMIN_NAME          | 管理员的账号名                                            |
| POCKET_CONSUMER_KEY | 用于稍后阅读服务Pocket，可以用你自己的Key或就直接使用这个    |
| HIDE_MAIL_TO_LOCAL  | 是否允许将生成的邮件保存到本地，用于调试或测试目的           |




<a id="database"></a>
## 数据库选择
数据库用于保存应用的配置数据和订阅数据。    
得益于SQL数据库ORM库 [peewee](https://pypi.org/project/peewee/) 和作者因KindleEar需要而创建的NoSQL数据库ODM库 [weedata](https://github.com/cdhigh/weedata)，KindleEar支持很多数据库类型，包括：datastore, sqlite, mysql, postgresql, cockroachdb, mongodb, redis, pickle， 基本兼容了市面上的主流数据库，更适合全平台部署，平台支持什么数据库就可以使用什么数据库。    
如果目标平台同时支持SQL/NoSQL，则建议NoSQL，其最大的优点是万一以后升级需要修改数据库结构，则NoSQL不会影响原有数据，而SQL会删掉原数据。    
本应用的数据量不大，确切的来说，很小很小，一般就几十行数据，选择什么数据库都不会对资源消耗和性能造成什么影响，即使最简单的就用一个文本文件当做数据库使用可能都会比其他正规的数据库要快。    



### Datastore
Datastore为google的NoSQL数据库，我们要使用的是firebase的datastore模式。    
如果要部署到google cloud，基本上你只能选择datastore，因为它有免费额度。    
要使用datastore，参数配置如下：
```python
DATABASE_URL = 'datastore'
```



### SQLite
单文件数据库。适用于有本地文件系统读写权限的平台，特别是资源受限系统比如树莓派和各种派之类的。    
数据库文件的路径支持绝对路径和相对路径，相对路径的基目录为项目目录。  
要使用datastore，参数配置如下：
```python
#template:
DATABASE_URL = 'sqlite:////path/to/database.db'
#examples:
DATABASE_URL = 'sqlite:////C:/Users/name/kindleear/site.db'
DATABASE_URL = 'sqlite:////home/username/dbfilename.db'
DATABASE_URL = 'sqlite:///dbfilename.db'  #relative path
```



### MySQL/PostgreSQL/CockroachDB
典型企业级SQL数据库。大炮打蚊子，如果平台支持，直接使用也无妨。    
参数配置如下：
```python
#template:
DATABASE_URL = 'mysql://username:password@hostname:port/database_name'
DATABASE_URL = 'postgresql://username:password@hostname:port/database_name'

#examples:
DATABASE_URL = 'mysql://root:password@localhost:3306/mydatabase'
DATABASE_URL = 'mysql://user:pass123@example.com:3306/mydatabase'
DATABASE_URL = 'postgresql://postgres:password@localhost:5432/mydatabase'
DATABASE_URL = 'postgresql://user:pass123@example.com:5432/mydatabase'

import os
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
database_url = f"mysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
```



### MongoDB
应用最广的典型NoSQL数据库。      
1. 参数配置如下：
```python
#template:
DATABASE_URL = 'mongodb://username:password@hostname:port/'
#examples:
DATABASE_URL = 'mongodb://127.0.0.1:27017/'
DATABASE_URL = 'mongodb://user:pass123@example.com:27017/'
```

2. 如果部署的目标平台没有安装mongodb-server，可以参考 [官方文档](https://www.mongodb.com/docs/manual/installation/) 进行安装。   
这里是在ubuntu的安装方法：
```bash
sudo apt install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```


### Redis
可以持久化到磁盘的NoSQL内存数据库。如果目标系统已经安装并使用了redis用于任务队列，则直接使用redis可以省去安装其他数据库的资源消耗，但使用前要做好相关的redis持久化配置，避免丢失数据。     
1. 参数配置如下(db_number可以省略，如果是0，建议省略)：    
```python
DATABASE_URL = 'redis://[:password]@hostname:port/db_number'
DATABASE_URL = 'redis://127.0.0.1:6379/'
DATABASE_URL = 'redis://:password123@example.com:6379/1'
```

2. 如果不是的目标平台没有安装redis，可以参考 [官方文档]() 进行安装。  
这里是在ubuntu的安装方法：   
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```


### Pickle
作者使用Python的pickle数据持久化标准库创建的一个非常简单的单文件NoSQL"数据库"，可以用于资源特别受限的系统或用于测试目的。   
数据库文件的路径支持绝对路径和相对路径，相对路径的基目录为项目目录。  
参数配置如下：  
```python
#template:
DATABASE_URL = 'pickle:////path/to/database.db'
#examples:
DATABASE_URL = 'pickle:////C:/Users/name/kindleear/site.db'
DATABASE_URL = 'pickle:////home/username/dbfilename.db'
DATABASE_URL = 'pickle:///dbfilename.db'  #relative path
```



<a id="taskqueue"></a>
## 任务队列和定时任务选择
任务队列用于异步执行抓取网页内容、制作电子书、发送邮件等耗时任务。     
定时任务用于定时检查是否需要推送、清零过期推送记录等事项。     

### gae
如果要部署到google cloud，你只能选择gae。
```python
TASK_QUEUE_SERVICE = "gae"
TASK_QUEUE_BROKER_URL = ""
```



### apscheduler
比较轻量，最简配置可以不依赖redis和其他数据库，直接使用内存保存任务状态，只是有一定的丢失任务风险，在任务队列执行过程中掉电重新上电后原任务不会重新运行，只能等新的任务时间到达。     
如果要使用数据库持久化，支持sqlite/mysql/postgresql/mongodb/redis，可以配置为DATABASE_URL相同的值。
```python
TASK_QUEUE_SERVICE = "apscheduler"

TASK_QUEUE_BROKER_URL = "memory" #use memory store
#or
TASK_QUEUE_BROKER_URL = "redis://127.0.0.1:6379/"
#or
TASK_QUEUE_BROKER_URL = "sqlite:////home/username/dbfilename.db"
```

注意事项：
1. apscheduler 3.x不支持多进程（不管使用什么jobstore），配合 gunicorn 使用时需要使用多线程，比如设置 workers=1, threads=3，并且 preload_app=False。   




### celery
最著名的任务队列，支持多种后端技术，包括redis、mongodb、sql、共享目录等，如果要使用数据库保存任务状态，可以配置为DATABASE_URL相同的值。
```python
TASK_QUEUE_SERVICE = "celery"

TASK_QUEUE_BROKER_URL = "redis://127.0.0.1:6379/"
#or
TASK_QUEUE_BROKER_URL = "sqlite:////home/username/dbfilename.db"
#or
TASK_QUEUE_BROKER_URL = "file:///var/celery/results/" #results is a directory
TASK_QUEUE_BROKER_URL = "file:////?/C:/Users/name/results/" #keep the prefix 'file:////?/' if in windows
```



### rq
比celery稍轻量的任务队列，依赖redis，需要额外安装redis服务。    
```python
TASK_QUEUE_SERVICE = "celery"
TASK_QUEUE_BROKER_URL = "redis://127.0.0.1:6379/"
```



<a id="sendmail"></a>
## 邮件发送服务选择
为了更方便使用和规避一些免费额度的限制，邮件发送服务可以等部署完成后在网页上配置。    
* **gae**:
部署到google cloud时建议使用，额度足够，邮件大小也慷慨，单邮件最大31.5MB。     

* **sendgrid**:
部署到其他平台时建议使用，需要额外 [注册账号](https://sendgrid.com/) 并申请一个ApiKey，单邮件最大30MB。 
注：我一直无法正常注册sendgrid，不管换多少种方法多少个邮件地址都无法正常登录sendgrid，所以此功能我没有亲自测试，测试通过的朋友可以告知我。    

* **mailjet**:
[Mailjet](https://www.mailjet.com/)是另一个选项， 需要注册账号并且申请ApiKey和SecretKey，单邮件最大15MB。记得发送前确认自己的发件地址有没有在 [Sender addresses](https://app.mailjet.com/account/sender) 里面。     
测试过程中还发现一个问题，如果你的发件人邮件地址不是你注册mailjet的地址，则mailjet不会报错，只是对方永远收不到。所以如果使用mailjet发送邮件失败，请确认发件地址是否正确。    

* **SMTP**:
这个选项就灵活了，大部分的电子邮件服务平台都支持SMTP，只是很多平台对SMTP登录都有诸多限制，使用前请注意阅读相关说明，特别是大多数平台的SMTP密码都和正常的账号密码不一致。   
除了使用市场上已有的服务外，ubuntu等平台也很方便的使用postfix等部署一个自己的SMTP服务。   




<a id="wsgi"></a>
## WSGI协议容器
KindleEar使用Flask框架实现Web界面管理，入口点在 main.app （main.py文件内的app实例对象），
可以使用任何支持wsgi标准接口的Web服务器软件启动此app即可。    
要求不高的，使用Flask的调试服务器直接启动都可以。    
如果部署到google cloud，默认使用 Gunicorn，也可以任意切换为 uWSGI, Tornado, mod_wsgi 等。    
其他目标平台也是一样的做法，选择已有的或自己喜欢的就行。  



<a id="pip"></a>
## requirements.txt
KindleEar使用requirements.txt管理各种库的依赖，在各种平台部署时都可以一行命令就完成应用的环境配置
```bash
pip install -r requirments.txt
```
因各种配置组合较多，要手动配置requirements.txt比较复杂，容易出错。    
为此，作者提供了一个脚本文件tools/update_req.py，
配置好config.py后，直接执行此文件就可以生成requirements.txt。    
或者你可以不用此脚本，而是将requirements.txt里面的所有注释都删除，也就是安装全部依赖库，反正也占用不了多少空间。


