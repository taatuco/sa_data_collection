# This file return the access information to connect to database

class sa_db_access:

    def username(self):
        sa_usr = "__db_user_name__"
        return sa_usr

    def password(self):
        sa_pwd = "__mysql_user_password__"
        return sa_pwd

    def db_name(self):
        sa_db_name = "smartalpha"
        return sa_db_name

    def db_server(self):
        sa_srv = "localhost"
        return sa_srv

    def smtp_username(self):
        smtp_usr = '__smtp_user_name__'
        return smtp_usr

    def smtp_password(self):
        smtp_pwd = '__smtp_password__'
        return smtp_pwd

    def smtp_server(self):
        smtp_srv = 'localhost'
        return smtp_srv

    def smtp_port(self):
        smtp_port = 587
        return smtp_port
