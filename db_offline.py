from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from file_generator import FileGenerator
import json
import collections
import re

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
        subject_modules = ['X20PS9400', 'X20DC1376', 'X20AT2222', 'X20AI2622', 'X20DI9371', 'X20AO2622', 'X20DO9322']
        # data = [[1, 1, subject_modules[0], '[1,2]'], [1, 2, subject_modules[1], '[1,2]'],
        #         [1, 3, subject_modules[2], '[1,2]'], [1, 4, subject_modules[3], '[1,2]'],
        #         [1, 5, subject_modules[4], '[1,2]']]
        data = [[1, 1, subject_modules[0], ''], [1, 2, subject_modules[1], ''],
                [1, 3, subject_modules[2], ''], [1, 4, subject_modules[3], '[1,2]'],
                [1, 5, subject_modules[4], '[1,2]'], [1, 6, subject_modules[5], '[3,4]'],
                [1, 7, subject_modules[6], '[1,4]']]

        data_processed = []

        # First query in the cycle- returns the list of all necessary module configuration files to automation studio
        if self._query_type == 'modules':
            self._fileGenerator = FileGenerator(template_path='templates')
            for row in data:
                print('row[2]', row[2])
                modules = self._fileGenerator.add_module(row[2], eval(row[3]))
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
                    data_processed.append([row[1], 'empty.ar', [], 'empty.io', [],
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
                print([row[content][0:min(len(row), 100)] if content != 'ID' else row[content] for content in row])

        # second query in the cycle- the data returned from the database after this query is discarded.
        # It generates main configuration file based on the previous query with all the module data
        elif self._query_type == 'conf':
            response = sqlToJson_offline(['config'], [[self._fileGenerator.generate_main_file()]])
            response['types'] = ['VAR_STRING']
            print('main configuration file: \n'+str(response))
            self._query_type = 'io'

        # third query in the cycle- based on active ports data received in the first query, generates a table of
        # desired connections. The table has a following structure:
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
            response = sqlToJson_offline(['di', 'do', 'ai', 'ao'],
                                         [[conn['di'][i], conn['do'][i], conn['ai'][i], conn['ao'][i]] for i in range(len(conn['di']))])
            response['types'] = ['VAR_STRING', 'VAR_STRING', 'VAR_STRING', 'VAR_STRING']
            self._query_type = 'modules'
            print('connections: \n'+str(response))
        #debug_log(response)
        self._jsonResponse = makeJsonResponse(0, "", response)
        return json.dumps({"responseSize": len(self._jsonResponse)})
