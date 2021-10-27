import os
from PIL import Image

images = []
folder = 'testimages'
files = os.listdir(folder)
files.sort()
for file in files:
    image = Image.open(folder + '/' + file)
    images.append(image)


imageSize = image.size
nImages = len(images)
result = Image.new('RGB', (nImages * imageSize[0], imageSize[1]), (250, 250, 250))
i = 0
for image in images:
    result.paste(image, (i, 0))
    i += imageSize[0]
result.save(folder + "/mergeTotal.jpg", "JPEG")
#result.show()
