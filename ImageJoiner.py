from PIL import Image
import os
import random

images = []
PATH = "Digits/"
for x in os.listdir("Digits"):
    images.append(PATH + str(x.title()).replace("Png", "png"))

rand = random.randint(0, 8)
first_image = Image.open(images[rand])
w, h = first_image.size

new_width = w
new_height = 0

max_width = 10 * w
max_height = 5 * h
result = Image.new('1', (max_width, max_height), color=255)
for counter in range(0, 51, 1):
    r1 = random.randint(0, 8)
    r2 = random.randint(0, 8)
    add_image1 = Image.open(images[r1])
    add_image2 = Image.open(images[r2])

    result.paste(im=add_image1, box=(0, 0))
    result.paste(im=add_image2, box=(new_width, new_height))

    if new_width + w <= max_width:
        new_width += w

    if counter % 10 == 0 and counter != 0:
        new_height += h
        new_width = 0

    print(new_width, new_height)
    result.save("train.png")
