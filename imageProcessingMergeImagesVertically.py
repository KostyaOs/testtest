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
result = Image.new('RGB', (imageSize[0], nImages * imageSize[1]), (250, 250, 250))
i = 0
for image in images:
    result.paste(image, (0, i))
    i += imageSize[1]
result.save(folder + "/merge2.jpg", "JPEG")
#result.show()
