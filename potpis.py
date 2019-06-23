# -*- coding: utf-8 -*-
#
# GLAVNI DIO PROGRAMA
#
# Verzija Python-a 2.7.6
#
#
import os
import obrada


def usporedi_greska(a, b, tolerancija):
    if abs(a-b) > tolerancija:
        print "Razlika (F)....: {} - {} -> {}".format(a, b, abs(a-b))
        return True
    else:
        print "Razlika (T)....: {} - {} -> {}".format(a, b, abs(a-b))
        return False


def main():

    app_dir = os.path.dirname(__file__)

    # ------------------------------------------------------------------------------------------------------------------
    # Funkcija prikazuje na ekranu sve potpise za određenog korisnika prema tipu (folderi)
    # ------------------------------------------------------------------------------------------------------------------
    #
    # obrada.ispisi_na_ekran(app_dir, 'autentican', '1')

    # ------------------------------------------------------------------------------------------------------------------
    # Funkcija "preuzmi_obiljezja" generira polje i datoteku sa izuzetim karakteristikama za potpise
    # Params:
    #   app_dir   - putanja aplikacije
    #   vrsta     - ["autentican","krivotvoren"]
    #   korisnik  - 1,2,3, ... broj direktorija u kojemu su slike
    #   spremi    - spremi u TXT file
    #
    # Generiranjem datoteka moguće je te podatke ubaciti u DM model i
    # na temelju toga dobiti podatke na koji način je potrebno "vagati" pojedine parametre
    # ------------------------------------------------------------------------------------------------------------------
    #

    print "Ispisujem obilježja u tekstualnu datoteku..."

    obrada.preuzmi_obiljezja(app_dir, 'autentican', '1', True)

    # ------------------------------------------------------------------------------------------------------------------
    # Pošto trenutno nemamo dovoljno vremena za daljnje modeliranje i implementaciju sustava neuronskih mreža ili
    # nekog drugog klasifikatora, za primjer smo uzeli parametre potpisa za određeni broj instanci te su na temelju toga
    # izvedene srednje vrijednosti (ponderane) kako bi se dobila jedinstvena klasifikacija (predložak) za usporedbu
    # ------------------------------------------------------------------------------------------------------------------
    #
    print "Radim..."

    ob_klasa = obrada.preuzmi_obiljezja(app_dir, 'autentican', '1', False)

    # Inicijalizacija varijabli za računannje srednjih vrijednosti
    #
    mean_h = 0
    mean_w = 0
    mean_ovd = 0
    mean_zp = 0
    mean_ar = 0
    mean_obl = 0
    mean_obd = 0
    mean_okl = 0
    mean_okd = 0
    mean_sx = 0
    mean_sy = 0
    mean_slp = 0
    mean_dis = 0

    broj_instanci = 0

    # Sumiranje kolona za izračun srednjih vrijednosti pokazatelja
    #
    for i in range(len(ob_klasa)):
        instanca_kolona = ob_klasa[i]
        mean_h += float(instanca_kolona[2])
        mean_w += float(instanca_kolona[3])
        mean_ovd += float(instanca_kolona[4])
        mean_zp += float(instanca_kolona[5])
        mean_ar += float(instanca_kolona[6])
        mean_obl += float(instanca_kolona[7])
        mean_obd += float(instanca_kolona[8])
        mean_okl += float(instanca_kolona[9])
        mean_okd += float(instanca_kolona[10])
        mean_sx += float(instanca_kolona[11])
        mean_sy += float(instanca_kolona[12])
        mean_slp += float(instanca_kolona[13])
        mean_dis += float(instanca_kolona[14])
        broj_instanci += 1

    # ------------------------------------------------------------------------------------------------------------------
    # Funkcija preuzima potpis čiju autentičnost želimo provjeriti
    # ------------------------------------------------------------------------------------------------------------------
    # vrsta     = autentican, krivotvoren
    # korisnik  = 1,2
    # datoteka  = signature-001.png - signature-006.png
    #
    vrsta = 'autentican'
    korisnik = '1'
    datoteka = 'signature-001.png'

    ob_instanca = obrada.preuzmi_obiljezja_instance(app_dir, vrsta, korisnik, datoteka)

    # ------------------------------------------------------------------------------------------------------------------
    # Funkcija ispisuje potpis čiju autentičnost želimo provjeriti (može se označiti sa oznakom komentara)
    # ------------------------------------------------------------------------------------------------------------------
    #
    obrada.ispisi_instancu_na_ekran(app_dir, vrsta, korisnik, datoteka)

    # Srednje vrijednosti za klasu potpisa
    #
    # Visina i dužina
    mean_h = mean_h / broj_instanci
    mean_w = mean_w / broj_instanci

    # Omjer visina i dužina
    mean_ovd = mean_ovd / broj_instanci

    # Zauzeće potpisa
    mean_zp = mean_zp / broj_instanci
    mean_ar = mean_ar / broj_instanci

    # Omjer točaka i desnog i lijevog dijela potpisa
    mean_obl = mean_obl / broj_instanci
    mean_obd = mean_obd / broj_instanci
    mean_okl = mean_okl / broj_instanci
    mean_okd = mean_okd / broj_instanci

    # Centralna vrijednost
    mean_sx = mean_sx / broj_instanci
    mean_sy = mean_sy / broj_instanci

    # Nagib i udaljenost
    mean_slp = mean_slp / broj_instanci
    mean_dis = mean_dis / broj_instanci

    # Počinjem uspoređivati podatke iz klase (predloška) i testne instance
    #
    rezultat_usporedbe = True

    print "Uspoređujem..."

    # Prosječna širina i dužina nisu dobar pokazatelj jer ne sklairaju
    # zato se koisti omjer širine i dužine (mean_ovd)
    #
    # if usporedi_greska(ob_instanca[0][2], mean_h, 100.0):
    #     rezultat_usporedbe = False
    # if usporedi_greska(ob_instanca[0][3], mean_w, 100.0):
    #     rezultat_usporedbe = False

    # Parametri za toleranciju greške u mjerama ručno su trenirane iako je pokušano i sa
    # WEKA alatom, međutim nije bilo dovoljno vremena da bi se ti modeli implementirali
    # pretpostavka je da bi rezultati bili bolji čak i sa ovakvim jednostavnim usporedbama
    #
    # Nastavak na ovaj jednostavni dokaz bila bi implementacija nekog od algoritama neuronskih mreža BPNN...
    # sa čime bi rezultati bili još bolji i pouzdaniji
    #
    if usporedi_greska(ob_instanca[0][4], mean_ovd, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][5], mean_zp, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][6], mean_ar, 150.0):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][7], mean_obl, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][8], mean_obd, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][9], mean_okl, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][10], mean_okd, 0.2):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][11], mean_sx, 10.0):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][12], mean_sy, 20.0):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][13], mean_slp, 10.0):
        rezultat_usporedbe = False
    if usporedi_greska(ob_instanca[0][14], mean_dis, 10.0):
        rezultat_usporedbe = False

    print rezultat_usporedbe

    if rezultat_usporedbe:
        print 'Potpis je autentičan!'
    else:
        print 'Potpis nije autentičan!'


if __name__ == '__main__':
    main()
