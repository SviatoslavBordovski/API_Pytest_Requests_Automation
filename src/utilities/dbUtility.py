from src.configs.hosts_config import DB_HOST
from src.utilities.credentialsUtility import CredentialsUtility
import os
import pymysql
import logging as logger

class DBUtility(object):

    def __init__(self):
        creds_helper = CredentialsUtility()
        self.creds = creds_helper.get_db_credentials()

        self.machine = os.environ.get('MACHINE')
        assert self.machine, f"Environment variable 'MACHINE' must be set."

        self.wp_host = os.environ.get('WP_HOST')
        assert self.wp_host, f"Environment variable 'WP_HOST' must be set."

        if self.machine == 'docker' and self.wp_host == 'local':
            raise Exception(f"Can not run test in docker if WP_HOST=local")

        self.env = os.environ.get('ENV', 'test')

        self.host = DB_HOST[self.machine][self.env]['host']
        # self.socket = DB_HOST[self.machine][self.env]['socket']
        self.port = DB_HOST[self.machine][self.env]['port']
        self.database = DB_HOST[self.machine][self.env]['database']
        self.table_prefix = DB_HOST[self.machine][self.env]['table_prefix']

    def create_connection(self):
        if self.wp_host == 'localhost':
            connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                         password=self.creds['db_password'], port=self.port)
                                         # unix_socket=self.socket)
        elif self.wp_host == 'ampps':
            connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                         password=self.creds['db_password'],
                                         port=self.port)
        else:
            raise Exception("Unknown WP_HOST.")

        return connection

    def execute_select(self, sql_request):

        conn = self.create_connection()

        try:
            logger.debug(f"Executing sql request: {sql_request}")
            cur = conn.cursor(pymysql.cursors.DictCursor)  # makes each row of table as dictionary
            cur.execute(sql_request)  # execution of actual request
            rs_dict = cur.fetchall()  # fetched all results that were requested/executed
            cur.close()  # closed connection
        except Exception as e:
            raise Exception(f"Failed running sql: {sql_request} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict

    def execute_sql(self, sql):
        pass
