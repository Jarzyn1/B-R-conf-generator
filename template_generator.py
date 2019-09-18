import re
import os


class Module:
    def __init__(self, text):
        self.text_ar = text
        parameters = re.findall('".*?"', text)
        self.ID = parameters[0][1:-1]
        self.hardware = parameters[1][1:-1]
        self.text_io = ''

    def merge(self, module):
        self.text_ar += module.text_ar

    def add_headers_footers(self):
        self.text_ar = '<?xmlversion="1.0"?>\n' \
                       '<?AutomationRuntimeIOSystem Version = 1.0?>\n' \
                       '<IOCFG xmlns="http://www.br-automation.com/AR/IO" Version="2.0">\n' + self.text_ar + '\n</IOCFG>'
        self.text_io = '<?xmlversion="1.0" encoding="utf-8"?>\n' \
                       '<?AutomationRuntimeIOSystem Version="1.0"?>\n' \
                       '<IO xmlns="http://www.br-automation.com/AR/IO">\n' \
                       '<Links>\n'+ self.text_io + '\n</Links>\n</IO>\n'

    def assign_io(self, text_io):
        beginings = [m.start() for m in re.finditer('<LN', text_io)]
        ends = [m.start() for m in re.finditer('</LN', text_io)]
        for char_start, char_end in zip(beginings, ends):
            fragment = text_io[char_start: char_end+5]
            parameters = re.findall('".*?"', fragment)
            if parameters[2][1:-1] == self.ID:
                di = re.findall('DigitalInput..', fragment)
                do = re.findall('DigitalOutput..', fragment)
                ai = re.findall('AnalogInput..', fragment)
                ao = re.findall('AnalogOutput..', fragment)
                if len(di) > 0:
                    replacement = '>\n#di'+di[0][-2:]+'#\n</LN>'
                    fragment = re.sub('>\s</LN>', replacement, fragment)
                if len(do) > 0:
                    replacement = '>\n#do'+do[0][-2:]+'#\n<Cons'
                    fragment = re.sub('>\s<Cons', replacement, fragment)
                if len(ai) > 0:
                    replacement = '>\n#ai'+ai[0][-2:]+'#\n</LN>'
                    fragment = re.sub('>\s</LN>', replacement, fragment)
                if len(ao) > 0:
                    replacement = '>\n#ao' + ao[0][-2:] + '#\n<Cons'
                    fragment = re.sub('>\s<Cons', replacement, fragment)
                self.text_io += fragment +'\n'


    def replace_ID(self, replacement='#module_path#'):
        self.text_ar = re.sub(self.ID, replacement, self.text_ar)
        self.text_io = re.sub(self.ID, replacement, self.text_io)


    def store_tamplate(self, templates_path):
        file_ar = open(templates_path+'/'+self.hardware+'.ar', 'w')
        file_io = open(templates_path+'/'+self.hardware+'.io', 'w')
        file_ar.write(self.text_ar)
        file_io.write(self.text_io)
        file_ar.close()
        file_io.close()

def generate_templates(ar_file_name = "backup/arconfig.ar.bup", io_file_name = "backup/iomap.io.bup", templates_path = "templates/"):
    ar_file = open(ar_file_name, 'r')
    io_file = open(io_file_name, 'r')
    content_ar = ar_file.read()
    content_io = io_file.read()
    beginings = [m.start() for m in re.finditer('<Module', content_ar)]
    ends = [m.start() for m in re.finditer('</Module', content_ar)]
    modules = []
    for char_start, char_end in zip(beginings, ends):
        modules.append(Module(content_ar[char_start: char_end+9]))

    for module in modules:
        same_hardware = [m for m in modules if m.hardware == module.hardware and not m == module]
        for m in same_hardware:
            module.merge(m)
            modules.remove(m)

    if not os.path.isdir(templates_path):
        os.mkdir(templates_path)
    for module in modules:
        module.assign_io(content_io)
        module.replace_ID()
        module.add_headers_footers()
        module.store_tamplate(templates_path)
