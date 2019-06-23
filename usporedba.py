# -*- coding: utf-8 -*-
#
# USPOREDBA DVA POTPISA
# (Korak nakon izlucivanja)
#
# TRENUTNO SE NE KORISTI U GLAVNOM PROGRAMU
# FUNKCIONIRA SA GRAYSCALE SLIKAMA
#
# Isprobane su opcije SURF, SIFT, ORB, FAST
# Isprobani su sustavi za usporedbu ključnih točaka BFMatcher, FlannBasedMatcher
# međutim kako nisu pronađeni modeli prema kojima bi se potpisi mogli pouzdano detektirati
# nakon testiranja tih metoda daljnje testiranje je išlo u smjeru izvlačenja generalnih obilježja
# i jednostavne usporedbe,
# dok bi konačni konačni cilj istraživanja bio da se uz generalna obilježja implementiraju
# i neka lokalna obilježja, te nadograditi to sa BPNN neuronskom mrežom koja bi za svakog korisnika imala pohranjeni
# istreniran model koji bi se sa svakom novom pozitivnom verifikacijom ažurirao na način
# da se sustav detekcije usklađuje protekom vremena za svakog korisnika
#
import cv2
from numpy import *
from matplotlib import pyplot as plt


def usporedi_potpis(image1, image2, broj_podudarnosti):

    # Iniciram SURF detector
    surf = cv2.xfeatures2d.SURF_create(400)

    # Pronalazi ključne točke i kreira opisnike (descriptors) točaka
    mask = uint8(ones(image1.shape))
    kp1, des1 = surf.detectAndCompute(image1, mask)
    mask = uint8(ones(image2.shape))
    kp2, des2 = surf.detectAndCompute(image2, mask)

    FLANN_INDEX_KDTREE = 0

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    podudarni = flann.knnMatch(des1, des2, k=2)

    # Spremi sve usporedbe koje odgovaraju određenom omjeru
    # Lowe's ratio test
    print(podudarni)

    podudarni_ok = []
    for m, n in podudarni:
        if m.distance < 0.70 * n.distance:
            podudarni_ok.append(m)

    images = [image1, image2]
    titles = ['Usporedi 1', 'Usporedi 2']

    plt.figure(figsize=(10, 10))
    for i in range(2):
        plt.subplot(1, 2, i + 1), plt.imshow(images[i], None)
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

    if len(podudarni_ok) >= broj_podudarnosti:
        return True
    return False
