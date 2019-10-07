"""
Requiements:
* Python 3.x
* library PIL
"""
from PIL import Image, ImageDraw

img = Image.open('sample.PNG') # The image file must exist in the same directory as the script
img = img.convert('1') # Convert the file data to 1-byte per pixel (Black == 0 & White == 1)

# Get the size of the input image
width, height = img.size

# The following four variables will define the edges of the non empty region (i.e containing black pixels) 
min_x = width
min_y = height
max_x = 0
max_y = 0
# This variable is only for statistics
NonEmptyPixelCount = 0

# Main loop: for each black pixel found, update the extremum values of the non empty region
for x in range(0, width):
    for y in range(0, height):
        if img.getpixel((x, y)) == 0:
            if min_x > x : min_x = x
            if min_y > y : min_y = y
            if max_x < x : max_x = x
            if max_y < y : max_y = y
            NonEmptyPixelCount += 1

# Now, draw for lines forming a rectangle "surrounding" the region of interest 
draw = ImageDraw.Draw(img)
# line's width is 1 pixel and its color is black (fill=0)
draw.line((min_x, min_y, max_x, min_y), fill = 0,  width=1) # line from top left to top right
draw.line((min_x, min_y, min_x, max_y), fill = 0,  width=1) # line from top left to bottom left
draw.line((max_x, min_y, max_x, max_y), fill = 0,  width=1) # line from top right to bottom right
draw.line((min_x, max_y, max_x, max_y), fill = 0,  width=1) # line from bottom left to bottom right

print("###################### STATS ######################")
print("Input image width : " + str(width))
print("Input image height : " + str(height))
print("Number of non empty pixels : " + str(NonEmptyPixelCount))

img.show()
