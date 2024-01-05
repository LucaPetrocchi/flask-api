# # from flask import current_app
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# from setti

# def validate_database():
#     SQLALCHEMY_DATABASE_URI = current_app.config.get('SQLALCHEMY_DATABASE_URI')
#     print(SQLALCHEMY_DATABASE_URI)
#     engine = create_engine(SQLALCHEMY_DATABASE_URI)
#     if not database_exists(engine.url):
#         create_database(engine.url)
#         print(f'CREATED DB: {SQLALCHEMY_DATABASE_URI}')
#     else:
#         print(f'DB ALREADY EXISTS')

# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# validate_database()