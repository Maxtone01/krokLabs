import glob
import os
import cv2
from multiprocessing import Pool, cpu_count
from functools import partial
from timeit import default_timer as timer


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
TYPES = ['*.jpg', '*.png', '*.jpeg']

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def GetPathImage():
    paths = []

    for file_type in TYPES:
        paths.extend(glob.glob(os.path.join(INPUT_DIR, file_type)))

    return paths


def ReplaceJpg(img_path):
    replaceTypes = ['.png', '.jpeg']

    imgName = img_path.split('/')[-1]
    for type in replaceTypes:
        imgName = imgName.replace(type, '.jpg')

    return imgName


def FaceRecog(img_path):
    img = cv2.imread(img_path)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.2)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(os.path.join(
        OUTPUT_DIR,
        ReplaceJpg(img_path)
        ),
        img
    )


def AllFaceRecog(imgPaths, nProcesses):
    start = timer()
    with Pool(nProcesses) as p:
        p.map(partial(FaceRecog), imgPaths)

    print(f'Took {timer() - start} seconds with {nProcesses=}')


if __name__ == '__main__':
    img_paths = GetPathImage()

    n_processes = 3
    AllFaceRecog(img_paths, n_processes)
