import sys
import os
from PIL import Image
from os import listdir
from os.path import isfile, join


# grab arguments from python file
library = sys.argv[1]
target_path = sys.argv[2]
print(len(sys.argv))
print(str(sys.argv))

# create new folder if there is none
if not os.path.exists(target_path):
    os.makedirs(target_path)

# loop through all images and
# covert them to png
# save to new folder

onlyfiles = [f for f in listdir(library) if isfile(join(library, f))]
for file in onlyfiles:
    to_convert = Image.open(rf".\{library}\{file}")
    to_convert.save(rf".\{target_path}\{file[0:-4]}.png")
