# -*- coding: utf-8 -*-
#
# IZLUČIVANJE KARAKTERISTIKA POTPISA
# korak nakon predprocesiranja
#
import math
import cv2 as cv
import numpy as np


def centar_mase(image, h, w):

    suma_x = 0
    suma_y = 0
    broj_tocaka = 0
    for i in range(0, h, 1):
        for j in range(0, w, 1):
            if image[i, j] == 1:
                suma_x += i
                suma_y += j
                broj_tocaka += 1

    return suma_x // broj_tocaka, suma_y // broj_tocaka


def obiljezja(vrsta, korisnik, image, ispis, rezultat):

    # O1
    # Omjer visine naspram dužine
    # Height to Width Ratio
    #
    x, y, w, h = cv.boundingRect(image)
    omjer_visina_duzina = float(h) / w

    # O2
    # Omjer broja pixela potpisa prema broju pixela cijele slike
    # (Signature Occupancy Ratio)
    #
    # points = cv.findNonZero(image)  # List of point coordinates
    points = np.count_nonzero(image)
    zauzece_potpis = float(points) / (w * h)

    # O3
    # Omjer gornje i donje linije potpisa množen sa brojem pixela potpisa
    # (Adjacency Ratio)
    #

    LT = []
    LB = []

    for i in range(0, w, 1):
        if np.any(image[:, i]):
            row = image[:, i]
            top = np.amin(np.where(row == 1))
            bot = np.amax(np.where(row == 1))
            LT.append(top)
            LB.append(bot)
            # LTv.append([i, top]) # 2D (Ako je potrebno vizualizirati)
            # LBv.append([i, bot]) # 2D (Ako je potrebno vizualizirati)

    AR = (sum(LT)+sum(LB)) * zauzece_potpis

    # O4 & O5
    # Omjer broja bijelih pixela lijeve polovice slike prema cijeloj slici
    # (White Pixel Ratio)
    #
    limage, rimage = np.array_split(image, 2, 1)

    lpoints = np.count_nonzero(limage)
    omjer_bijeli_lijevo = float(lpoints) / points

    rpoints = np.count_nonzero(rimage)
    omjer_bijeli_desno = float(rpoints) / points

    # O6 & O7
    # Omjer broja bijelih pixela desne polovice slike prema cijeloj slici
    # (White Pixel Ratio)
    #
    corners = cv.cornerHarris(image, 2, 3, 0.04)
    lcorners = cv.cornerHarris(limage, 2, 3, 0.04)
    rcorners = cv.cornerHarris(rimage, 2, 3, 0.04)

    omjer_kutovi_lijevo = float(np.count_nonzero(lcorners)) / np.count_nonzero(corners)
    omjer_kutovi_desno = float(np.count_nonzero(rcorners)) / np.count_nonzero(corners)

    # O8 & O9
    # Centar mase za X i Y os
    # (Coordinates of the Centre of mass for image)
    #
    srednji_x, srednji_y = centar_mase(image, h, w)

    # O10
    # Nagib
    # Linija koja spaja dvije točke centara mase za lijevu i desnu polovicu
    # (Slope of the line joining the Centre of masses of left and right halve of signature)

    lh, lw = limage.shape
    rh, rw = rimage.shape
    lsrednji_x, lsrednji_y = centar_mase(limage, lh, lw)
    rsrednji_x, rsrednji_y = centar_mase(rimage, rh, rw)

    nagib = float((rsrednji_y - lsrednji_y)) / (rsrednji_x - lsrednji_x)

    # O11
    # Udaljenost
    # Linija koja spaja dvije točke centara mase za lijevu i desnu polovicu
    # (Distance of the line joining the centre of masses of left and right halve of signature)
    #
    udaljenost = math.sqrt(pow((rsrednji_y - lsrednji_y), 2) + pow((rsrednji_x - lsrednji_x), 2))

    #
    # Ispis rezultata izuzimanja obilježja potpisa
    # (Report)
    #
    if ispis:
        print 'TYPE ...:', vrsta
        print 'USR ....:', korisnik
        print 'H ......:', h
        print 'W ......:', w
        print 'HWR ....:', omjer_visina_duzina
        print 'SOR ....:', zauzece_potpis
        # print 'LT .....:', LT
        # print 'LB .....:', LB
        print 'AR .....:', AR
        print 'WPR-L ..:', omjer_bijeli_lijevo
        print 'WPR-D ..:', omjer_bijeli_desno
        print 'HCM-L ..:', omjer_kutovi_lijevo
        print 'HCM-D ..:', omjer_kutovi_desno
        print 'CM-X ...:', srednji_x
        print 'CM-Y ...:', srednji_y
        print 'SLOPE ..:', nagib
        print 'DIS ....:', udaljenost

    rezultat.append([ vrsta
                    , korisnik
                    , h
                    , w
                    , omjer_visina_duzina
                    , zauzece_potpis
                    , AR
                    , omjer_bijeli_lijevo
                    , omjer_bijeli_desno
                    , omjer_kutovi_lijevo
                    , omjer_kutovi_desno
                    , srednji_x
                    , srednji_y
                    , nagib
                    , udaljenost])

    return rezultat
