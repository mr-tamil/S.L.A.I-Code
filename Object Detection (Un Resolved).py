# ------------------------------------------------------------------
# Vision Engine
# from git import Repo
# Repo.clone_from("https://github.com/tzutalin/labelImg.git", "C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code\\Data\\")


# pip install --upgrade pyqt5 lxml

import cv2
import uuid
import os
import time
from git import Repo

labels = ['thumbsup', 'thumbsdown', 'thankyou', 'livelong']
number_imgs = 5

# collect the images for training and testing the vision
def collectimages(labels, number_imgs):
    IMAGES_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'collectedimages')

    if not os.path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)

    for label in labels:
        path = os.path.join(IMAGES_PATH, label)
        if not os.path.exists(path):
            os.mkdir(path)

    for label in labels:
        cap = cv2.VideoCapture(0)
        print('Collecting images for {}'.format(label))
        time.sleep(5)
        for imgnum in range(number_imgs):
            print('Collecting image {}'.format(imgnum))
            ret, frame = cap.read()
            imgname = os.path.join(IMAGES_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
            cv2.imwrite(imgname, frame)
            cv2.imshow('frame', frame)
            time.sleep(2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()









import os
import shutil
import cv2

xml_string = """<annotation>
    <folder>{folder_name}</folder>
    <filename>{image_name}</filename>
    <path>{image_dir}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{width}</width>
        <height>{height}</height>
        <depth>{depth}</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{name}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{xmin}</xmin>
            <ymin>{ymin}</ymin>
            <xmax>{xmax}</xmax>
            <ymax>{ymax}</ymax>
        </bndbox>
    </object>
</annotation>
"""


def dimensions(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    return img.shape


def bBox(img_path, dimensions, ratio):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (dimensions[1] // ratio, dimensions[0] // ratio))
    bbox = cv2.selectROI("Tracking", img, False, False)
    return [ratio * i for i in bbox]


class LabelImg:
    def __init__(self, img_path, cwd):
        self.img_path = img_path
        self.cwd = cwd
        self.img_name = os.path.basename(img_path)

        self.workspace_folder_path = os.path.join(self.cwd, "Workspace")
        self.images_folder_path = os.path.join(self.workspace_folder_path, "Images")
        self.test_folder_path = os.path.join(self.images_folder_path, "test")
        # self.train_folder_path = os.path.join(self.images_folder_path, "train") # ToDo: UnComment
        self.train_folder_path = os.path.join(self.images_folder_path, "AllImages") # ToDo: Remove
        self.check_paths()

        # height, width, depth
        self.dimensions = dimensions(img_path)
        # xmin, ymin, amax, ymax
        self.bbox = bBox(img_path, self.dimensions, ratio=5)
        self.update_values()

    def create_xml_file(self, test=False):

        xml_file_name = os.path.join(f"{self.img_name.split('.')[0]}.xml")
        if not test:
            xml_path = os.path.join(self.train_folder_path, xml_file_name)
            final_image_path = os.path.join(self.train_folder_path, os.path.basename(self.img_path))
            self.values.update({"folder_name": "train",
                                "image_dir": final_image_path})

            self.xml_string_updated = xml_string.format(**self.values)
            with open(xml_path, 'wb') as xml_file:
                xml_file.write(self.xml_string_updated.encode())

            # shutil.copy(self.img_path, final_image_path)

        else:
            xml_path = os.path.join(self.test_folder_path, xml_file_name)
            final_image_path = os.path.join(self.test_folder_path, os.path.basename(self.img_path))
            self.values.update({"folder_name": "test",
                                "image_dir": final_image_path})

            self.xml_string_updated = xml_string.format(**self.values)
            with open(xml_path, 'wb') as xml_file:
                xml_file.write(self.xml_string_updated.encode())

            # shutil.copy(self.img_path, final_image_path)

    def update_values(self):
        self.values = {"height": self.dimensions[0],
                       "width": self.dimensions[1],
                       "depth": self.dimensions[2],
                       "xmin": self.bbox[0],
                       "ymin": self.bbox[1],
                       "xmax": self.bbox[2],
                       "ymax": self.bbox[3],
                       "image_name": self.img_name}

    def name(self, name):
        self.values.update({"name": name})

    def check_paths(self):
        if not os.path.exists(self.workspace_folder_path):
            os.mkdir(self.workspace_folder_path)

        if not os.path.exists(self.images_folder_path):
            os.mkdir(self.images_folder_path)

        if not os.path.exists(self.test_folder_path):
            os.mkdir(self.test_folder_path)

        if not os.path.exists(self.train_folder_path):
            os.mkdir(self.train_folder_path)


# # img_path = "C:\\Users\\ELCOT\\Desktop\\Img_0.png"
# img_path = 'C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code\\Documents\\IMG_20210819_141110.jpg'
# app_dir = "C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code"
#
# imlabel = LabelImg(img_path, app_dir)
#
# name = str(input("Name: "))
# imlabel.name(name)
#
# test = int(input("Test: "))
# if test == 0:
#     imlabel.create_xml_file()
# else:
#     imlabel.create_xml_file(True)



# get the label names
label_names = []

# label all the images from the given folder path
def folderLabelimg(folder_path,app_dir):
    # make globally available the label names
    global label_names
    label_names = []

    images = []
    for name in os.listdir(folder_path):
        images.append(name)
    for name in images:
        img_path = os.path.join(folder_path, name)
        imlabel = LabelImg(img_path, app_dir)

        name = str(input("Name: "))
        imlabel.name(name)
        imlabel.create_xml_file()

        if name not in label_names:
            label_names.append(name)

if __name__ == "__main__":
    folder_path = "C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code\\Tensorflow\\workspace\\images\\AllImages"
    app_dir = "C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code\\Tensorflow\\"

    folderLabelimg(folder_path, app_dir)

# -----------------------------------------------


import os
import shutil
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import cv2
import numpy as np
from matplotlib import pyplot as plt


cwd = "C:\\Users\\ELCOT\\IdeaProjects\\S.L.A.I Code"
tensorflow_folder = os.path.join(cwd, "Tensorflow")
WORKSPACE_PATH = cwd + '\\Tensorflow\\workspace'
SCRIPTS_PATH = cwd + '\\Tensorflow\\scripts'
APIMODEL_PATH = cwd + '\\Tensorflow\\models'
ANNOTATION_PATH = WORKSPACE_PATH + '\\annotations'
IMAGE_PATH = WORKSPACE_PATH + '\\images'
MODEL_PATH = WORKSPACE_PATH + '\\models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH + '\\pre-trained-models'
CONFIG_PATH = MODEL_PATH + '\\my_ssd_mobnet\\pipeline.config'
CHECKPOINT_PATH = MODEL_PATH + '\\my_ssd_mobnet\\'




# old
# labels = [{'name': 'one', 'id': 1},
#           {'name': 'two', 'id': 2},
#           {'name': 'three', 'id': 3},
#           {'name': 'four', 'id': 4}]


# new
labels = []
for i in range(len(label_names)):
    labels.append({"name": label_names[i],
                   "id": i+1})



with open(ANNOTATION_PATH + '\\label_map.pbtxt', 'w') as f:
    for label in labels:
        f.write('item { \n')
        f.write('\tname:\'{}\'\n'.format(label['name']))
        f.write('\tid:{}\n'.format(label['id']))
        f.write('}\n')


train = f"{SCRIPTS_PATH}\\generate_tfrecord.py -x {IMAGE_PATH}\\train -l {ANNOTATION_PATH}\\label_map.pbtxt -o {ANNOTATION_PATH}\\train.record"
test = f"{SCRIPTS_PATH}\\generate_tfrecord.py -x{IMAGE_PATH}\\test -l {ANNOTATION_PATH}\\label_map.pbtxt -o {ANNOTATION_PATH}\\test.record"
print(train)
print(test)



# old
# from git import Repo
# Repo.clone_from("https://github.com/tensorflow/models", tensorflow_folder+ "\\models")

# new
if not os.path.exists(os.path.join(tensorflow_folder, "models")):
    Repo.clone_from("https://github.com/tensorflow/models", tensorflow_folder+ "\\models")



CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
my_ssd_mobnet = cwd + '\\Tensorflow\\workspace\\models\\'+CUSTOM_MODEL_NAME
if not os.path.exists(my_ssd_mobnet):
    os.mkdir(my_ssd_mobnet)

shutil.copy(f"{PRETRAINED_MODEL_PATH}\\ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\\pipeline.config", f"{MODEL_PATH}\\{CUSTOM_MODEL_NAME}")



CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'
config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
print(config)


pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
with tf.io.gfile.GFile(CONFIG_PATH, "r") as f:
    proto_str = f.read()
    text_format.Merge(proto_str, pipeline_config)


pipeline_config.model.ssd.num_classes = len(label_names)
pipeline_config.train_config.batch_size = 4
pipeline_config.train_config.fine_tune_checkpoint = PRETRAINED_MODEL_PATH+'/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ckpt-0'
pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
pipeline_config.train_input_reader.label_map_path= ANNOTATION_PATH + '/label_map.pbtxt'
pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [ANNOTATION_PATH + '/train.record']
pipeline_config.eval_input_reader[0].label_map_path = ANNOTATION_PATH + '/label_map.pbtxt'
pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [ANNOTATION_PATH + '/test.record']


print("""python {}\\research\\object_detection\\model_main_tf2.py --model_dir={}\\{} --pipeline_config_path={}\\{}\\pipeline.config --num_train_steps=5000""".format(APIMODEL_PATH, MODEL_PATH,CUSTOM_MODEL_NAME,MODEL_PATH,CUSTOM_MODEL_NAME))
# os.system("""python {}\\research\\object_detection\\model_main_tf2.py --model_dir={}\\{} --pipeline_config_path={}\\{}\\pipeline.config --num_train_steps=5000""".format(APIMODEL_PATH, MODEL_PATH,CUSTOM_MODEL_NAME,MODEL_PATH,CUSTOM_MODEL_NAME))


# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-6')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections



category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')

# Setup capture
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while True:
    ret, frame = cap.read()
    image_np = np.array(frame)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes']+label_id_offset,
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=.5,
        agnostic_mode=False)

    cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break

detections = detect_fn(input_tensor)
# Vision Engine
# ------------------------------------------------------------------
