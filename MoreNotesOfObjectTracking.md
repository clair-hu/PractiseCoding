## Salient Object Detection (Fixation Prediction)

* Salient → most noticeable or important. (https://towardsdatascience.com/cvpr-2014-paper-summary-the-secrets-of-salient-object-segmentation-9c777babdc5)

* salient object detection is a term used to segment the most important objects in the image.
* 1) detecting the most salient object and 2) segmenting the accurate
region of that object.

* Saliency, defined as
uniqueness in terms of global regional contrast,
In addition to color uniqueness, distinctiveness
of complementary cues such as texture [175] and
structure [179] is also considered for salient object
detection.

* salient object subitizing

* **Paper** [Revisiting Salient Object Detection:Simultaneous Detection, Ranking, and Subitizing of Multiple Salient Objects](chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/http://openaccess.thecvf.com/content_cvpr_2018/CameraReady/2523.pdf?source=post_page---------------------------)

* [SOD with KCF](chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://kuscholarworks.ku.edu/bitstream/handle/1808/24144/Nandi_ku_0099M_15079_DATA_1.pdf?sequence=1)

https://towardsdatascience.com/cvpr-paper-summary-revisiting-salient-object-detection-simultaneous-detection-ranking-and-b759a9226d63

-------------------------
## Auto object tracking without manually selecting bounding boxes

### Static Object Detection Based on a Dual Background Model and a Finite-State Machine (2010-2011)
https://jivp-eurasipjournals.springeropen.com/articles/10.1155/2011/858502

* **Background subtraction** is a commonly used technique for the segmentation of foreground regions in video sequences taken from a static camera, which basically consists on detecting the moving objects from the **difference** between the current frame and a background model

* In order to achieve good segmentation results, the background model must be regularly kept updated so as to adapt to the varying **lighting conditions** and to stationary changes in the scene. Therefore, background subtraction techniques often do not suffice for the detection of stationary objects and are thus supplemented by an additional approach.

* **Porikli** et al. [5]. proposed a pixelwise system which uses **dual foregrounds**. 
    * They used **two background models** with different learning rates, a short-term and a long-term background model.
    * In this way, they were able to control how fast static objects get absorbed by the background models and detect them as those groups of pixels classified as background by the short-term but not by the long-term background model.



## More materials to cover
https://cv-tricks.com/object-detection/faster-r-cnn-yolo-ssd/
https://cv-tricks.com/object-tracking/quick-guide-mdnet-goturn-rolo/
https://cv-tricks.com/object-tracking/quick-guide-mdnet-goturn-rolo/
https://www.semanticscholar.org/paper/Object-tracking-initialization-using-automatic-Ng-Delp/e684eb040657a0ee861176d051d8a426c7b4a05a
chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/http://jardcs.org/papers/v10/i201858.pdf
https://www.researchgate.net/publication/313895318_A_Static_Object_Detection_in_Image_Sequences
chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://pdfs.semanticscholar.org/392e/226b5afa9747e0da5e4638b1b8bd804ca161.pdf