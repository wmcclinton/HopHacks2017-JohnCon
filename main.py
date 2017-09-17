from JohnCon import JohnCon
import os
import glob

images = []

for file in glob.glob("Mortage/*.png"):
    print(file)
    images.append(file)

JC = JohnCon(2)
JC.render(images,MONTAGE=True)
