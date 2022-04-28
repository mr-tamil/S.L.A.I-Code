import datetime
import os.path
import time

import numpy

import VisionEngine
import file_helper
import filehandler
import slaiCode
from SpREngine import TextFromRAFile
from SpEngine import SpeakText
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior, CircularElevationBehavior, FocusBehavior
from kivymd.uix.textfield import MDTextField

# UIX Color
chat_input_color = 225 / 256, 224 / 256, 230 / 256, 1
chat_input_focus_color = 160 / 256, 158 / 256, 255 / 256, 1
microphone_on_unfocus_color = 255 / 256, 184 / 256, 187 / 256, 1
microphone_unfocus_color = (246 / 256, 245 / 256, 256 / 256, 1)
microphone_focus_color = (0, 0, 1, 1)
input_text_color_normal = (0, 0, 0, 1)
input_text_color_focus = (0, 0, 1, 1)
animation_icon_color_1 = (105 / 256, 108 / 256, 240 / 256, 1)
animation_icon_color_2 = (52 / 256, 55 / 256, 247 / 256, 1)
animation_icon_color_3 = (0, 4 / 256, 1, 1)

kv = """

<SubScreen>
    elevation: 5
    radius: 10
    shadow_pos: -4, -4


MDBoxLayout:
    orientation: "vertical"

    MDBoxLayout:
        padding: 10
        spacing: 10
        id: screen

        SubScreen:
            id: vision_box_id
            md_bg_color: 8/256, 44/256, 108/256,1

        SubScreen:
            id: chat_box
            spacing: 1
            orientation: "vertical"
            md_bg_color: 232/256, 232/256, 1,1

            ScrollView:
                effect_cls: "ScrollEffect"
                MDGridLayout:
                    spacing: 15
                    padding: 10
                    adaptive_height: True
                    cols: 1
                    id: chatting
            
    MDBoxLayout:
        size_hint_y: None
        height: "80dp"

        BoxLayout:
            id: aiui
        MDBoxLayout:
            adaptive_width: True
            MDBoxLayout:
                adaptive_width: True
                id: animation
            
        MDBoxLayout:
            id: keyboard_open_id
            MDBoxLayout:
                size_hint_x: None
                width: "30dp"
            
"""


class SubScreen(RoundedRectangularElevationBehavior, MDBoxLayout):
    pass


class Chat(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adaptive_height = True


class ChatBoxConnection:
    def __init__(self, instance):
        self.chat_box = instance

    def send(self, msg):
        self.chat_box.add_widget(Chat(text=msg, halign='right', theme_text_color="Primary"))

    def receive(self, msg):
        self.chat_box.add_widget(Chat(text=msg, halign='left', theme_text_color="Primary"))

    def info(self, info):
        self.chat_box.add_widget(Chat(text=info, halign='center', theme_text_color="Secondary"))


class ChatInput(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 10
        self.adaptive_height = True
        self.md_bg_color = chat_input_color
        self.spacing = 5
        self.padding = (5, 0, 5, 0)


# this is for animation of the app mic button
# class Animate_Icon(MDIconButton):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
#         self.theme_icon_color = "Custom"


class ChatBoxIcon(MDIconButton, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.theme_icon_color = "Custom"
        self.focus_color = chat_input_focus_color
        self.unfocus_color = chat_input_color
        self.md_bg_color = chat_input_color


class Microphone_Icon(CircularElevationBehavior, MDIconButton, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.theme_icon_color = "Custom"
        self.elevation = 5
        self.focus_color = microphone_focus_color
        self.unfocus_color = microphone_unfocus_color
        self.md_bg_color = microphone_unfocus_color
        self.shadow_pos = (-4, -4)


class Microphone_Icon_Close(CircularElevationBehavior, MDIconButton, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.theme_icon_color = "Custom"
        self.elevation = 5
        self.focus_color = microphone_on_unfocus_color
        self.unfocus_color = microphone_unfocus_color
        self.md_bg_color = microphone_unfocus_color
        self.shadow_pos = (-4, -4)


class SLAI_Controller:
    def __init__(self, instances):
        self.speech_engine_work = True
        self.code_ = None
        self.arduino_status = False
        self.drone = None
        self.chat_input_text = None
        self.app = instances
        self.ai_status = False
        self.ai_code_connect = None
        # self.activate(32)  # Todo: Remove after

    def connect_arduino(self):
        if not self.arduino_status:
            self.drone = file_helper.Arduino_Control()
            self.arduino_status = True

    def disconnect_arduino(self):
        if self.arduino_status:
            self.drone.close()
            self.arduino_status = False

    def slai(self, state):
        if state == "activate":
            if not self.ai_status:
                self.ai_code_connect = file_helper.SlaiCodeConnector()
                self.ai_code_connect.add_instances(self)
                self.ai_code_connect.start()
                self.app.root.ids.aiui.add_widget(self.ai_code_connect)
                self.ai_status = True
        else:
            if self.ai_status:
                self.app.root.ids.aiui.remove_widget(self.ai_code_connect)
                self.ai_code_connect.end()
                self.ai_status = False

    def activate(self, value, data=None):
        # open keyboard
        if value == 0:
            self.app.keyboard_open()

        # close keyboard
        if value == 1:
            self.app.keyboard_close()

        # system camera open or close
        if value == 2:
            self.app.info_box("camera", 0)

        # ip camera open or close method 1
        if value == 3:
            self.app.info_box("camera", 1)

        # ip camera open or close method 2
        if value == 4:
            self.app.info_box("camera", 2)

        # ip camera open or close method 3
        if value == 5:
            self.app.info_box("camera", 3)

        # activate or de-activate system camera vision
        if value == 6:
            self.app.info_box("vision", 0)

        # activate or de-activate ip camera vision
        if value == 7:
            self.app.info_box("vision", 1)

        # adding image into vision
        if value == 8:
            self.app.info_box("image", data)

        # remove info box info
        if value == 9:
            self.app.remove_info_box()

        # stop camera
        if value == 10:
            self.app.stop_camera(True)

        # save image of info box
        if value == 11:
            self.app.save_image()

        # activating the speech engine
        if value == 12:
            # self.app.animate_voice()  # this line is for animation of the app button
            if self.speech_engine_work:
                SpeakText(data)
            # self.app.end()  # this line is for animation of the app button

        # turn on microphone
        if value == 13:
            self.app.microphone_on_press()

        # Drone Controller Unit (14 - 29)
        if value == 14:
            self.drone.up.write(1)
            print("Drone---UP-1")
        if value == 15:
            self.drone.up.write(0)
            print("Drone---UP-0")

        if value == 16:
            self.drone.down.write(1)
            print("Drone---DOWN-1")

        if value == 17:
            self.drone.down.write(0)
            print("Drone---DOWN-0")

        if value == 18:
            self.drone.left.write(1)
            print("Drone---LEFT-1")

        if value == 19:
            self.drone.left.write(0)
            print("Drone---LEFT-0")

        if value == 20:
            self.drone.right.write(1)
            print("Drone---RIGHT-1")

        if value == 21:
            self.drone.right.write(0)
            print("Drone---RIGHT-0")

        if value == 22:
            self.drone.front.write(1)
            print("Drone---FRONT-1")

        if value == 23:
            self.drone.front.write(0)
            print("Drone---FRONT-0")

        if value == 24:
            self.drone.back.write(1)
            print("Drone---BACK-1")

        if value == 25:
            self.drone.back.write(0)
            print("Drone---BACK-0")

        if value == 26:
            self.drone.emergency.write(1)

        if value == 27:
            self.drone.emergency.write(0)

        # drone controller power on
        if value == 28:
            self.drone.power.write(1)

        # drone controller power off
        if value == 29:
            self.drone.power.write(0)

        # connect the connection of the arduino
        if value == 30:
            self.connect_arduino()

        # disconnect the connection of the arduino
        if value == 31:
            self.disconnect_arduino()

        # activate s.l.a.i code
        if value == 32:
            self.slai("activate")

        # deactivate s.l.a.i code
        if value == 33:
            self.slai("deactivate")

        # activating dark mode of the application
        if value == 34:
            self.app.theme_cls.theme_style = "Dark"

        # activating light mode of the application
        if value == 35:
            self.app.theme_cls.theme_style = "Light"

        # s.l.a.i code to access send message button in chat box
        if value == 36:
            self.app.chat_box.send(data)

        # s.l.a.i code to reply in chat box
        if value == 37:
            self.app.chat_box.receive(data)
        # show info into info box as the picture format

        # s.l.a.i code to manage info of the chat box
        if value == 38:
            self.app.chat_box.info(data)

        # start recording vision data
        if value == 39:
            if self.app.vision_box_status:
                self.app.vision_box.video_record()

        # stop recording vision data
        if value == 40:
            if not self.app.vision_box_status:
                self.app.vision_box.stop_recording()

    def get(self, data):
        if data == "audio":
            try:
                dir_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audio.wav")
                text = TextFromRAFile(dir_)
                self.app.chat_box.send(text)
                self.app.microphone_on_end()

                if data.lower() == "code-s":
                    self.activate(32)

                if data.lower() == "code-q":
                    self.activate(33)

            except:
                # text = "System: No internet for using Speech Recognition Engine"
                self.app.chat_box.receive("No internet for using Speech Recognition Engine")
                self.activate(12, "No internet for using Speech Recognition Engine")
            try:
                if text not in ["code-s", "code-q"]:
                    self.chat_input_text = text
            except:
                pass
        if data == "text":
            self.code_ = self.app.chat_input_text
            if self.code_.lower() == "code-s":
                self.activate(32)

            if self.code_.lower() == "code-q":
                self.activate(33)

            if self.code_ not in ["code-s", "code-q"]:
                self.chat_input_text = self.code_


class UIISApp(MDApp):
    # pre_value = 1
    # values = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard_status = False
        self.vision_box_status = False
        self.started = False
        self.model = None
        self.chat_box = None
        self.data = None
        self.vision_box = None
        self.text_input = None
        self.keyboard_open_button = None
        self.chat_input_text = None
        self.chat_input = None
        self.keyboard_close_button = None
        self.microphone = None
        self.slai = None
        self.microphone = None
        self.keyboard_close_button = None

    def build(self):
        Window.size = (800, 500)
        return Builder.load_string(kv)

    def on_start(self):
        dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "researchFile.json")
        self.research_file = filehandler.FileHandler(dir__)
        self.started_uiis = time.time()

        self.slai = SLAI_Controller(self)

        self.microphone = Microphone_Icon(icon="microphone", icon_size="40dp", on_press=self.microphone_on_press)
        # self.microphone_close = Microphone_Icon_Close(icon= "record-circle", icon_size= "40dp",
        # on_press= self.microphone_on_end, icon_color=(1,0,0,1))
        self.keyboard_open_button = Microphone_Icon(icon="keyboard", on_release=self.keyboard_open)

        self.keyboard_close_button = ChatBoxIcon(icon="keyboard-close", on_release=self.keyboard_close,
                                                 pos_hint={"center_x": 0.5, "center_y": 0.5}, height="30dp")

        self.text_input = MDTextField(multiline=False, active_line=False, height="30dp",
                                      text_color_normal=input_text_color_normal,
                                      text_color_focus=input_text_color_focus,
                                      on_text_validate=self.text_field)

        self.send_icon = ChatBoxIcon(icon="send", pos_hint={"center_x": 0.5, "center_y": 0.5}, height="30dp",
                                     on_release=self.text_field)
        self.chat_input = ChatInput()

        self.chat_input.add_widget(self.keyboard_close_button)
        self.chat_input.add_widget(self.text_input)

        self.chat_input.add_widget(self.send_icon)

        self.root.ids.animation.add_widget(self.microphone)
        self.root.ids.keyboard_open_id.add_widget(self.keyboard_open_button)

        self.chat_box = ChatBoxConnection(self.root.ids.chatting)
        self.chat_box.info(str(datetime.datetime.today().strftime("%I %M %p, %b %d")))
        self.chat_box.receive("Welcome to UIIS!")

    # below lines is for animation of the app button
    # Not in use        
    # def animate_voice(self, *args):
    #     ""---
    #     Icon_1 = Animate_Icon(icon= "record", icon_size = "33dp", icon_color= animation_icon_color_1, on_press= self.end)
    #     Icon_2 = Animate_Icon(icon= "record-circle", icon_size = "65dp", icon_color= animation_icon_color_2, on_press= self.end)
    #     Icon_3 = Animate_Icon(icon= "record-circle-outline", icon_size = "65dp", icon_color= animation_icon_color_3, on_press= self.end)
    #     self.values = (Icon_1, Icon_2, Icon_3)
    #     ""---

    #     Icon_1 = Animate_Icon(icon= "record-circle", icon_size = "33dp", icon_color= animation_icon_color_1, on_press= self.end)
    #     Icon_2 = Animate_Icon(icon= "access-point", icon_size = "65dp", icon_color= animation_icon_color_2, on_press= self.end)
    #     self.values = (Icon_1, Icon_2)

    #     self.root.ids.animation.remove_widget(self.microphone)
    #     self.root.ids.keyboard_open_id.remove_widget(self.keyboard_open_button)

    #     self.pre_value = 0
    #     self.root.ids.animation.add_widget(self.values[self.pre_value])

    #     Clock.schedule_interval(self.start, 0.5)

    # def end(self, *args):
    # Clock.unschedule(self.start)
    # self.root.ids.animation.remove_widget(self.values[self.pre_value])
    # self.root.ids.animation.add_widget(self.microphone)
    # if not self.keyboard_status:
    #     self.root.ids.keyboard_open_id.add_widget(self.keyboard_open_button)

    def on_stop(self):
        stopped = time.time() -self.started_uiis
        # self.research_file.append({"opened": self.research_file.read()[""] + 1})
        runtime = self.research_file.read()

        dict__ = runtime["runtime"]
        dict_ = numpy.array(dict__)

        try:
            if str(datetime.date.today()) not in dict_[:, 0]:
                dict__.append([str(datetime.date.today()), stopped])
                self.research_file.append({"runtime": dict__})
            else:
                last = dict__[-1][1]
                del dict__[-1]
                dict__.append([str(datetime.date.today()), last + stopped])
                self.research_file.append({"runtime": dict__})
        except:
            dict__.append([str(datetime.date.today()), stopped])
            self.research_file.append({"runtime": dict__})



    def microphone_on_press(self, *args):
        # Some problem
        # self.root.ids.animation.remove_widget(self.microphone)
        # self.root.ids.animation.add_widget(self.microphone_close)

        self.root.ids.keyboard_open_id.remove_widget(self.keyboard_open_button)
        self.slai.get("audio")

    def microphone_on_end(self):
        # Some problem
        # self.root.ids.animation.remove_widget(self.microphone_close)
        # self.root.ids.animation.add_widget(self.microphone)
        if not self.keyboard_status:
            self.root.ids.keyboard_open_id.add_widget(self.keyboard_open_button)

    # below lines is for animation of the app button
    # def start(self,*args):
    # self.root.ids.animation.remove_widget(self.values[self.pre_value])
    # """
    # if self.pre_value == 0:
    #     self.pre_value = 1
    #
    # elif self.pre_value == 1:
    #     self.pre_value = 2
    #
    # elif self.pre_value == 2:
    #     self.pre_value = 0
    # """
    # if self.pre_value == 0:
    #     self.pre_value = 1
    #
    # elif self.pre_value == 1:
    #     self.pre_value = 0
    #
    # self.root.ids.animation.add_widget(self.values[self.pre_value])

    def keyboard_open(self, *args):
        if not self.keyboard_status:
            self.root.ids.chat_box.add_widget(self.chat_input)
            self.root.ids.keyboard_open_id.remove_widget(self.keyboard_open_button)
            self.keyboard_status = True

    def keyboard_close(self, *args):
        if self.keyboard_status:
            self.root.ids.chat_box.remove_widget(self.chat_input)
            self.root.ids.keyboard_open_id.add_widget(self.keyboard_open_button)
            self.keyboard_status = False

            self.text_input.show_keyboard = True

    def text_field(self, *args):
        if self.text_input.text != "":
            # print(self.text_input.text) # Testing
            self.chat_input_text = self.text_input.text
            self.text_input.text = ""
            self.chat_send()
        self.text_input.focus = True

    def info_box(self, model, data):
        self.remove_info_box()

        if model == "camera":
            self.vision_box = file_helper.Vision()
            if data != 0:
                connection_status = file_helper.connection_status()
                if connection_status:
                    self.vision_box.set_operation("camera", data)
                    self.root.ids.vision_box_id.add_widget(self.vision_box)
                    self.vision_box_status = True
                    self.model = model
                    self.data = data
                else:
                    print("Not Connected to Server.")
            else:
                self.vision_box.set_operation("camera", data)
                self.root.ids.vision_box_id.add_widget(self.vision_box)
                self.vision_box_status = True
                self.model = model
                self.data = data

        if model == "image":
            self.vision_box = file_helper.Vision()

            self.vision_box.set_operation("image", data)
            self.root.ids.vision_box_id.add_widget(self.vision_box)
            self.vision_box_status = True
            self.model = model
            self.data = data

        if model == "vision":
            self.vision_box = file_helper.Vision()
            if data != 0:
                connection_status = file_helper.connection_status()
                if connection_status:
                    self.vision_box.set_operation("vision", data)
                    self.root.ids.vision_box_id.add_widget(self.vision_box)
                    self.vision_box_status = True
                    self.model = model
                    self.data = data
                else:
                    print("Not Connected to Server.")
            else:
                self.vision_box.set_operation("vision", data)
                self.root.ids.vision_box_id.add_widget(self.vision_box)
                self.vision_box_status = True
                self.model = model
                self.data = data

    def remove_info_box(self):
        if self.vision_box_status:
            self.root.ids.vision_box_id.remove_widget(self.vision_box)
            if (self.model == 'camera' or self.model == "vision") and self.data == 0:
                self.stop_camera()

            self.vision_box_status = False

    def stop_camera(self, ai_control=False):
        if not ai_control:
            self.vision_box.close()

        else:
            self.info_box(None, None)

    def save_image(self):
        try:
            self.vision_box.save_picture()
        except:
            print("Camera is not enabled.")

    def chat_send(self):
        self.chat_box.send(self.chat_input_text)
        self.slai.get("text")


UIISApp().run()
