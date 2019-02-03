import os
import matplotlib.pyplot as plt
import cv2
import argparse
from matplotlib.widgets import RectangleSelector
from write_to_XML import write_xml
import shutil
from datetime import datetime
#Author: Mark Jay

img = None
tl_list = []
br_list = []
object_list = []
annotated_dir = "annotated_images"
#constants

image_folder = ""
savedir = "annotations"
obj = "scorpion"

def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)
     
def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == "q":
        fd = open("progress.log", "a")
        fd.write(str(datetime.today()) + " " +  img.name + " completed\n")
        if not os.path.isdir(annotated_dir):
            os.mkdir(annotated_dir)
        print(img.path)
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)      
        tl_list = []
        br_list = []
        object_list = []
        shutil.move(img.path, annotated_dir)
        img = None
        fd.close()
        plt.close()
    elif event.key == "r":
        fd = open("img_for_revision.txt", "a")
        fd.write(str(datetime.today()) + " " + img.name + "\n")
        tl_list = []
        br_list = []
        object_list = []
        img = None
        fd.close()
        plt.close()
        
def toggle_selector(event):
    toggle_selector.RS.set_active(True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--imagedir", required=True, help="path to images")
    args = vars(ap.parse_args())
    image_folder = args["imagedir"]
    num_imgs = (len(list(os.scandir(image_folder))))
    for n, image_file in enumerate(os.scandir(image_folder)):
        cnt = n + 1
        print(cnt, " images out of ", num_imgs)
        img = image_file
        fig, ax = plt.subplots(1)
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        toggle_selector.RS = RectangleSelector(ax, line_select_callback, drawtype = "box", useblit = True, button = [1], minspanx = 5
                                               , minspany = 5, spancoords = "pixels", interactive = True)
        bbox = plt.connect("key_press_event", toggle_selector)
        key = plt.connect("key_press_event", onkeypress)
        plt.show()
