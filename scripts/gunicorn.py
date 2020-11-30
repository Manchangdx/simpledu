import multiprocessing

# 对应 -b 选项
bind = '127.0.0.1:5000'

# 对应 -w 选项
workers = multiprocessing.cpu_count() * 2 + 1

# 对应 -k 选项
worker_class = 'flask_sockets.worker'
