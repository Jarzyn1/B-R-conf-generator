#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from file_generator import FileGenerator
import json
import ssl
import datetime
import urlparse
import SocketServer
import collections
import decimal
import re
#from db_offline import *
from mysql.connector import FieldType

# Dictionary for translating odbc datatype to MpDatabase
# approved types (currenly based on MySql type table)
# Connector for mssql: pyodbc (Microsoft recommended)
# https://github.com/mkleehammer/pyodbc/wiki/Data-Types#python-2
# Connector for MySql: mysql
# https://dev.mysql.com/doc/connectors/en/connector-python-api-fieldtype.html
pyodbc_mysql_datatype_map = {
    bool: (FieldType.BIT),
    str: (FieldType.VAR_STRING),
    datetime.date: (FieldType.DATE),
    datetime.time: (FieldType.TIME),
    datetime.datetime: (FieldType.DATETIME),
    int: (FieldType.TINY),
    long: (FieldType.LONGLONG),
    float: (FieldType.FLOAT),
    unicode: (FieldType.VAR_STRING),
    decimal.Decimal: (FieldType.NEWDECIMAL)
}

# MSSQL Float storage size is specification: https://docs.microsoft.com/en-us/sql/t-sql/data-types/float-and-real-transact-sql?view=sql-server-2017
def specifyFloat(internalSize):
    if 1<=internalSize<=24:
        return FieldType.FLOAT
    else:
        return FieldType.DOUBLE

def makeJsonResponse(status, message, response):
    data = {}
    data['status'] = status
    data['message'] = message
    data['response'] = response
    return json.dumps(data, default=myconverter)

def debug_log(text):
    if len(args.l) > 0:
        try:
            with open(args.l, 'w+') as f:
                f = open(args.l, 'w+')
                f.write(makeJsonResponse(0, "",text))
        except:
            print('Can not log to file "{0}"'.format(args.l))

def debug_print(error, msg):
    print("Exception: code %s, message %s" % (str(error),msg))

def sqlToJson(column_names, dataIn, colTypes):
    types = []
    for desc in colTypes:
        if(args.sqlType == 'mssql'):
            coltype = pyodbc_mysql_datatype_map[desc[1]]
            if coltype == FieldType.FLOAT:
                coltype = specifyFloat(desc[3])
            types.append(FieldType.get_info(coltype))
        else:
            coltype = desc[1]
            types.append(FieldType.get_info(coltype))
    data = []
    for row in dataIn:
        i = 0
        dataRow = collections.OrderedDict()
        for field in row:
            dataRow[column_names[i]] = field
            i = i + 1
        data.append(dataRow)
    response = {}
    response['data'] = data
    response['types'] = types
    return response

def makeTime(o, onlyTime = False):
    value = {}
    try:
        value['year'] = o.year
    except:
        value['year'] = 0
    try:
        value['month'] = o.month
    except:
        value['month'] = 0
    try:
        value['day'] = o.day
    except:
        value['day'] = 0
    try:
        value['wday'] = o.weekday()
    except:
        value['wday'] = 0
    try:
        value['hour'] = o.hour
    except:
        value['hour'] = 0
    try:
        value['minute'] = o.minute
    except:
        value['minute'] = 0
    try:
        value['second'] = o.second
    except:
        value['second'] = 0
    try:
        value['millisecond'] = o.microsecond / 1000
    except:
        value['millisecond'] = 0
    try:
        value['microsecond'] = o.microsecond - value['millisecond']*1000
    except:
        value['microsecond'] = 0
    if onlyTime:
        value['year'] = 0
        value['month'] = 0
        value['wday'] = 0
    return value

def myconverter(o):
    if isinstance(o, datetime.datetime) or isinstance(o, datetime.date) or isinstance(o, datetime.timedelta):
        if isinstance(o, datetime.timedelta):
            if o.days > 0:
                # pass as datetime object, because we have to represent days
                return makeTime((datetime.datetime.min + o) - datetime.timedelta(days=1),True)
            elif o.days == 0:
                return makeTime((datetime.datetime.min + o).time())
            else:
                return makeTime(datetime.datetime.min.time())
        else:
            return makeTime(o)
    elif isinstance(o, decimal.Decimal):
        return float(o)# python's float has double precision

class DB:

    _user = None
    _password = None
    _host = None
    _database = None
    _cnx = None
    _jsonResponse = None
    _query_type = 'modules'
    _fileGenerator = FileGenerator(template_path='templates')

    def connect(self, user, password, host, port, database):
        self._user = user
        self._password = password
        self._host = host
        self._database = database
        self._port = port
        if(args.sqlType == 'mssql'):
            import pyodbc
            server = str(self._host) + ',' + str(self._port)
            self._cnx = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                                       server=server,
                                       database=self._database,
                                       uid=self._user, pwd=self._password)
        else:
            import mysql.connector
            self._cnx = mysql.connector.connect(user=self._user, password=self._password,
                                                host=self._host,
                                                database=self._database,
                                                port=self._port)

    def disconnect(self):
        try:
            self._cnx.close()
            return makeJsonResponse(0, "disconnected", "")
        except Exception as ex:
            debug_print(1, str(ex))
            debug_print(1, 'not connected to sql server')
            return makeJsonResponse(1, "not connected to sql server", "")

    def getData(self):
        return self._jsonResponse

    def query(self, sql):
        try:
            if args.sqlType == 'mssql':
                cursor = self._cnx.cursor()
            else:
                cursor = self._cnx.cursor(buffered=True)
        except Exception as ex:
            debug_print(1, str(ex))
            return makeJsonResponse(1, "not connected to sql server", "")

        begin = re.search('FROM', sql).start()
        end = re.search('WHERE', sql).start()
        table_name = sql[begin + 5:end - 1]
        print('table name: ' + table_name)
        ID_project = re.findall(r'\d+', sql)[-1]

        # change all queries to selecting all module entries from a given project
        sql = "SELECT * FROM Configurations WHERE ID_project = '"+ID_project+"'"
        print('ID_project = '+ID_project)
        for statement in re.sub(r'(\)\s*);', r'\1%;%', sql).split('%;%'):
            print('executing: ' + statement)
            cursor.execute(statement)
        data = []
        response = {}
        # Always try to fetch data independent of insert / select
        try:
            data = cursor.fetchall()
        except Exception as ex:
            pass
        self._cnx.commit()

        data_processed = []

        # First query - returns the list of all necessary module configuration files to automation studio
        if self._query_type == 'modules':
            self._fileGenerator = FileGenerator(template_path='templates')
            for row in data:
                module_sub_idx = row[1]
                module_name = row[2].strip()
                active_ports = eval(row[3].strip())

                modules = self._fileGenerator.add_module(module_name, active_ports, module_sub_idx=module_sub_idx)
                # method add_module returns a list of generated module info (including file names and contents). If the
                # subject module is IO, the list contains 2 modules- subject and test
                if len(modules) == 2:
                    test_module = modules[1]
                    sub_module = modules[0]
                    data_processed.append([row[1], test_module.file_name+'.ar', test_module.content_ar,
                                           test_module.file_name+'.io', test_module.content_io,
                                           sub_module.file_name+'.ar', sub_module.content_ar,
                                           sub_module.file_name+'.io', sub_module.content_io])
                else:
                    sub_module = modules[0]
                    data_processed.append([row[1], 'empty.ar', '', 'empty.io', '',
                                           sub_module.file_name + '.ar', sub_module.content_ar,
                                           sub_module.file_name + '.io', sub_module.content_io])
            response = sqlToJson(['ID', 'test_name_ar', 'test_file_ar', 'test_name_io', 'test_file_io', 'sub_name_ar',
                                  'sub_file_ar',  'sub_name_io', 'sub_file_io'], data_processed, cursor.description)
            # overwriting variable types- cursor.description contains information on the actual database
            # table that has only 4 columns.
            response['types'] = ['TINY', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING',
                                 'VAR_STRING', 'VAR_STRING']
            self._query_type = 'conf'
            print('sending module configuration files: ')
            for row in response['data']:
                print([row[content][0:min(len(row), 100)] if content != 'ID' else row[content] for content in row])

        # second query - the data returned from the database after this query is discarded.
        # It generates main configuration file based on the previous query with all the module data
        elif self._query_type == 'conf':
            response = sqlToJson(['config'], [[self._fileGenerator.generate_main_file()]], cursor.description)
            response['types'] = ['VAR_STRING']
            print('main configuration file: \n'+str(response))
            self._query_type = 'io'

        # third query - based on active ports data received in the first query, a table of
        # desired connections is generated. The table has a following structure:
        # [[di_conn[0], do_conn[0], ai_conn[0], ao_conn[0]],[di_conn[1], do_conn[1], ai_conn[1], ao_conn[1]], ...]
        # it is necessary that all the connection types (di, do, ai, ao) have the same length.
        elif self._query_type == 'io':
            conn = self._fileGenerator.connections

            # to ensure that connection lists of each type have the same length, they are filled with empty strings
            max_len = max([len(conn[key]) for key in conn])
            for key in conn:
                while len(conn[key]) < max_len:
                    conn[key].append('')

            # the connection list is converted from
            # {'di':[di1, di2...], 'do':[do1, do2...], 'ai':[a1, ai2...], 'ao':[ao1, ao2...]}
            # to
            # [[d1, do1, ai1, ao1],[d2, do2, ai2, ao2],...]
            response = sqlToJson(['di', 'do', 'ai', 'ao'],
                                 [[conn['di'][i], conn['do'][i], conn['ai'][i], conn['ao'][i]] for i in range(len(conn['di']))],
                                 cursor.description)
            response['types'] = ['VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING']
            self._query_type = 'modules'
            print('connections: \n'+str(response))
        cursor.close()
        #debug_log(response)
        self._jsonResponse = makeJsonResponse(0, "", response)
        return json.dumps({"responseSize": len(self._jsonResponse)})


def sqlToJson_offline(column_names, dataIn):
    types = []
    data = []
    for row in dataIn:
        i = 0
        dataRow = collections.OrderedDict()
        for field in row:
            dataRow[column_names[i]] = field
            i = i + 1
        data.append(dataRow)
    response = {}
    response['data'] = data
    response['types'] = types
    return response


class DB_offline:

    _user = None
    _password = None
    _host = None
    _database = None
    _cnx = None
    _jsonResponse = None
    _query_type = 'modules'
    _fileGenerator = FileGenerator(template_path='templates')

    def connect(self, user, password, host, port, database):
        print('connected to offline database')

    def disconnect(self):
        print('disconnecting from offline database')

    def getData(self):
        return self._jsonResponse

    def query(self, sql):
        begin = re.search('FROM', sql).start()
        end = re.search('WHERE', sql).start()
        table_name = sql[begin + 5:end - 1]
        print('table name: ' + table_name)
        ID_project = re.findall(r'\d+', sql)[-1]

        # change all queries to selecting all module entries from a given project
        sql = 'SELECT * FROM ' + table_name + " WHERE ID_project = '"+ID_project+"';"
        print('ID_project = '+ID_project)
        for statement in re.sub(r'(\)\s*);', r'\1%;%', sql).split('%;%'):
            print('simulating executing: ' + statement)
        response = {}
        #subject_modules = ['X20AT2222', 'X20AI2622', 'X20DI9371', 'X20AO2622', 'X20DO9322']
        subject_modules = ['X20PS9400a', 'X20DC1376', 'X20AT2222', 'X20AI2622', 'X20DI9371', 'X20AO2622', 'X20DO9322']

        # simulation of database return data
        # data = [[1, 1, subject_modules[0], '[1,2]'], [1, 2, subject_modules[1], '[1,2]'],
        #         [1, 3, subject_modules[2], '[1,2]'], [1, 4, subject_modules[3], '[1,2]'],
        #         [1, 5, subject_modules[4], '[1,2]']]
        data = [[1, 1, subject_modules[0], '[]'], [1, 2, subject_modules[1], '[]'],
                [1, 3, subject_modules[2], '[]'], [1, 4, subject_modules[3], '[1]'],
                [1, 5, subject_modules[4], '[4]'], [1, 6, subject_modules[5], '[]'],
                [1, 7, subject_modules[6], '[1,11]']]
        data_processed = []

        # First query - returns the list of all necessary module configuration files to automation studio
        if table_name == 'modules':
            self._fileGenerator = FileGenerator(template_path='templates')
            for row in data:
                print(row)
                module_sub_idx = row[1]
                module_name = row[2]
                active_ports = eval(row[3])

                modules = self._fileGenerator.add_module(module_name, active_ports, module_sub_idx=module_sub_idx)
                # method add_module returns a list of generated module info (including file names and contents). If the
                # subject module is IO, the list contains 2 modules- subject and test
                if len(modules) == 2:
                    test_module = modules[1]
                    sub_module = modules[0]
                    data_processed.append([row[1], test_module.file_name+'.ar', test_module.content_ar,
                                           test_module.file_name+'.io', test_module.content_io,
                                           sub_module.file_name+'.ar', sub_module.content_ar,
                                           sub_module.file_name+'.io', sub_module.content_io])
                else:
                    sub_module = modules[0]
                    data_processed.append([row[1], 'empty.ar', '', 'empty.io', '',
                                           sub_module.file_name + '.ar', sub_module.content_ar,
                                           sub_module.file_name + '.io', sub_module.content_io])
            response = sqlToJson_offline(['ID', 'test_name_ar', 'test_file_ar', 'test_name_io', 'test_file_io', 'sub_name_ar',
                                  'sub_file_ar',  'sub_name_io', 'sub_file_io'], data_processed)
            # overwriting variable types- cursor.description contains information on the actual database
            # table that has only 4 columns.
            response['types'] = ['TINY', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING',
                                 'VAR_STRING', 'VAR_STRING']
            self._query_type = 'conf'
            print('sending module configuration files: ')
            for row in response['data']:
                print([row[content][0:min(len(row[content]), 1000)] if content != 'ID' else row[content] for content in row])

        # second query - the data returned from the database after this query is discarded.
        # It generates main configuration file based on the previous query with all the module data
        elif table_name == 'conf':
            response = sqlToJson_offline(['config'], [[self._fileGenerator.generate_main_file()]])
            response['types'] = ['VAR_STRING']
            print('main configuration file: \n'+str(response))
            self._query_type = 'io'

        # third query - based on active ports data received in the first query, a table of
        # desired connections is generated. The table has a following structure:
        # [[di_conn[0], do_conn[0], ai_conn[0], ao_conn[0]],[di_conn[1], do_conn[1], ai_conn[1], ao_conn[1]], ...]
        # it is necessary that all the connection types (di, do, ai, ao) have the same length.
        elif table_name == 'io':
            conn = self._fileGenerator.connections

            # to ensure that connection lists of each type have the same length, they are filled with empty strings
            max_len = max([len(conn[key]) for key in conn])
            for key in conn:
                while len(conn[key]) < max_len:
                    conn[key].append('')

            # the connection list is converted from
            # {'di':[di1, di2...], 'do':[do1, do2...], 'ai':[a1, ai2...], 'ao':[ao1, ao2...]}
            # to
            # [[d1, do1, ai1, ao1],[d2, do2, ai2, ao2],...]
            response = sqlToJson_offline(['di', 'do', 'ai', 'ao'],
                                         [[conn['di'][i], conn['do'][i], conn['ai'][i], conn['ao'][i]] for i in range(len(conn['di']))])
            response['types'] = ['VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING']
            self._query_type = 'modules'
            print('connections: \n'+str(response))
        #debug_log(response)
        self._jsonResponse = makeJsonResponse(0, "", response)
        return json.dumps({"responseSize": len(self._jsonResponse)})


class S(BaseHTTPRequestHandler):

    __sqlDb = DB_offline()

    def _set_headers(self, contentLength):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header("Content-Length", contentLength)
        self.send_header("Connection", "Keep-Alive")
        self.end_headers()

    def _respond(self, jsonResponse):
        self._set_headers(len(jsonResponse))
        self.wfile.write(jsonResponse)

    def do_GET(self):
        self._set_headers(len("server up.."))
        self.wfile.write("server up..")

    def do_POST(self):
        # FIXME: handle invalid request
        length = int(self.headers.getheader('content-length'))
        data = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        jsonRequest = data.items()[0][0]
        try:
            serialized = json.loads(jsonRequest)
        except Exception as ex:
            print('failed parsing {0}'.format(jsonRequest))
            self._respond(makeJsonResponse(2, "", {}))
            return
        try:
            if serialized.has_key("getData"):
                # get actual data
                self._respond(self.__sqlDb.getData())
            else:
                # Execute query to get response size
                execQuery = serialized['query']
                if(args.sqlType == 'mssql'):
                    execQuery = execQuery.translate({ord(c): None for c in '`'})
                else:
                    execQuery = execQuery
                self._respond(self.__sqlDb.query(execQuery))
        except KeyError:
            try:
                # try to connect and do test query
                connection = serialized['connection'][0]
                self.__sqlDb.connect(connection['user'], connection['password'], args.sqlHost, args.sqlPort, connection['database'])
                self._respond(makeJsonResponse(0, "", {}))
            except KeyError:
                # try to disconnect
                self._respond(self.__sqlDb.disconnect())
            except Exception as ex:
                debug_print(ex[0],ex[1])
                self._respond(makeJsonResponse(ex[0], ex[1], ""))

def run(server_class=HTTPServer, handler_class=S, webServerPort=85):
    handler_class.protocol_version = 'HTTP/1.1'
    httpd = SocketServer.TCPServer(("",webServerPort),handler_class)
    print('Starting httpd at port ' + str(webServerPort))
    print('SQL server host ' + args.sqlHost + ':' + str(args.sqlPort))
    # FIXME: line below sets up HTTPS server, but it is args.sqlType yet supported from a client side
    # httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    __version__ = "V5.4.0"
    parser = argparse.ArgumentParser(
        description='This script works as a bridge between MpDatabase and defined SQL server',
        epilog='EXAMPLES:\n\n# start the script with default parameters (85, 127.0.0.1, 3306, mysql)\n$ python mappDatabaseConnector.py\n\n# start the script with defined parameters (e.g. 86, 192.168.1.15, 58964, mssql)\n$ python mappDatabaseConnector.py 86 \'192.168.1.15\' 58964 \'mssql\'',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('httpPort', type=str,
                    default='85', const=1, nargs='?',
                    help='http server port (default: 85)')
    parser.add_argument('sqlHost', type=str,
                    default='127.0.0.1', const=1, nargs='?',
                    help='sql server host (default: 127.0.0.1)')
    parser.add_argument('sqlPort', type=int,
                    default=3306, const=1, nargs='?',
                    help='sql server port (default: 3306)')
    parser.add_argument('sqlType', type=str,
                    default='mysql', const=1, nargs='?',
                    help='sql server type: mysql, mssql (default: mysql)')
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-l', type=str,
                    const=1, nargs='?', default='',
                    help='File name (full path) to log SQL response. File must be writable, data is overwritten')
    args = parser.parse_args()
    #db = DB()
    #db.query("SELECT ID,Config,Config_Name FROM Projekt_BR1 WHERE ID = '1'")
    run(webServerPort=int(args.httpPort))
    
    