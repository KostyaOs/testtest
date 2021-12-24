import os
from basic_functions import get_top_dir_path
from PIL import Image


topdirpath = get_top_dir_path()
print(topdirpath)
with open(topdirpath + "/top_dir_path.txt", "r") as file:
    file_contents = file.read()
    print(file_contents)
exit()





#create first row, it's unique
#loop over
    #create first block of next row
    # use it's data to select 3 images to glue to it
