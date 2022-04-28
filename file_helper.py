# import required modules
import os
from fileinput import filename
from os import path
from pydub import AudioSegment
import requests
from kivy.properties import Clock
import numpy as np
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
import cv2
from kivy.graphics.texture import Texture
from pyfirmata import Arduino
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import Clock
import time

import database
import filehandler
import slaiCode


class SlaiCodeConnector(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = None
        self.controller = None
        self.ai = None

    def start(self):
        self.event = Clock.schedule_interval(self.activate, 1.0 / 1.0)
        self.ai = slaiCode.SlaiCode(self.controller)
        self.ai.start()
        self.event()
        self.controller.activate(37, "SLAI-Code Enabled.")
        self.controller.activate(12, "Welcome, slai Code Enabled.")

    def add_instances(self, controller):
        self.controller = controller

    def end(self):
        self.ai.end()
        self.controller.activate(37, "SLAI-Code Disabled.")
        self.controller.activate(12, "slai Code Disabled, We will see")
        self.event.cancel()

    def activate(self, *args):
        chat_input_text = self.controller.chat_input_text
        if chat_input_text is not None:
            self.ai.input(text= chat_input_text)
            self.controller.chat_input_text = None
        self.ai.process()


class Arduino_Control():
    def __init__(self):
        self.port = 'COM5'
        self.board = Arduino(self.port)

        self.front = self.board.get_pin('d:4:o')
        self.back = self.board.get_pin('d:5:o')  # Cleared
        self.left = self.board.get_pin('d:6:o')
        self.right = self.board.get_pin('d:7:o')  # Cleared
        self.up = self.board.get_pin('d:8:o')  # Cleared
        self.down = self.board.get_pin('d:9:o')
        self.emergency = self.board.get_pin('d:10:o')  # Created : My Way
        self.power = self.board.get_pin('d:2:o')  # Cleared

    def close(self):
        self.board.exit()

# convert mp3 file to wav file
def mp32wav(input, output):
    sound = AudioSegment.from_mp3(input)


def change_dimension(frame, ratio):
    shape = frame.shape
    img = cv2.resize(frame, (shape[1] // ratio, shape[0] // ratio))
    return img


def drawBox(img, bbox):
    x, y, w, h = [int(i) for i in bbox]
    cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


class Vision(MDBoxLayout):
    recording_started = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.image = Image()
        self.frame_rate = 30 # Testing :1.66
        self.add_widget(self.image)


    # @property
    def set_operation(self, operation, data):
        self.operation = operation
        self.data = data

        self.clock_it

    @property
    def clock_it(self):
        if self.operation == "camera":
            if self.data == 0:
                self.capture = cv2.VideoCapture(0)
                self.event = Clock.schedule_interval(self.Camera, 1.0 / self.frame_rate)
                self.event()
            if self.data == 1:
                self.event = Clock.schedule_interval(self.Saved_Mobile_Image, 1.0 / self.frame_rate)
                self.event()
            if self.data == 2:
                db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
                db = database.Database(db_path)
                data = db.table_data("system")
                url = data[3][2]
                self.capture = cv2.VideoCapture(url)
                self.event = Clock.schedule_interval(self.Mobile_Camera_Video, 1.0 / self.frame_rate)
                self.event()
            if self.data == 3:
                self.event = Clock.schedule_interval(self.Mobile_Camera_Image, 1.0 / self.frame_rate)
                self.event()

        if self.operation == 'video':
            self.event = Clock.schedule_interval(self.Video, 1.0 / self.frame_rate)
            self.event()

        if self.operation == "image":
            self.Image()

        # Model is for some purpose & Not in use
        if self.operation == "images":
            # Animation:
            self.event = Clock.schedule_interval(self.Image, 1.0 / self.frame_rate)
            self.event()

        if self.operation == "vision":
            if self.data == 0:
                camera = 0
            if self.data == 1:
                db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
                db = database.Database(db_path)
                data = db.table_data("system")
                url = data[3][2]
                camera = url
            self.external= False
            self.precious= True
            self.ratio = 3
            self.capture = cv2.VideoCapture(camera)
            # tracker = cv2.legacy.TrackerMOSSE_create()
            self.tracker = cv2.legacy.TrackerCSRT_create()


            self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))

            self.frame_height =int( self.capture.get( cv2.CAP_PROP_FRAME_HEIGHT))

            self.fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

            self.out = cv2.VideoWriter("output.avi", self.fourcc, 5.0, (1280,720))

            ret, self.frame1 = self.capture.read()
            ret, self.frame2 = self.capture.read()
            self.frame1 = change_dimension(self.frame1, self.ratio)
            self.frame2 = change_dimension(self.frame2, self.ratio)
            print(self.frame1.shape)

            self.bbox = cv2.selectROI("Tracking", self.frame1, False)
            self.tracker.init(self.frame1, self.bbox)

            self.event = Clock.schedule_interval(self.vision, 1.0 / 30.0)

    def vision(self,*args):
        self.timer = cv2.getTickCount()
        success, self.img = self.capture.read()
        self.img = change_dimension(self.img, self.ratio)

        success, self.bbox = self.tracker.update(self.img)

        diff = cv2.absdiff(self.frame1, self.frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if self.precious == True:
            cv2.drawContours(self.frame1, contours, -1, (0, 255, 0), 2)

        else:
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(self.frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(self.frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)


        image = cv2.resize(self.frame1, (1280,720))
        self.out.write(image)

        print(self.bbox)
        if success:
            drawBox(self.frame1, self.bbox)
            file = filehandler.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), "datum.txt"))
            file.write(str(self.bbox))
        else:
            cv2.putText(self.frame1, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        fps = cv2.getTickFrequency() / cv2.getTickCount() - self.timer
        cv2.putText(self.frame1, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        if self.external == True:
            cv2.imshow("feed", self.frame1)
        else:
            self.get_image = self.frame1

        self.frame1 = self.frame2
        ret, self.frame2 = self.capture.read()
        self.frame2 = change_dimension(self.frame2, self.ratio)

        # if self.external == True:
        #     if cv2.waitKey(40) == 27:
        #         break

        buffer = cv2.flip(self.get_image, 0).tostring()
        texture = Texture.create(size=(self.frame1.shape[1], self.frame1.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


        # if self.external == True:
        #     cv2.destroyAllWindows()
        #     self.capture.release()
        #     self.out.release()


    def save_picture(self):
        dir_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Storager")
        if not os.path.exists(dir_):
            os.mkdir(dir_)
        dir_ = os.path.join(dir_, "Images")
        if not os.path.exists(dir_):
            os.mkdir(dir_)

        img_name = os.path.join(dir_, f"{str(time.time()).replace('.', '')}.png")
        cv2.imwrite(img_name, self.image_frame)

    @property
    def camera_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate

    def close(self):
        self.event.cancel()
        if self.data in [0, 2] and (self.operation == "camera" or self.operation == "vision"):
            self.capture.release()


    def video_record(self, filename= f"{str(time.time()).replace('.', '')}.avi"):
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        self.size = (self.frame_width, self.frame_height)
        self.video_hex_file = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, self.size)
        self.recording_started =True

    def stop_recording(self):
        self.video_hex_file.release()
        self.recording_started =True

    def Camera(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        if self.recording_started == True:
            self.video_hex_file.write(frame)

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


    # Testing Version: Not Confirmed
    def Mobile_Camera_Image(self, *args):
        while True: # Finaly found working secret
            db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
            db = database.Database(db_path)
            data = db.table_data("system")
            url = data[4][2]

            img_resp = requests.get(url)
            img_np = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_np, -1)
            self.image_frame = frame
            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    # Testing Version: Not Confirmed
    def Mobile_Camera_Video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def Saved_Mobile_Image(self, *args):
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        db = database.Database(db_path)
        data = db.table_data("system")
        url = data[4][2]

        img_resp = requests.get(url)
        img_np = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)
        cv2.imwrite("Img_0.png", frame)

        frame = cv2.imread("Img_0.png")

        self.image_frame = frame
        if self.recording_started == True:
            self.video_hex_file.write(frame)

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    # Testing Version: Not Completed
    def Video(self, *args):
        capture = cv2.VideoCapture(self.data)
        while True:
            ret, frame = capture.read()
            self.image_frame = frame
            cv2.imwrite("Img_0.png", frame)
            frame = cv2.imread("Img_0.png")

            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture


    def Image(self, *args):
        try:
            frame = cv2.imread(r"{}".format(self.data))
            self.image_frame = frame

            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

        except:
            print("There is no file which you gave me.")
    


def connection_status():
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    data = db.table_data("system")
    url = data[4][2]
    try:
        img_resp = requests.get(url)
        return True

    except:
        return False
