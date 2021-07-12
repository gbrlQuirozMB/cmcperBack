import os

name = 'cmcper'
loglevel = 'info'
errorlog = '-'
accesslog = '-'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# #sync
# # workers = 2
# workers = os.cpu_count() * 2 + 1
# worker_class = 'sync'

#async
# pip install gevent
workers = os.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 500