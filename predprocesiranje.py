# -*- coding: utf-8 -*-
#
# PREDPROCESIRANJE SLIKE
# (Početna priprema slike)
#
import cv2
import numpy as np
from skimage import io, color, morphology


def pripremi_sliku(image):
    # Vraća razne nekoliko izmjenih slika za daljnji upotrebu

    # Čišćenje od smetnji
    # img_clean = cv2.fastNlMeansDenoising(image)
    img_clean = image

    # Glađenje
    img_smooth = cv2.medianBlur(img_clean, 5)

    # Pretvaranje u binarnu sliku
    ret, img_binary = cv2.threshold(img_smooth, 117, 1,  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Izrezan potpis
    img_crop = crop(img_binary)

    # img_crop = np.array(img_crop, dtype=np.uint8)

    # Stanjiti potpis na jedan pixel
    img_skeleton = morphology.skeletonize(img_crop)
    img_skeleton = np.array(img_skeleton, dtype=np.uint8)

    img_thin = morphology.thin(img_crop)
    img_thin = np.array(img_thin, dtype=np.uint8)

    return img_smooth, img_binary, img_crop, img_skeleton, img_thin


def crop(image):
    # Izrezuje sliku na minimalne dimenzije sa bijelim pixelima

    points = cv2.findNonZero(image)
    x, y, w, h = cv2.boundingRect(points)
    return image[y: y+h, x: x+w]