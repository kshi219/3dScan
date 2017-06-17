# 3dScan
Structured light decoder and re-constructor. "From Images to 3D Model"
### From Images of the Scene:
<img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_07.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_09.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_11.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_13.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_16.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_17.png" width="120"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/cam_19.png" width="120">
### We Construct a Point Cloud of the Scene, Recovering Depth Information (on the right is actual output from this implementation, on the left is the object we "scanned"):
<img src="https://github.com/kshi219/3dScan/blob/master/gifs/out-6.gif" width="300"><img src="https://github.com/kshi219/3dScan/blob/master/gifs/out.gif" width="520">

Given a series of structured light images (images with special light projected on them, like the one below) and projector-camera calibration, this module will produce a 3D model of the scene. Purely academic motivations/goals, implemented as to exercise computer vision and geometry concepts for machine perception after groking through some online course materials and scientific papers. Using python and numpy the code was able to express concisely the mathematics of point-cloud reconstruction from structured light images. No computer vision libraries (openCV, PIL, VTK etc) were used. Input structured-light images and calibration software were found [here](http://mesh.brown.edu/scanning/). 


This code is only concerned with reconstruction. The 2 gifs above display the resulting pointcloud next to a rotation of the scanned object. We can see a good representation of the relative depth and form of the firgure's arms, head, torso and bottom platform. Note that we only are able to discern accurate depth information for frontal regions of the figure which were consistently illuminated by the structured light. A side-on view of the point cloud's profile matches that of the actual figure.


## Further Work:
### Speed: 
this runs painfully slow, I tried not to think about speed the first time around and focus on understanding the math as I implemented, this should be improved.

### Surface Reconstruction with color: 
given the point cloud we should be able to reconstruct a 3d surface model with colors from the input images that forms a more complete representation of the scanned scene.



## Draws heavily upon the following resources:

https://fling.seas.upenn.edu/~cis580/wiki/index.php?title=Machine_Perception_CIS_580_Spring_2015

http://www.cs.cornell.edu/courses/cs5670/2017sp/

http://mesh.brown.edu/scanning/

http://mesh.brown.edu/desktop3dscan/



*skimage use restricted to image i/o
