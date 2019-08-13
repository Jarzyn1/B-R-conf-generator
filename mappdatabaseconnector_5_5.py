#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import datetime
import urlparse
import SocketServer
import collections
import decimal
import re

from mysql.connector import FieldType
from file_generator import FileGenerator

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
    print('status: '+str(status)+' of class '+str(status.__class__.__name__))

    data['message'] = message
    print('message: ' + str(status) + ' of class ' + str(status.__class__.__name__))

    data['response'] = response
    print('response: ' + str(status) + ' of class ' + str(status.__class__.__name__))
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
        return float(o) # python's float has double precision

class DB:
    def __init__(self):
        self.file_generator = FileGenerator()

    _user = None
    _password = None
    _host = None
    _database = None
    _cnx = None
    _jsonResponse = None

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
            import mysql
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
        print("getData function: " + str(self._jsonResponse))
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
        # split multistatement queries, but ignore semicolon within queries
        for statement in re.sub(r'(\)\s*);', r'\1%;%', sql).split('%;%'):
            cursor.execute(statement)
        print('query will be executed: ' + sql)
        data = []
        response = {}
        # Always try to fetch data independent of insert / select
        try:
            data = cursor.fetchall()
            data_processed = self.file_generator.generate_response(data["module_name"], eval(data["active_ports"]))
        except Exception as ex:
            pass
        # cursor description is available if there was a response
        # Hence we create the json response that can later be forwared
        if(cursor.description):
            if(args.sqlType == 'mssql'):
                column_names = [column[0] for column in cursor.description]
            else:
                column_names = cursor.column_names
            response = sqlToJson(column_names, data, cursor.description)
        self._cnx.commit()
        cursor.close()
        debug_log(response)
        self._jsonResponse = makeJsonResponse(0, "", response)

        print("query function: "+str(self._jsonResponse))
        return json.dumps({"responseSize":len(self._jsonResponse)})

class S(BaseHTTPRequestHandler):

    __sqlDb = DB()

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

    run(webServerPort=int(args.httpPort))