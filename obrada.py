# -*- coding: utf-8 -*-
#
# OBRADE (ZAJEDNIČKE FUNKCIJE)
#
import izlucivanje
import predprocesiranje
import cv2
import os
from matplotlib import pyplot as plt


def preuzmi_obiljezja_instance(app_dir, vrsta, korisnik, filename):

    rezultat = []

    # Izlučivanje potpisa za usporedbu
    #
    img_dir = os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/{}".format(vrsta, korisnik, filename)))

    if "png" in filename:
        # Čitanje potpisa
        image = cv2.imread(img_dir, 0)
        img_smooth, img_inverted, img_crop, img_skeleton, img_thin = predprocesiranje.pripremi_sliku(image)

        # Izlucivanje
        rezultat = izlucivanje.obiljezja(vrsta, korisnik, img_thin, True, rezultat)

    return rezultat


def preuzmi_obiljezja(app_dir, vrsta, korisnik, spremi):

    rezultat = []
    img_dir = ''
    img_num = 0

    # Orginalni potpisi (priprema)
    # Krivotvoreni potpisi (priprema)
    # Izlučivanje potpisa za usporedbu
    #
    for filename in os.listdir(os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/".format(vrsta, korisnik)))):
        print filename
        if "png" in filename:
            img_dir = os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/{}".format(vrsta, korisnik, filename)))
            print img_dir

            # Čitanje potpisa
            image = cv2.imread(img_dir, 0)
            img_smooth, img_inverted, img_crop, img_skeleton, img_thin = predprocesiranje.pripremi_sliku(image)

            img_num += 1

            # Izlucivanje
            rezultat = izlucivanje.obiljezja(vrsta, korisnik, img_thin, True, rezultat)

    if spremi:
        if not rezultat:
            print 'Nema podataka u direktoriju! {}'.format(img_dir)
        else:
            datoteka = open("podaci/podaci-{}-{}.csv".format(vrsta, korisnik), "w")
            datoteka.write("TYPE, USR, H, W, HWR, SOR, AR, WPR-L, WPR-D, HCM-L, HCM-D, CM-X, CM-Y, SLOPE, DIS \n")
            for i in range(img_num):
                datoteka.write("{} \n".format(str(rezultat[i]).strip('[]')))
            datoteka.close()

    return rezultat


def ispisi_na_ekran(app_dir, vrsta, korisnik):
    titles = []
    images = []

    # Pregled datoteka u odabranom folderu (png format)
    #
    for filename in os.listdir(os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/".format(vrsta, korisnik)))):
        print filename
        if "png" in filename:
            img_dir = os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/{}".format(vrsta, korisnik, filename)))
            print img_dir

            # Čitanje potpisa
            image = cv2.imread(img_dir, 0)
            img_smooth, img_inverted, img_crop, img_skeleton, img_thin = predprocesiranje.pripremi_sliku(image)

            titles.append(filename)
            images.append(img_thin)

    plt.style.use('seaborn-white')
    for i in range(len(images)):
        plt.subplot(3, 2, i + 1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

    return True


def ispisi_instancu_na_ekran(app_dir, vrsta, korisnik, filename):

    titles = []

    # Pregled datoteka u odabranom folderu (png format)
    #
    if "png" in filename:
        img_dir = os.path.normpath(os.path.join(app_dir, "podaci/{}/{}/{}".format(vrsta, korisnik, filename)))
        print img_dir

        # Čitanje potpisa
        image = cv2.imread(img_dir, 0)
        img_smooth, img_inverted, img_crop, img_skeleton, img_thin = predprocesiranje.pripremi_sliku(image)

        titles.append("Originalni potpis")
        titles.append("Potpis - BW")
        titles.append("Potpis - CROP/INV")
        titles.append("Potpis - THIN")

        images = [image, img_inverted < 0.5, img_crop, img_thin < 0.5]

        for i in range(len(images)):
            plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()

    return True
