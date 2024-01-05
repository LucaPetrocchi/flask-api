from environs import Env

env = Env()
env.read_env()

SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
# MYSQL_PASSWORD = env.str('MYSQL_PASSWORD')
# MYSQL_USER = env.str('MYSQL_USER')
# MYSQL_DATABASE = env.str('MYSQL_DATABASE')
