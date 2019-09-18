BASE_PATH_SUBJECT = "IF1.ST2.IF1.ST"
BASE_PATH_TEST = "IF1.ST1.IF1.ST"

import re
import os


def bind_IO_pv(variable_name):
    # Function that generates the appropriate line to insert in io file to bind port with PV
    # Input and output lines differ slightly so we assume the 2nd character is o if output and i if input
    if variable_name[1] == 'o':
        return '<Prod Device="TC#4-CPYDEV" DPName="::' + variable_name + '" Kind="pv"/>'
    else:
        return '<Cons Device="TC#4-CPYDEV" DPName="::' + variable_name + '" Kind="pv"/>'


def module_type(module_name):
    # This function determines the type of module - di, do, ai, ao or other, based on the name
    if 'DI' in module_name or 'di' in module_name:
        return 'di'
    if 'DO' in module_name or 'do' in module_name:
        return 'do'
    if 'AI' in module_name or 'ai' in module_name:
        return 'ai'
    if 'AO' in module_name or 'ao' in module_name:
        return 'ao'
    return 'other'

def get_complementary_module(module_name):
    # This method assigns a testing module for subject module given as argument
    # TODO: modify this function so it detects the type of module, not just hard coded module name
    if module_name == 'X20AI2622':
        return 'X20AO2622'
    if module_name == 'X20AO2622':
        return 'X20AI2622'
    if module_name == 'X20DI9371':
        return 'X20DO9322'
    if module_name == 'X20DO9322':
        return 'X20DI9371'
    else:
        return None


class ModuleConfiguration:
    # This class represents a module- it contains its path, name and contents of the configuration files
    def __init__(self, path, file_name, content_ar, content_io):
        self.path = path
        self.file_name = file_name
        self.content_ar = content_ar
        self.content_io = content_io

    def store_files(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        f = open(directory + '/' + self.file_name + '.ar', 'w')
        f.write(self.content_ar)
        f.close()
        f = open(directory + '/' + self.file_name + '.io', 'w')
        f.write(self.content_io)
        f.close()


class FileGenerator:
    # This class generates configuration files
    def __init__(self, template_path='templates'):
        self.template_path = template_path
        self.module_idx_subject = 2
        self.module_idx_test = 4 #PS,DC,AT hardcoded
        self.modules = []
        self.connections = {'di': [], 'do': [], 'ai': [], 'ao': []}

    def add_module(self, module_name, active_ports, module_sub_idx=None, module_test_idx=None):
        # Calling this method will add the subject module given as argument to the list of configured modules.
        # It automatically generates .io and .ar for the module and, if necessary, for the complementary testing module.
        # The method also adds the connections specified in active_ports argument to the list
        modules = []
        if module_sub_idx is not None:
            self.module_idx_subject = module_sub_idx
        if module_test_idx is not None:
            self.module_idx_test = module_test_idx
        modules.append(ModuleConfiguration(BASE_PATH_SUBJECT+str(self.module_idx_subject),
                                         module_name+'_sub'+str(self.module_idx_subject),
                                         self.generate_ar(module_name, is_on_subject=True),
                                         self.generate_io(module_name, is_on_subject=True)))

        self.module_idx_subject += 1

        testing_module = get_complementary_module(module_name)
        if testing_module is not None:
            modules.append(ModuleConfiguration(BASE_PATH_TEST + str(self.module_idx_test),
                                               testing_module + '_test' + str(self.module_idx_test),
                                               self.generate_ar(testing_module, is_on_subject=False),
                                               self.generate_io(testing_module, is_on_subject=False)))
            print(self.module_idx_test)
            self.module_idx_test += 1
        self.modules += modules
        if not module_type(module_name) == 'other':
            for port in active_ports:
                self.connections[module_type(module_name)].append(str(self.module_idx_subject-1).zfill(2) +
                                                                  str(port).zfill(2) +
                                                                  str(self.module_idx_test-1).zfill(2) +
                                                                  str(port).zfill(2))
        return modules

    def create_other(self):
        # This method creates empty template files for any module that is not IO.
        # It should be called if the other.io or other.ar is not found in templates directory
        if not os.path.isdir(self.template_path):
            os.mkdir(self.template_path)
        f = open(self.template_path + '/other.ar', 'w')
        f.write('  <?xmlversion="1.0"?>\n'
                '<?AutomationRuntimeIOSystem Version = 1.0?>\n'
                '<IOCFG xmlns="http://www.br-automation.com/AR/IO" Version="2.0">\n'
                '<Module ID="#module_path#" Hardware="#module_name#">\n'
                '<Parameter ID="HardwareModuleName" Value="#module_name#" />\n'
                '</Module>\n'
                '</IOCFG>)')
        f.close()
        f = open(self.template_path + '/other.io', 'w')
        f.write('<?xmlversion="1.0" encoding="utf-8"?>\n'
                '<?AutomationRuntimeIOSystem Version="1.0"?>\n'
                '<IO xmlns="http://www.br-automation.com/AR/IO">\n'
                '<Links>\n'
                '</Links\n'
                '</IO>')
        f.close()

    def generate_ar(self, module_name, is_on_subject):
        # This method generates a .ar configuration file
        if is_on_subject:
            module_path = BASE_PATH_SUBJECT+str(self.module_idx_subject)
        else:
            module_path = BASE_PATH_TEST + str(self.module_idx_test)

        if module_type(module_name) == 'other':
            if not os.path.isfile(self.template_path+'/other.ar'):
                self.create_other()
            f = open(self.template_path+'/other.ar', 'r')
            file_content = f.read()
            file_content = re.sub('#module_path#', module_path, file_content)
            file_content = re.sub('#module_name#', module_name, file_content)
            return file_content
        try:
            f = open(self.template_path + '/' + module_name + '.ar', 'r')
        except:
            raise Exception('couldn\'t open file "' + module_name + '.ar' + '" in directory "'+self.template_path +
                            '". Run generate_templates function first to generate necessary configuration files')


        file_content = f.read()
        file_content = re.sub('#module_path#', module_path, file_content)
        file_content = re.sub('"Supervision" Value="on"', '"Supervision" Value="off"', file_content)
        return file_content


    def generate_io(self, module_name, is_on_subject):
        # This method generates a .io configuration file. If the module is IO, it modifies the template file to bind
        # ports to appropriate array elements, according to the module's type and path
        if module_type(module_name) == 'other':
            if not os.path.isfile(self.template_path+'/other.io'):
                self.create_other()
            f = open(self.template_path+'/other.io', 'r')
            return f.read()
        if is_on_subject:
            array_name = module_type(module_name)+'_sub[' + str(self.module_idx_subject)
            module_path = BASE_PATH_SUBJECT+str(self.module_idx_subject)
        else:
            array_name = module_type(module_name)+'_test[' + str(self.module_idx_test)
            module_path = BASE_PATH_TEST + str(self.module_idx_test)
        template_file = self.template_path + '/' + module_name+'.io'
        try:
            f = open(template_file, 'r')
        except:
            raise Exception('couldn\'t open file "' + template_file+ '" in directory "'+self.template_path)
        file_content = f.read()

        io_binds = re.findall('#....#', file_content)
        for bind in io_binds:
            port_idx = bind[3:5]
            if port_idx[0] =='0':
                port_idx = port_idx[1]
            variable_name = array_name+','+port_idx+']'
            file_content = re.sub(bind, bind_IO_pv(variable_name), file_content)

        file_content = re.sub('#module_path#', module_path, file_content)
        file_content = re.sub('#....#', '', file_content)

        return file_content

    def generate_main_file(self):
        # This method returns a main configuration file based on all the modules that have been added by add_module method
        content = '<IOCFG xmlns="http://www.br-automation.com/AR/IO" Version="2.0">\n' \
                  '<Module ID="$root" Source = "AR" SourceID="$root" />\n' \
                  '<Module ID="IF1.ST1" Source = "AR" SourceName="X20BC0083" />\n' \
                  '<Module ID="IF1.ST2" Source = "AR" SourceName="X20BC0083" />\n' \
                  '<Module ID="IF1.ST1.IF1.ST1" Source = "AR" SourceName="X20PS9400a" />\n' \
                  '<Module ID="IF1.ST1.IF1.ST2" Source = "AR" SourceName="X20DC1376" />\n' \
                  '<Module ID="IF1.ST1.IF1.ST3" Source = "AR" SourceName="X20AT2222" />\n'
        for module in self.modules:
            content += '<Module ID="' + module.path + '" Source = "Template" SourceName="' + module.file_name + '" />\n'
        content += '</IOCFG>'
        return content

    def store_files(self, directory='processed'):
        # This method stores all files on local machine (for debugging or manual file transfer to the PLC)
        for module in self.modules:
            module.store_files(directory)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        f = open(directory+'/configuration.xml', 'w')
        f.write(self.generate_main_file())
        f.close()
