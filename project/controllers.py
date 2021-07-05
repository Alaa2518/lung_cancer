import pickle
import pydicom
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import skimage.morphology as morphology
import scipy.ndimage as ndimage
import pandas as pd  # reading and processing of tables
import skimage
import os
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.measure import label, regionprops, perimeter
from skimage.morphology import binary_dilation, binary_opening
from skimage.filters import roberts, sobel
from skimage import measure, feature
from skimage.segmentation import clear_border
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.misc
CT_OFFSET = 1024
ZERO_VALUE = -2000

CT_OFFSET = 1024
ZERO_VALUE = -2000


class preprocessing():
    def transform_to_hu(self,medical_image, image):
        intercept = medical_image.RescaleIntercept  if 'RescaleIntercept' in medical_image else -1024
        slope = medical_image.RescaleSlope if 'RescaleSlope' in medical_image else 1
        hu_image = image * slope + intercept

        return hu_image

    def window_image(self,image, window_center, window_width):
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        window_image = image.copy()
        window_image[window_image < img_min] = img_min
        window_image[window_image > img_max] = img_max
        
        return window_image

    def FixImages(self,file_path, display=False):
        medical_image = pydicom.read_file(file_path)
        image = medical_image.pixel_array
        hu_image = self.transform_to_hu(file_path, image)
        lung_image = self.window_image(hu_image, -600, 1500)  # best based on experience
        return lung_image

    def PreProcessedAndSegment(self,in_im, plot=False):
        im = in_im.copy()  # don't change the input
        '''
        This funtion segments the lungs from the given 2D slice.
        '''
        if plot == True:
            f, plots = plt.subplots(3, 3, figsize=(10, 10))
            plots = plots.flatten()

        if plot == True:
            plots[0].axis('off')
            plots[0].imshow(in_im, cmap='gray')
            plots[0].set_title('Orginal Image: ')
        '''
        Step 1: Convert into a binary image. 
        '''
        binary = im < -400
        if plot == True:
            plots[1].axis('off')
            plots[1].imshow(binary, cmap=plt.cm.bone)
            plots[1].set_title('First Threshold')
        '''
        Step 2: Remove the blobs connected to the border of the image.
        '''
        cleared = clear_border(binary)
        if plot == True:
            plots[2].axis('off')
            plots[2].imshow(cleared, cmap=plt.cm.bone)
            plots[2].set_title('Remove Border')
        '''
        Step 3: Label the image.
        '''
        label_image = label(cleared)
        if plot == True:
            plots[3].axis('off')
            plots[3].imshow(label_image, cmap=plt.cm.gist_earth)
            plots[3].set_title('Label Components')
        '''
        Step 4: Keep the labels with 2 largest areas.
        '''
        areas = [r.area for r in regionprops(label_image)]
        areas.sort()
        if len(areas) > 2:
            for region in regionprops(label_image):
                if region.area < areas[-2]:
                    for coordinates in region.coords:
                        label_image[coordinates[0], coordinates[1]] = 0
        binary = label_image > 0
        if plot == True:
            plots[4].axis('off')
            plots[4].imshow(binary, cmap=plt.cm.bone)
            plots[4].set_title('Keep Biggest 2')
        '''
        Step 5: Erosion operation with a disk of radius 2. This operation is 
        seperate the lung nodules attached to the blood vessels.
        '''
        selem = disk(2)
        binary = binary_erosion(binary, selem)
        if plot == True:
            plots[5].axis('off')
            plots[5].imshow(binary, cmap=plt.cm.bone)
            plots[5].set_title('Erosion')
        '''
        Step 6: Closure operation with a disk of radius 10. This operation is 
        to keep nodules attached to the lung wall.
        '''
        selem = disk(10)
        binary = binary_closing(binary, selem)
        if plot == True:
            plots[6].axis('off')
            plots[6].imshow(binary, cmap=plt.cm.bone)
            plots[6].set_title('Close Image')
        '''
        Step 7: Fill in the small holes inside the binary mask of lungs.
        '''
        edges = roberts(binary)
        binary = ndi.binary_fill_holes(edges)
        if plot == True:
            plots[7].axis('off')
            plots[7].imshow(binary, cmap=plt.cm.bone)
            plots[7].set_title('Fill holes')
        '''
        Step 8: Superimpose the binary mask on the input image.
        '''
        get_high_vals = (binary == 0)
        im[get_high_vals] = ZERO_VALUE  # minimum value
        if plot == True:
            plots[8].axis('off')
            plots[8].imshow(im, cmap=plt.cm.bone)
            plots[8].set_title('Binary Masked Input')

        return im
    

    loaded_model = pickle.load(open('SVM_Model.sav', 'rb'))

    def PredictImage(self,ImagePath):
        #Make All False to True to view the images of steps
        photoAfterRemoveNoise = self.FixImages(ImagePath, False)
        SegmentedImage = self.PreProcessedAndSegment(photoAfterRemoveNoise, False)
        dataset_size = len(SegmentedImage)
        test_img = SegmentedImage.reshape(1, -1)
        cat = self.loaded_model.predict(test_img)
        return cat



