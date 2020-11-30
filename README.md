# simpledu 在线教育网站代码

# 创建数据库 
mysql -uroot -e 'CREATE SCHEMA simpledu'

# 设置环境变量
export FLASK_DEBUG=1 FLASK_APP=manage.py

# 创建数据表
flask db upgrade

# 添加数据
python3 -m scripts.generate

# 启动程序
gunicorn -c scripts/gunicorn.py manage:app
