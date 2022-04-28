# Version 0.2

# add DictWriter in csv


import os
import pre_code
import csv
import json
import numpy

text_files = {'txt': 't',
              'json': 't',
              'csv': 't'}

making_in_pro = ['txt', 'csv', 'json']


# class FileHandler to edit file
class FileHandler:
    # ri stands required input # ToDo
    def __init__(self, file_name= os.path.join(os.path.dirname(os.path.realpath(__file__)),'file.txt'), bt=None, ff=None):
        file_format = file_name.rsplit('.', 1)[-1]

        # mention binary/text mode
        if bt == None:
            try:
                if text_files[file_format] == 't':
                    self.bt = 't'
                else:
                    self.bt = 'b'

            except:
                self.bt = 'b'

        else:
            self.bt = bt

        # file format
        if ff == None:
            if file_format == 'csv':
                self.ff = 'csv'

            elif file_format == 'json':
                self.ff = 'json'

            else:
                self.ff = 'txt'

        else:
            if ff in making_in_pro:
                self.ff = ff

            else:
                raise Exception(f"Only {making_in_pro} is accepted.")

        self.file_name = r'{}'.format(file_name)

        if os.path.exists(self.file_name):
            pass
        else:
            open(self.file_name, self.mode('w'))

    # adding information
    def append(self, info, continuity=False):

        if self.ff == 'txt':
            temp = open(self.file_name, self.mode('r')).read()

            nl = '\n'
            if continuity == True or temp == b'' or temp == '':
                nl = ''
            if self.bt == 'b':
                nl = nl.encode('ascii')

            with open(self.file_name, self.mode('a')) as file:
                file.write(nl + info)

        # CSV adding data
        elif self.ff == 'csv':
            with open(self.file_name, self.mode('a')) as file:
                write = csv.writer(file)

                if numpy.array(info).ndim == 1:
                    write.writerow(info)

                else:
                    write.writerows(info)


        # JSON adding data
        elif self.ff == 'json':
            with open(self.file_name, self.mode('r')) as file:
                try:
                    read = json.load(file)

                except:
                    read = {}

                if type(info) == str:
                    info = json.loads(info)

                for key in info.keys():
                    read[key] = info[key]

            with open(self.file_name, self.mode('w')) as file:
                json.dump(read, file)

    # deleting the file completely
    @property
    def delete(self):
        os.remove(self.file_name)

    @delete.deleter
    def file(self):
        os.remove(self.file_name)

    # empty the file
    @property
    def clear(self):
        clear = open(self.file_name, self.mode('w'))

        if self.ff == 'json':
            json.dump({}, clear)

    # write the information
    def write(self, info):
        if self.ff == 'txt':
            with open(self.file_name, self.mode('w')) as file:
                file.write(info)

        # CSV adding data
        elif self.ff == 'csv':
            with open(self.file_name, self.mode('w')) as file:
                write = csv.writer(file)

                if numpy.array(info).ndim == 1:
                    write.writerow(info)

                elif numpy.array(info).ndim == 2:
                    write.writerows(info)

                else:
                    print('Only 1 or 2 dimention array is accepted.')

        # JSON adding data
        elif self.ff == 'json':
            with open(self.file_name, self.mode('w')) as file:

                if type(info) == dict:
                    json.dump(info, file)

                elif type(info) == str:
                    file.write(info)

                else:
                    print("Only 'dict' and 'json string' is accepted'")

    # read the file
    def read(self, str_=False, delimiter=',', indent=0):

        # opening original file
        original_file = open(self.file_name, self.mode('r')).read()

        if str_ == False and self.ff == 'csv':
            with open(self.file_name, self.mode('r')) as file:
                data = csv.DictReader(file)
                original_file = []
                for line in data:
                    original_file.append(line)

        elif self.ff == 'json':
            original_file = json.load(open(self.file_name))

            if str_ == True:
                original_file = json.dumps(original_file, indent=indent)

        return original_file

    # copy the file with new file name
    def copy_file(self, copy_file_name=None):

        # opening original file
        original_file = open(self.file_name, self.mode('r')).read()

        # if copy file name not declared
        if copy_file_name != None:

            # creating new file with new name
            with open(copy_file_name, self.mode('w')) as file:
                file.write(original_file)

        # if copy file name declared
        else:
            return pre_code.file_name_creation(self.file_name, data=original_file, bt=self.bt)

    def __str__(self):
        # print readed file
        original_file = open(self.file_name, self.mode('r')).read()

        return original_file

    # adding binary or text mode in modes
    def mode(self, op=''):
        return op + self.bt

    #	def req_input(self,ri):
    #		if self.ff == 'csv':
    #			if ri == None:
    #				self.delimiter = ','
    #			if ri != None:
    #				self.delimiter = ri['delimiter']
    #				with open(self.file_name, self.mode('r')) as file:

    # getting all the info
    @property
    def info(self):
        try:
            check_file = open(self.file_name, 'rt').read()
            mode = 'text/binary'

        except:
            mode = 'binary'

        return {'name': self.file_name, 'mode': mode}
