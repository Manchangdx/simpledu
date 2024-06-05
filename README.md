# simpledu 在线教育网站代码

## 启动项目

首先启动 MySQL 和 Redis 服务。

**创建数据库**
```bash
mysql -uroot -e 'CREATE SCHEMA simpledu'
```

**设置环境变量**
```bash
export FLASK_DEBUG=1 FLASK_APP=manage.py
```

**创建数据表**
```bash
flask db upgrade
```

**添加数据**
```bash
python3 -m scripts.generate
```

**启动程序**
```bash
gunicorn -c scripts/gunicorn.py manage:app
```
