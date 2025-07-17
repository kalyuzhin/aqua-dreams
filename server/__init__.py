import pymysql
pymysql.version_info = (1, 4, 6, "final", 0)
pymysql.install_as_MySQLdb()

# Настройка SSL/TLS для подключения
pymysql.connections.DEFAULT_SSL = {'ssl': {}}
