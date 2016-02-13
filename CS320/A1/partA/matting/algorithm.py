## CSC320 Winter 2016 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
from matplotlib import pyplot as plt
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = { 
            'backA': None, 
            'backB': None, 
            'compA': None, 
            'compB': None, 
            'colOut': None,
            'alphaOut': None, 
            'backIn': None, 
            'colIn': None, 
            'alphaIn': None, 
            'compOut': None, 
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self): 
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }

    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()



    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################
            
    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        
        if fileName == None:
            return success, msg
        image = cv.imread(fileName)
        self._images[key] = image
        success = True
        msg = 'success'
        
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        
        if fileName == None:
            return success, msg
        image = self._images[key]
        cv.imwrite(fileName, image)
        success = True
        msg = 'success'

        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. return two images: color and greyscale
    def triangulationMatting(self):
        """
success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'
        
        if (self._images['backA'] is None) or (self._images['backB'] is None) or (self._images['compA'] is None) or (self._images['compB'] is None):
            return success, msg

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        backA = (self._images['backA']).astype('int64')
        backB = (self._images['backB']).astype('int64')
        compA = (self._images['compA']).astype('int64')
        compB = (self._images['compB']).astype('int64')
        
        height, width = backA.shape[0:2] #shape of the image
        result = np.empty((height, width, 4))   #array to hold result RGBa values

        background = np.reshape(
                np.concatenate((backA, backB), 2),
                (height, width, 6, 1))
        background = -background    #negative background colors

        #left side of equation. Matrix with the delta values
        delta = np.reshape(
                np.concatenate((compA - backA, compB - backB), 2),
                (height, width, 6, 1))

        matrix = np.tile(np.identity(3), (2, 1))     
        many_matrices = np.tile(matrix, (height, width, 1, 1)) 
        A = np.concatenate((many_matrices, background), axis = 3)   #right side of equation
        Apinv = np.empty((height, width, 4, 6)) #empty matrix to store A after psuedo-inverse

        for y, x in np.ndindex(backA.shape[0], backA.shape[1]):
            Apinv[y, x] = np.linalg.pinv(A[y, x])   #psuedo-inverse
            result[y, x] = np.reshape(
                        np.dot(Apinv[y, x], delta[y, x]), (4))  #dot product to get RGBa in vector form

        alphaOut = np.clip(result[:,:,3], 0.0, 1.0) * 255.0;    #alpha values in matrix
        colOut = np.clip(result[:,:,0:3], 0.0, 255.0)   #RGB values in matrix

        #########################################

        self._images['alphaOut'] = alphaOut
        self._images['colOut'] = colOut

        success = True
        msg = 'success'
        return success, msg


    def createComposite(self):
        """
success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        
        #composite_img = background_img * (1 - alpha) + foreground_img
        success = False
        msg = 'Placeholder'

        if (self._images['colIn'] is None) or (self._images['alphaIn'] is None) or (self._images['colIn'] is None):
            return success, msg

        backIn = self._images['backIn'].astype('int64')/255.0
        colIn = self._images['colIn'].astype('int64')/255.0
        alphaIn = self._images['alphaIn'].astype('int64')/255.0    
        
        compOut = backIn * (1.0 - alphaIn) + colIn
        self._images['compOut'] = compOut * 255.0

        #########################################

        success = True
        msg = 'success'
        return success, msg

