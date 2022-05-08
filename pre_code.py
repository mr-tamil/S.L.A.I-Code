# Version 0.2

import os
import subprocess


def binary_to_string(data):
    string = ''
    for b in data:
        string += chr(b)

    return string


def new_name_create(file_name, data):
    # split the original file name
    entered_in = False
    try:
        name, format_ = file_name.rsplit('.', 1)
        normal = True

    except:
        format_ = ''
        name = file_name
        normal = False

    # check the file name exists or not
    try:
        if file_name in data:

            entered_in = True
            # check the condition
            if '(' in name and (name[-1] == ')'):
                name_0 = name.rsplit('(', 1)
                number = name_0[-1][:-1]
                # if the value inside () is int
                try:
                    number = int(number)
                    file_name = name + '.' + format_

                    number = 0

                    # checking path exists
                    if normal == False:
                        file_name = file_name[:-1]

                    while file_name in data:
                        number += 1
                        name = name_0[0].strip() + f' ({number})'
                        file_name = name + '.' + format_
                        if normal == False:
                            file_name = file_name[:-1]
                    if normal == False:
                        file_name = file_name + '.'

                # if the value inside () is not int
                except:
                    name = name.strip()
                    name_0 = name + f' ({1})'
                    file_name = name_0 + '.' + format_
                    number = 1

                    if normal == False:
                        file_name = file_name[:-1]
                    # checking path exists
                    while file_name in data:
                        number += 1
                        name_0 = name + f' ({number})'
                        file_name = name_0 + '.' + format_
                        if normal == False:
                            file_name = file_name[:-1]
                    if normal == False:
                        file_name = file_name + '.'


            # if the condition fails
            else:
                name = name.strip()
                name_0 = name + f' ({1})'
                file_name = name_0 + '.' + format_
                number = 1

                if normal == False:
                    file_name = file_name[:-1]

                # checking path exists
                while file_name in data:
                    number += 1
                    name_0 = name + f' ({number})'
                    file_name = name_0 + '.' + format_

                    if normal == False:
                        file_name = file_name[:-1]

                if normal == False:
                    file_name = file_name + '.'
    except:
        pass

    if normal == False and entered_in == True:
        file_name = file_name[:-1]
    return file_name


# rename for copy the file
def file_name_creation(file_name, data='', bt='t'):
    # split the original file name

    name, format_ = file_name.rsplit('.', 1)

    # check the file name exists or not
    if os.path.exists(file_name) == True:

        # check the condition
        if '(' in name and (name[-1] == ')'):
            name_0 = name.rsplit('(', 1)
            number = name_0[-1][:-1]

            # if the value inside () is int
            try:
                number = int(number)
                file_name = name + '.' + format_

                number = 0

                # checking path exists
                while os.path.exists(file_name) == True:
                    number += 1
                    name = name_0[0].strip() + f' ({number})'
                    file_name = name + '.' + format_



            # if the value inside () is not int
            except:
                name = name.strip()
                name_0 = name + f' ({1})'
                file_name = name_0 + '.' + format_
                number = 1

                # checking path exists
                while os.path.exists(file_name) == True:
                    number += 1
                    name_0 = name + f' ({number})'
                    file_name = name_0 + '.' + format_



        # if the condition fails
        else:
            name = name.strip()
            name_0 = name + f' ({1})'
            file_name = name_0 + '.' + format_
            number = 1

            # checking path exists
            while os.path.exists(file_name) == True:
                number += 1
                name_0 = name + f' ({number})'
                file_name = name_0 + '.' + format_

        # mention binary/text mode
        def mode(op, bt=bt):
            return op + bt

        if bt == 't':
            pass

        else:
            data = data.encode('ascii')

        # creating new file with new name
        with open(file_name, mode('w')) as file:
            file.write(data)

    return file_name
