# Version 0.2

import subprocess
import os
import smtplib
from email.message import EmailMessage
# filehandler = __import__("filehandler_v0.2")


# main()

# Method 1: Send Mail
# class Mail:
#     def __init__(self, user, pwd):
#         self.service = smtplib.SMTP('smtp.gmail.com', 587)
#         self.service.starttls()
#         self.service.login(user, pwd)
#
#     def send_message(self, receiver, message):
#         self.service.sendmail("shield.ai.001@gmail.com", f"{receiver}", message)
#         # self.service.quit()


# Mail: sending Files
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
#
# sender = "shield.ai.001@gmail.com"
# receiver = "highnesslee003@gmail.com"
# msg = MIMEMultipart()
# msg['From'] = sender
# msg['To'] = receiver
# msg['Subject'] = "Testing_Subject"
# body = f"Testing_02 from {sender}"
# msg.attach(MIMEText(body, 'plain'))
# filename = "Image.jpg"
# attachment = open("image_3.jpg", "rb")
# p = MIMEBase('application', 'octet-stream')
# p.set_payload((attachment).read())
# encoders.encode_base64(p)
# p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# msg.attach(p)
# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
# s.login(sender, "Mr.Dinesh000@Shield")
# text = msg.as_string()
# s.sendmail(sender, receiver, text)
# s.quit()


# Method 2: Send Mail
class Mail:
    def __init__(self, user, pwd):
        self.msg = EmailMessage()
        self.msg['from'] = user
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(user, pwd)

    def send_mail(self, sub, body, to):
        self.msg['subject'] = sub
        self.msg['to'] = to
        self.msg.set_content(body)
        self.server.send_message(self.msg)

    def exit(self):
        self.server.quit()


# Testing
'''
user = "shield.ai.001@gmail.com"
pwd = "Mr.Dinesh000@Shield"
receiver = "highnesslee003@gmail.com"

body = """Hi Dinesh,

    Testing_01 from SHIELD A.I"""

mail = Mail(user, pwd)
mail.send_mail('Highliss System Password', body, 'mr.tamil003@gmail.com')
'''


# WiFi Connect
def connect_wifi(ssid):
    os.system(f'''cmd /c "netsh wlan connect name={ssid}"''')


# WiFi search networks availability
def show_availabe_wifi():
    # os.system('cmd /c "netsh wlan show networks"') # just showing, not get string
    devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    devices = devices.decode('ascii')
    data = devices
    lines = [i for i in data.splitlines()]

    try:
        output = [["Availables", int(lines[2].split(' ')[2])]]
    except:
        output = [["Availables", 0]]

    for line in lines:
        if line == '':
            continue

        if ':' in line:
            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            output.append([key, value])

    data = {}
    for i in range(output[0][1]):
        j = 4 * i
        l = [output[2 + j], output[3 + j], output[4 + j], output[5 + j]]
        data[f"Device_{i + 1}"] = l

    return data


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
