import sys
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
import ipdb
#ipdb.set_trace()
paths = ['Aloe','Baby1','Baby2','Baby3','Bowling1','Bowling2','Cloth1','Cloth2','Cloth3','Cloth4','Flowerpots','Lampshade1','Lampshade2','Midd1','Midd2','Monopoly','Plastic','Rocks1','Rocks2','Wood1','Wood2']

errors = np.empty([len(paths)])
index  = 0

if len(sys.argv) < 2:
  print('Usage:\n python stereo.py <input_data_vers_number>')
  quit()

in_version = int(sys.argv[1])

inputpath = '/datasets/middlebury-stereo/v'+str(in_version)+'/'
truthpath = '/datasets/middlebury-stereo/groundtruth/'


for name in paths:
    #pathname = 'data/'+name+'/'
    input_img_path = inputpath+name+'/'
    truth_img_path = truthpath+name+'/'

    #load images and ground truth
    imgL = cv2.imread(input_img_path+'view1.png')
    imgR = cv2.imread(input_img_path+'view5.png')
    imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)
    
    true_disp = cv2.imread(truth_img_path+'disp1.png',0)
    
    #parameters for algorithm 
    # Used this reference: http://docs.opencv.org/java/2.4.9/org/opencv/calib3d/StereoSGBM.html
    window_size = 7
    min_disp = 0
    num_disp = 256 
    P1 = 8*3*window_size*window_size
    P2 = 32*3*window_size*window_size

    #Calculate Disparity map from rectified stereo images
    stereo = cv2.StereoSGBM(minDisparity = min_disp, numDisparities = num_disp, SADWindowSize = window_size,P1=P1,P2=P2)

    print('computing disparity for '+name)
    disp = stereo.compute(imgL, imgR).astype(np.float32)
    disp /= 16 #scaling factor noted in the StereoSGBM documentation to perform
    disp = disp.astype(np.uint8) #convert to integers
    
    # plotting results (useful for visualization)
#    f,axarr = plt.subplots(1,2)
#    axarr[0].imshow(disp,vmin=0,vmax=255)
#    axarr[1].imshow(true_disp,vmin=0,vmax=255)
#    plt.show()
    
    error = ((disp-true_disp)**2).mean()
    errors[index] = error
    index = index + 1 
    print error

mean_error = np.mean(errors, dtype=np.float32)
print('mean error: '+str(mean_error))
