import face_recognition
from PIL import Image, ImageDraw
import numpy as np
from peopledelect import *
from utils import *
from imutils import paths
import re
from settings import *
# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
known_face_names=[]
known_face_encodings=[]
for imagePath in paths.list_images("./known_person"):
    name=re.sub(r'\.\/known_person\\','',imagePath)
    name=re.sub(r'\.[a-zA-Z]+','',name)
    image=face_recognition.load_image_file(imagePath)
    encodeing=face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encodeing)
    known_face_names.append(name)

for imagePath in paths.list_images("./images"):
    illegalwalkersname=[]
    illegalwalkers=[]
    walkers=get_walkers(imagePath)
    for walker in walkers:
        if is_walker_in_area(walker,area):
            illegalwalkers.append(walker)        
    # print(illegalwalkers)
    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(imagePath)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)
    face_list=[]
    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        if left+text_width<right:
            text_width=right-left
        draw.rectangle(((left, bottom), (left+text_width, bottom+text_height)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom), name, fill=(255, 255, 255, 255))
        face_list.append(((top, right, bottom, left),name))
    # if not len(illegalwalkers):
    #     continue
    text_width, text_height = draw.textsize('illegal')
    if left+text_width<right:
        text_width=right-left
    for (top, right, bottom, left),name in face_list:
        for walker in illegalwalkers:
            if is_face_in_walker((left, top, right, bottom),walker):
                illegalwalkersname.append(name)
                draw.rectangle(((left, bottom+text_height), (left + text_width, bottom+2*text_height)), fill=(255, 0, 0), outline=(255,0, 0))
                draw.text((left + 6, bottom+text_height), 'illegal', fill=(255, 255, 255, 255))
                break

    # Remove the drawing library from memory as per the Pillow docs
    del draw
    if "Unknown" in illegalwalkersname:
        illegalwalkersname.remove("Unknown")
    print("图 "+imagePath+" 违法者名单："+str(illegalwalkersname))
    # Display the resulting image
    # pil_image.show()

    # You can also save a copy of the new image to disk if you want by uncommenting this line
    imagePath=re.sub("images",'output',imagePath)
    imagePath=re.sub(r"\.[a-z]+",'',imagePath)
    pil_image.save(imagePath+'.png',"PNG")