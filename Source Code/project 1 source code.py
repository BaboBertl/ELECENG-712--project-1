from PIL import Image
import math
from numpy import asarray
import numpy as np
import matplotlib.image as mpimg

#open the desired image
original_image = Image.open("images/project1.jpg")

#convert the image into an array
data = asarray(original_image)

#show the pixel value of the original image
#shown as (y, x) where y = height and x = width
[y, x] = data.shape
print("original image size: ", data.shape)

#create a function
def bilinear_resample(image, height, width):
  """
  `image` is the inputed 2-D numpy array
  `height` and `width` are the desired spatial dimension of the new 2-D array;
   where  height is the y-value of the pixel and width is the x-value of the 
   pixel
  """
  
  #sequence unpacking from the input data
  image_height, image_width = image.shape[:2]
  
  #returns a new array of given shape with the desired dimension
  resampled = np.empty([height, width])
  
  #determining the coefficient ratio of the length of integer intervals 
  #between the input data dimensions and the desired demensions
  x_coefficient = float(image_width - 1) / (width - 1) if width > 1 else 0
  y_coefficient = float(image_height - 1) / (height - 1) if height > 1 else 0

  #the for loop allows the function to iterate over a sequence of numbers 
  #produced by the range function, in this case i is all the elements in the 
  #desired height range and j is all the elements in the desired width range 
  for i in range(height):
    for j in range(width):    

      #this allows the function to interpolate the value at the coordinate 
      #[i,j], where 0 <= i < height and 0 <= j < width. the mapped coordinate
      #in the original 2-D array is computed as  
      #[y_coefficient * i, x_coefficient * j], where the coordinates of the
      #four points that are nearest to [i,j] are 
      #Q11 = [y_w, x_w], Q12 = [y_w, x_h], Q21 = [y_h, x_w], Q22 = [y_h, x_h]
      x_w, y_w = math.floor(x_coefficient * j), math.floor(y_coefficient * i)
      x_h, y_h = math.ceil(x_coefficient * j), math.ceil(y_coefficient * i)

      #linear interpolation computes it as a weighted average of the values
      #associated between two points, where the weights are proportional to 
      #the distance between the specific pixel and its 4 nearest neighbors 
      x_weight = (x_coefficient * j) - x_w
      y_weight = (y_coefficient * i) - y_w

      #the value of the four nearest neighbors 
      a = image[y_w, x_w]
      b = image[y_w, x_h]
      c = image[y_h, x_w]
      d = image[y_h, x_h]

      #general equation for bilinear interpolation 
      pixel_value = a * (1 - x_weight) * (1 - y_weight) \
              + b * x_weight * (1 - y_weight) + \
              c * y_weight * (1 - x_weight) + d * x_weight * y_weight

      #returend back to the exact spatial dimension of the original image 
      resampled[i][j] = pixel_value

  #end of the function
  return resampled

#calculating when t < 1
t1 = 0.2
resampled_t1 = bilinear_resample(data, int(y*t1), int(x*t1))

#calculating when t > 1
t2 = 2
resampled_t2 = bilinear_resample(data, int(y*t2), int(x*t2))

#displays the shape of the new images, allows the user to confirm that the
#new image 
print("resampled image size t < 1 (t=0.2): ", resampled_t1.shape)
print("resampled image size t > 1 (t=2): ", resampled_t2.shape)

#saves the new images as .jpg files
mpimg.imsave("t = 0.2.jpg", resampled_t1)
mpimg.imsave("t = 2.jpg", resampled_t2)
