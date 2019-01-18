
# **Object Detection and Tracking**

### Objective
To detect vehicles and track them automatically.

#### Algorithm

For object detection, yolo v3 was used. The bounding boxes of the top 4 detections
(high probability) by yolo are taken as points to be tracked. The object detection takes place
every 5 frame till we get at least one vehicle detection. For each object detected, a new tracker
is initialised and the object is tracked every frame. If the updated coordinates of the tracked
object goes out of the frame, then tracking is stopped for that particular object.

#### Dependencies & my environment


* Python2.7
* CUDA 9.0 
* GPU - 1050 GTX
* OpenCV 3.0, Numpy, dlib

#### How to compile and run the code

(1) Run the following script
```sh
git clone https://github.com/pjreddie/darknet
```
(2) darknet​ folder will be created. Copy the files ​ image.c​ , ​ image.h​ from
detection_object_tracking​ folder and place them inside s
rc​ folder which is inside the ​ darknet
folder. Delete these two files which are already there in the src folder.

(3) In the Makefile which is inside ​ detection_object_tracking​ folder, make GPU = 1 if you
have GPU. Copy this Makefile and place them inside the ​ darknet​ folder. Delete the Makefile
which is already there in the darknet folder.

(4) Go inside the darknet folder and run the script
```sh
make
```

(5) Copy the ​ libdarknet.so​ file generated in the ​ darknet​ folder and place them inside detection_object_tracking​ folder.

(6) Download the weight file from ​[here](https://drive.google.com/file/d/1W91Gg67AJmuk-okrcskVGtD9iOgHczNV/view?usp=sharing)​ and place them inside ​ detection_object_tracking folder.

(7) Run the script
```sh
python multiple_object_tracking.py -v input_videos/los_angeles.mp4 -l
```

(8) The output video will be saved in the ​ output_videos​ folder in the name ​ result.mp4.
