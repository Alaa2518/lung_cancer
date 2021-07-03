import pydicom
import numpy as np
import cv2
import os
import skimage.morphology as morphology
import scipy.ndimage as ndimage
from skimage.measure import label, regionprops, perimeter
from scipy import ndimage as ndi
from skimage.segmentation import clear_border
from skimage.filters import roberts, sobel
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing


CT_OFFSET = 1024
ZERO_VALUE = -2000


class Read_all():
    def transform_to_hu(medical_image, image):
        intercept = medical_image.RescaleIntercept if 'RescaleIntercept' in medical_image else -1024
        slope = medical_image.RescaleSlope if 'RescaleSlope' in medical_image else 1
        hu_image = image * slope + intercept
        return hu_image


    def window_image(image, window_center, window_width):
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        window_image = image.copy()
        window_image[window_image < img_min] = img_min
        window_image[window_image > img_max] = img_max

        return window_image


    def crop_image(image, display=False):
        # Create a mask with the background pixels
        mask = image == 0
        # Find the brain area
        coords = np.array(np.nonzero(~mask))
        top_left = np.min(coords, axis=1)
        bottom_right = np.max(coords, axis=1)
        # Remove the background
        croped_image = image[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]]
        return croped_image


    def add_pad(image, new_height=512, new_width=512):
        height, width = image.shape

        final_image = np.zeros((new_height, new_width))

        pad_left = int((new_width - width) / 2)
        pad_top = int((new_height - height) / 2)

        # Replace the pixels with the image's pixels
        final_image[pad_top:pad_top + height, pad_left:pad_left + width] = image
        
        return final_image


    def remove_noise(file_path, display=False):
        medical_image = pydicom.read_file(file_path)
        image = medical_image.pixel_array
        #image = color.rgb2gray(image[50:-50, 50:-50])

        hu_image = transform_to_hu(medical_image, image)
        brain_image = window_image(hu_image, -600, 1000)

        # morphology.dilation creates a segmentation of the image
        # If one pixel is between the origin and the edge of a square of size
        # 5x5, the pixel belongs to the same class

        # We can instead use a circule using: morphology.disk(2)
        # In this case the pixel belongs to the same class if it's between the origin
        # and the radius

        segmentation = morphology.dilation(brain_image, np.ones((5, 5)))
        labels, label_nb = ndimage.label(segmentation)

        label_count = np.bincount(labels.ravel().astype(np.int))
        # The size of label_count is the number of classes/segmentations found

        # We don't use the first class since it's the background
        label_count[0] = 0

        # We create a mask with the class with more pixels
        # In this case should be the brain
        mask = labels == label_count.argmax()

        # Improve the brain mask
        mask = morphology.dilation(mask, np.ones((5, 5)))
        mask = ndimage.morphology.binary_fill_holes(mask)
        mask = morphology.dilation(mask, np.ones((3, 3)))

        # Since the the pixels in the mask are zero's and one's
        # We can multiple the original image to only keep the brain region
        masked_image = mask * brain_image

        
        return masked_image


    def get_segmented_lungs(in_im, plot=False):
        im = in_im.copy()  # don't change the input
        
        '''
        Step 1: Convert into a binary image. 
        '''
        binary = im < -400
        
        '''
        Step 2: Remove the blobs connected to the border of the image.
        '''
        cleared = clear_border(binary)
        
        '''
        Step 3: Label the image.
        '''
        label_image = label(cleared)
        
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
        
        '''
        Step 5: Erosion operation with a disk of radius 2. This operation is seperate the lung nodules attached to the blood vessels.
        '''
        selem = disk(2)
        binary = binary_erosion(binary, selem)
        
        '''
        Step 6: Closure operation with a disk of radius 10. This operation is to keep nodules attached to the lung wall.
        '''
        selem = disk(10)
        binary = binary_closing(binary, selem)
        
        '''
        Step 7: Fill in the small holes inside the binary mask of lungs.
        '''
        edges = roberts(binary)
        binary = ndi.binary_fill_holes(edges)
        
        '''
        Step 8: Superimpose the binary mask on the input image.
        '''
        get_high_vals = (binary == 0)
        im[get_high_vals] = ZERO_VALUE  # minimum value
        
        return im


    def ReadAll(Path):
        photoAfterRemoveNoise = remove_noise(Path, False)
        photoAfterCropped = crop_image(photoAfterRemoveNoise, False)  # no Impact
        photoAfterpadding = add_pad(photoAfterCropped, 512, 512)  # no Impact
        SegmentedImage = get_segmented_lungs(photoAfterpadding, False)
        
        return SegmentedImage




