#ma być 21040 Goblinów, 754 wróżek, 27504 ludzi i 25357 elfów
from random import *
import json
import os
import pygame
import time
class Walka:
    def __init__(self, postać1, postać2):
        self.postać1 = postać1
        self.postać2 = postać2
        self.tura = 0
        self.log_walki = []
    def komunikat(self, tekst):
        self.log_walki.append(tekst)
        
        if len(self.log_walki) > 6:
            self.log_walki.pop(0)
def usuń_plik(plik):
    try:
        os.remove(plik)
        print("Plik został usunięty.")
    except FileNotFoundError:
        print("Plik nie istnieje.")
def zapisz_gre(stan_gry, plik):
    with open(f"gry/artefakty_pygame/saves/{plik}.json", "w") as f:
        json.dump(stan_gry, f)
    print("Gra zapisana!")
def wczytaj_gre(plik):
    try:
        with open(f"gry/artefakty_pygame/saves/{plik}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Brak zapisu gry.")
        return None
class dodanie_stat:
    def __init__(self, nazwa, obrona, atak, tury, wytrzymałość):
        self.nazwa = nazwa
        self.obrona = obrona
        self.atak = atak
        self.tury = tury
        self.wytrzymałość = wytrzymałość
    def po(self):
        return {"nazwa":self.nazwa,
                "obrona":self.obrona,
                "atak":self.atak,
                "tury":self.tury,
                "wytrzymałość":self.wytrzymałość}
    def wczytaj(self,wnazwa,wobrona,watak,wtury,wwytrzymałość):
        self.nazwa = wnazwa
        self.obrona = wobrona
        self.atak = watak
        self.tury = wtury
        self.wytrzymałość = wwytrzymałość
zbroje_def = {
    "czarno_zbroja": ("czarno zbroja", {"głowa":0, "klatka":20, "lręka":5, "pręka":5, "brzuch":20, "lrzebro":10, "przebro":10, "lnoga":0, "pnoga":0}, 10, 0, (100, 150)),
    "brak_zbroi": ("brak zbroi", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (0, 0)),
    "jasno_zbroja": ("jasno zbroja", {"głowa":20, "klatka":20, "lręka":10, "pręka":10, "brzuch":30, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (100, 120)),
    "łuska_smoka": ("łuska smoka", {"głowa":0, "klatka":300, "lręka":0, "pręka":0, "brzuch":500, "lrzebro":50, "przebro":50, "lnoga":0, "pnoga":0}, 500, 0, (500, 500)),
    "sdz_metalowa_zbroja": ("sdz metalowa zbroja", {"głowa":40, "klatka":50, "lręka":10, "pręka":10, "brzuch":50, "lrzebro":40, "przebro":40, "lnoga":60, "pnoga":60}, 0, 0, (10, 50)),
    "metalowa_zbroja": ("metalowa zbroja", {"głowa":50, "klatka":100, "lręka":70, "pręka":70, "brzuch":120, "lrzebro":100, "przebro":100, "lnoga":80, "pnoga":80}, 0, 0, (100, 150)),
    "zbroja_z_błota_i_liści": ("zbroja z błota i liści", {"głowa":0, "klatka":5, "lręka":0, "pręka":0, "brzuch":10, "lrzebro":1, "przebro":1, "lnoga":5, "pnoga":5}, 0, 0, (10, 20))
}
bronie_def = {
    "brak_broni": ("brak broni", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (0, 0)),
    "łuk": ("łuk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 50, 0, (50, 100)),
    "topur": ("topur", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 500, (500, 500)),
    "włócznia": ("włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 20, (100, 200)),
    "ostra_włócznia": ("ostra włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 50, (100, 150)),
    "cięki_patyk": ("cięki patyk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 10, (10, 20))
}
def stworz_przedmiot(definicja):
    nazwa, obrona, atak, tury, (min_w, max_w) = definicja
    wartosc = randint(min_w, max_w)
    return dodanie_stat(nazwa, obrona, atak, tury, wartosc)
def daj_zbroje(nazwa):
    return stworz_przedmiot(zbroje_def[nazwa])
def daj_bron(nazwa):
    return stworz_przedmiot(bronie_def[nazwa])
class Postać:
    wróżki = 0
    ludzie = 0
    elfy = 0
    Gobliny = 0
    żywi = []
    polegli = []
    def __init__(self, istota, imie, głowa, klatka, lręka, pręka, brzuch, lrzebro, przebro, lnoga, pnoga, napojenie,mnapojenie, głód, mgłód, atak, obrona, zbroja, broń,chce_zatakować,musi,x,y,szybkość,szybkość_ataku,hitbox_w, hitbox_h, offset_x, offset_y):
        self.imie = imie
        self.głód = głód
        self.mgłód = mgłód
        self.napojenie = napojenie
        self.mnapojenie = mnapojenie
        self.istota = istota
        self.głowa = głowa  # 20%
        self.klatka = klatka  # 25%
        self.lręka = lręka  # 5%
        self.pręka = pręka
        self.brzuch = brzuch  # 7.5%
        self.lrzebro = lrzebro  # 1.25%
        self.przebro = przebro
        self.lnoga = lnoga  # 17.5%
        self.pnoga = pnoga
        self.artefakty = {1: None, 2: None, 3: None}
        self.za_atak = atak
        self.za_obrona = obrona
        self.atak = atak
        self.obrona = obrona
        self.zbroja = zbroja
        self.broń = broń
        self.umiejętności = []
        self.ciało = głowa + klatka + lręka + pręka + brzuch + lrzebro + przebro + lnoga + pnoga
        self.nczęści_ciała = [self.głowa, self.klatka, self.lręka, self.pręka, self.brzuch, self.lrzebro, self.przebro,self.lnoga, self.pnoga]
        self.części_ciała = ["głowa", "klatka", "lręka", "pręka", "brzuch", "lrzebro", "przebro", "lnoga", "pnoga"]
        self.ogłuszony = False
        self.czas_ogłuszenia = 0
        self.chce = chce_zatakować
        self.musi = musi
        self.tury = broń.tury
        self.drużyna = []
        self.wrogowie = []
        self.ekwipunek = {"ciękie patyki": 0,"kamienie": 0,"kawałki metalu": 0,"siekiera":0}
        self.oszczędzenie = 0
        self.relacje = {}
        # Do obsługi działania artefaktów
        self.wochuk_uses = {}  # przeciwnik: ile razy użyto
        self.cozwoj_uses = 0
        # ... (Twój dotychczasowy kod w __init__) ...
        self.x = x
        self.y = y
        self.szybkość = szybkość
        self.szybkość_ataku = szybkość_ataku
        
        # --- TUTAJ DOPISZ PARAMETRY HITBOXU ---
        self.hitbox_w = hitbox_w
        self.hitbox_h = hitbox_h
        self.offset_x = offset_x
        self.offset_y = offset_y
        # Tworzymy właściwy obiekt prostokąta Pygame
        self.hitbox = pygame.Rect(self.x + self.offset_x, self.y + self.offset_y, self.hitbox_w, self.hitbox_h)
        # --------------------------------------

        Postać.żywi.append(self)
        if istota == "wróżka":
            Postać.wróżki += 1
        elif istota == "człowiek":
            Postać.ludzie += 1
        elif istota == "elf":
            Postać.elfy += 1
        elif istota == "Goblin":
            Postać.Gobliny += 1
    def wczytaj(self,wimie,wgłód,wmgłód,wnapojenie,wmnapojenie,wistota,wgłowa,wklatka,wlręka,wpręka,wbrzuch,wlrzebro,wprzebro,wlnoga,wpnoga,wartefakty,wza_atak,wza_obrona,watak,wobrona,wzbroja,wbronie,wumiejętności,wciało,wnczęści_ciała,wczęści_ciała,wogłuszony,wczas_ogłuszenia,wchce,wmusi,wtury,wdrużyna,wwrogowie,wekwipunek,woszczędzenie,wrelacje,wwochuk_uses,wcozwoj_uses,wx,wy,wplansza):
        self.imie = wimie
        self.głód = wgłód
        self.mgłód = wmgłód
        self.napojenie = wnapojenie
        self.mnapojenie = wmnapojenie
        self.istota = wistota
        self.głowa = wgłowa
        self.klatka = wklatka
        self.lręka = wlręka
        self.pręka = wpręka
        self.brzuch = wbrzuch
        self.lrzebro = wlrzebro
        self.przebro = wprzebro
        self.lnoga = wlnoga
        self.pnoga = wpnoga
        self.artefakty = wartefakty
        self.za_atak = wza_atak
        self.za_obrona = wza_obrona
        self.atak = watak
        self.obrona = wobrona
        self.zbroja.wczytaj(wzbroja["nazwa"],wzbroja["obrona"],wzbroja["obrona"],wzbroja["tury"],wzbroja["wytrzymałość"])
        self.broń.wczytaj(wbronie["nazwa"],wbronie["obrona"],wbronie["obrona"],wbronie["tury"],wbronie["wytrzymałość"])
        self.umiejętności = wumiejętności
        self.ciało = wciało
        self.nczęści_ciała = wnczęści_ciała
        self.części_ciała = wczęści_ciała
        self.ogłuszony = wogłuszony
        self.czas_ogłuszenia = wczas_ogłuszenia
        self.chce = wchce
        self.musi = wmusi
        self.tury = wtury
        self.drużyna = wdrużyna
        self.wrogowie = wwrogowie
        self.ekwipunek = wekwipunek
        self.oszczędzenie = woszczędzenie
        self.relacje = wrelacje
        self.wochuk_uses = wwochuk_uses
        self.cozwoj_uses = wcozwoj_uses
        self.x = wx
        self.y = wy
        self.plansza = wplansza
    def po(self):
        return {
            "imie": self.imie,
            "głód": self.głód,
            "mgłód": self.mgłód,
            "napojenie": self.napojenie,
            "mnapojenie": self.mnapojenie,
            "istota": self.istota,
            "głowa": self.głowa,
            "klatka": self.klatka,
            "lręka": self.lręka,
            "pręka": self.pręka,
            "brzuch": self.brzuch,
            "lrzebro": self.lrzebro,
            "przebro": self.przebro,
            "lnoga": self.lnoga,
            "pnoga": self.pnoga,
            "artefakty": self.artefakty,
            "za_atak": self.za_atak,
            "za_obrona": self.za_obrona,
            "atak": self.atak,
            "obrona": self.obrona,
            "zbroja": self.zbroja.po() if self.zbroja else None,
            "broń": self.broń.po() if self.broń else None,
            "umiejętności": self.umiejętności,
            "ciało": self.ciało,
            "nczęści_ciała": self.nczęści_ciała,
            "części_ciała": self.części_ciała,
            "ogłuszony": self.ogłuszony,
            "czas_ogłuszenia": self.czas_ogłuszenia,
            "chce": self.chce,
            "musi": self.musi,
            "tury": self.tury,
            "drużyna": self.drużyna,
            "wrogowie": self.wrogowie,
            "ekwipunek": self.ekwipunek,
            "oszczędzenie": self.oszczędzenie,
            "relacje": self.relacje,
            "wochuk_uses": self.wochuk_uses,
            "cozwoj_uses": self.cozwoj_uses
        }
    def aktualizuj_hitbox(self):
        self.hitbox.x = self.x + self.offset_x
        self.hitbox.y = self.y + self.offset_y
    def napraw_zbroje(self,ilość: int):
        if self.zbroja is None or self.zbroja.wytrzymałość == 0:
            print(f"{self.imie} nie ma zbroi do naprawy.")
            return
        if self.zbroja.nazwa in ["metalowa zbroja", "sdz metalowa zbroja"]:
            if self.ekwipunek.get("kawałki metalu", 0) < ilość:
                print(f"{self.imie} nie ma wystarczająco materiału do naprawy.")
                return
            self.ekwipunek["kawałki metalu"] -= ilość
            naprawa = 10 * ilość
            stara_wytrzymałość = self.zbroja.wytrzymałość
            self.zbroja.wytrzymałość = min(self.zbroja.wytrzymałość + naprawa, 150)
            print(f"{self.imie} naprawił zbroję o {naprawa} punktów wytrzymałości({stara_wytrzymałość} → {self.zbroja.wytrzymałość}).")
    def sprawdź_ekwipunek(self):
        print(f"ekwipunek postaci: {self.imie}")
        for przedmiot, ilość in self.ekwipunek.items():
            if ilość > 0:
                print(f"{przedmiot}: {ilość}")
    def zadaj_obrażenia(self, jaka_część: str, ile: int):
        setattr(self, jaka_część, getattr(self, jaka_część) - ile)
    def dodaj_relacje(self, postac, staty_relacji: int):
        if postac in self.relacje.values():
            self.relacje[postac] += staty_relacji
        else:
            self.relacje[postac] = staty_relacji
    def dodaj_wroga(self, wróg):
        self.wrogowie.append(wróg)
    def oszczędzanie(self, o_ile: float):
        self.oszczędzenie += o_ile
    def oszczędzony(self):
        return self.oszczędzenie > 100
    def synchronizacja(self, protokuł: int):

        # synchronizacja hp
        if protokuł == 3:
            self.ciało = sum(self.nczęści_ciała)

        # limity głodu/staminy
        elif protokuł == 2:
            self.głód = max(0, min(self.głód, self.mgłód))
            self.napojenie = max(0, min(self.napojenie, self.mnapojenie))
            self.oszczędzenie = max(0, min(self.oszczędzenie, 100))

        # statystyki
        elif protokuł == 1:

            # reset
            self.obrona = self.za_obrona.copy()
            self.atak = self.za_atak

            # goblin
            if self.istota == "goblin":

                if self.zbroja.nazwa not in ["łuska smoka", "brak zbroi"]:
                    print("Goblin może mieć tylko łuskę smoka!")
                    return

            else:

                if self.zbroja.nazwa == "łuska smoka":
                    print("Tylko goblin może nosić łuskę smoka!")
                    return

            # dodanie obrony zbroi
            if self.zbroja is not None:

                for część in self.obrona:
                    self.obrona[część] += self.zbroja.obrona.get(część, 0)

                self.atak += self.zbroja.atak

            # dodanie ataku broni
            if self.broń is not None:

                if self.broń.nazwa == "łuk" and self.istota == "elf":
                    self.atak += self.broń.atak + 20
                else:
                    self.atak += self.broń.atak
    def dodaj_osobę_do_drużyny_nieoficjalnie(self, p1):
        if p1 not in self.drużyna:
            self.drużyna.append(p1)
    def dodaj_osobę_do_drużyny_oficjalnie(self, p1, p2):
        if p1 not in self.drużyna:
            p2.drużyna.append(p1)
            p1.drużyna.append(p2)
        else:
            print("już jest")
    def dodaj_osoby_do_drużyny_oficjalnie(self, p1, p2, p3):
        if p1 not in p2.drużyna:
            p2.drużyna.append(p1)
        if p3 not in p2.drużyna:
            p2.drużyna.append(p3)
        if p1 not in p3.drużyna:
            p3.drużyna.append(p1)
        if p2 not in p3.drużyna:
            p3.drużyna.append(p2)
        if p3 not in p1.drużyna:
            p1.drużyna.append(p3)
        if p2 not in p1.drużyna:
            p1.drużyna.append(p2)
    def zaatakuj(self, wrog, jaka_czesc: str, walka: Walka):
        obrona_czesci = wrog.obrona[jaka_czesc]
        if self.chce or self.musi:
            if wrog in self.drużyna:
                walka.komunikat("chcesz zatakować swojego? co jest z tabą nie tak")
                return
            elif self.broń.tury > 0:
                self.broń.tury -= 1
                return
            elif self.broń.wytrzymałość == 0:
                walka.komunikat(f"{self.imie} nie może zaatakować, bo {self.bronie.nazwa} jest stępiona!")
                return
            elif jaka_czesc == "głowa" and randint(1, 100) != 1:
                walka.komunikat(f"{self.imie} chybił atak w głowę {wrog.imie}!")
                return
            elif wrog.istota == "goblin" and jaka_czesc == "głowa" and randint(1, 1000) != 1:
                walka.komunikat(f"{self.imie} chybił atak w głowę goblina o imieniu {wrog.imie}!")
                return
            elif self.broń.nazwa in ["włócznia", "ostra włócznia"]:
                for i in range(3):
                    if randint(1, wrog.szybkość) < self.szybkość_ataku:
                        walka.komunikat(f"{self.imie} uniknął ataku {wrog.imie}!")
                    obrazenia = max(0, randint(int(self.atak - (self.atak*0.1)), int(self.atak)) - obrona_czesci)
                    obrażenia_obrony = obrona_czesci*0.1
                    self.obrona[jaka_czesc] = max(0, self.obrona[jaka_czesc] - obrażenia_obrony)
                    aktualne_hp = getattr(wrog, jaka_czesc)
                    nowe_hp = max(0, aktualne_hp - obrazenia)
                    setattr(wrog, jaka_czesc, nowe_hp)
                    rzeczywiste_obrazenia = aktualne_hp - nowe_hp
                    wrog.ciało = max(0, wrog.ciało - rzeczywiste_obrazenia)
                    walka.komunikat(f"{wrog.imie} dostał {rzeczywiste_obrazenia} obrażeń w {jaka_czesc}!")
                    walka.komunikat(f"{wrog.imie} ma {nowe_hp} HP w {jaka_czesc}")
                if not self.broń.wytrzymałość == 0:
                    self.broń.wytrzymałość = max(0,self.broń.wytrzymałość - 1)
                if self.broń.wytrzymałość == 0:
                    walka.komunikat(f"{self.imie} nie może zaatakować, ponieważ {self.broń.nazwa} jest stępiona!")
                    return
            else:
                obrazenia = max(0, randint(int(self.atak - (self.atak * 0.1)), int(self.atak)) - obrona_czesci)
                obrażenia_obrony = obrona_czesci*0.1
                self.obrona[jaka_czesc] = max(0, self.obrona[jaka_czesc] - obrażenia_obrony)
                aktualne_hp = getattr(wrog, jaka_czesc)
                nowe_hp = max(0, aktualne_hp - obrazenia)
                setattr(wrog, jaka_czesc, nowe_hp)
                rzeczywiste_obrazenia = aktualne_hp - nowe_hp
                wrog.ciało = max(0, wrog.ciało - rzeczywiste_obrazenia)
                walka.komunikat(f"{wrog.imie} dostał {rzeczywiste_obrazenia} obrażeń w {jaka_czesc}!")
                walka.komunikat(f"{wrog.imie} ma {nowe_hp} HP w {jaka_czesc}")
            if not self.broń.wytrzymałość == 0:
                self.broń.wytrzymałość = max(0,self.broń.wytrzymałość - 1)
        else:
            if not self.chce:
                walka.komunikat("nie chcę atakować")
    def zyje(self):
        return self.ciało > 0 or self.głowa > 0
    def dodaj_artefakt(self, nazwa, wymuszony_slot):
            self.artefakty[wymuszony_slot] = nazwa
    def ma_artefakt(self, nazwa: str):
        return nazwa in self.artefakty.values()
    def użyj_wochuk(self):
        if not self.ma_artefakt("wochuk"):
            return f"{self.imie} nie posiada artefaktu Wochuk."
        for przeciwnik in self.wrogowie:
            użycia = self.wochuk_uses.get(przeciwnik, 0)
            szansa = max(0.5 - (użycia * 0.1), 0)
            if random() < szansa:
                przeciwnik.ogłuszony = True
                print(f"{przeciwnik.imie} został ogłuszony przez Wochuka!")
                self.wochuk_uses[przeciwnik] = użycia + 1
                self.czas_ogłuszenia = 3
            else:
                print(f"{przeciwnik.imie} oparł się działaniu Wochuka.")
    def użyj_cozwój(self, przeciwnik):
        if "cozwój" not in self.artefakty:
            return f"{self.imie} nie posiada artefaktu Cozwój."
        if self.cozwoj_uses >= 10:
            return f"{self.imie} zużył już cały artefakt Cozwój."
        self.cozwoj_uses += 1
        # Cofnięcie rozwoju: brak umiejętności
        przeciwnik.umiejętności = []
        return f"{przeciwnik.imie} został cofnięty do epoki kamienia łupanego!"
    def __str__(self):
        return f"{self.imie}({self.istota}):\n  Życie={self.ciało}\n  Atak={self.atak}\n  Obrona={self.obrona}\n  punkty oszczędzienia = {self.oszczędzenie}\n  broń: {self.broń.nazwa}\n  zbroja: {self.zbroja.nazwa}"
pos1 = Postać(
    "człowiek", "Tomek",
    200.0, 250.0, 50.0, 10.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    10.0, {"głowa": 10, "klatka": 10, "lręka": 5, "pręka": 0, "brzuch": 10, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("zbroja_z_błota_i_liści"),
    daj_bron("cięki_patyk"),
    True, False,
    0, 0,
    3,7,
    50, 50, -25, -25
)
pos2 = Postać(
    "Goblin", "Buzg",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    0.0, {"głowa": 100, "klatka": 200, "lręka": 150, "pręka": 150, "brzuch": 200, "lrzebro": 50, "przebro": 50, "lnoga": 300, "pnoga": 300, "ogon": 500},
    daj_zbroje("brak_zbroi"),
    daj_bron("topur"),
    False, True,
    0,0,
    1,4,
    100, 100, -50, -50
)
pos3 = Postać(
    "elf", "Elenor",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    8,7,
    50, 50, -25, -25
)
pos4 = Postać(
    "elf", "Romeo",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("czarno_zbroja"),
    daj_bron("łuk"),
    True, False,
    0,0,
    2,3,
    50, 50, -25, -25
)
pos5 = Postać(
    "elf", "Rukur",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True,
    0,0,
    7,8,
    50, 50, -25, -25
)
pos6 = Postać(
    "elf", "Rokil",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True,
    0,0,
    7,8,
    50, 50, -25, -25
)
pos7 = Postać(
    "Goblin", "Azyl",
    400.0, 500.0, 100.0, 100.0, 150.0, 25.0, 25.0, 350.0, 350.0,
    200.0, 300.0, 50.0, 100,
    0.0, {"głowa": 20, "klatka":40, "lręka": 30, "pręka": 30, "brzuch": 50, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    7,8,
    50, 50, -25, -25
)
pos8 = Postać(
    "Goblin", "Zazul",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    0.0, {"głowa": 20, "klatka":40, "lręka": 30, "pręka": 30, "brzuch": 50, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    7,8,
    50, 50, -25, -25
)
pos1.dodaj_relacje(pos3.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos1.dodaj_relacje("gracz", {"zaufanie": 0, "decyzje": []})
pos1.synchronizacja(1)
pos1.ekwipunek["ciękie patyki"] += 1
pos1.ekwipunek["kawałki metalu"] += 10
pos2.ogon = 1000000.0
pos2.części_ciała.append("ogon")
pos2.nczęści_ciała.append(pos2.ogon)
pos2.synchronizacja(3)
pos2.synchronizacja(1)
pos2.ekwipunek["siekiera"] += 1
pos3.dodaj_relacje(pos1.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos4.synchronizacja(1)
pos5.synchronizacja(1)
pos6.synchronizacja(1)
def zamien_czas(sekundy):
    rok = 365 * 24 * 60 * 60
    miesiac = 30 * 24 * 60 * 60
    dzien = 24 * 60 * 60
    godzina = 60 * 60
    minuta = 60

    lata = sekundy // rok
    sekundy %= rok

    miesiace = sekundy // miesiac
    sekundy %= miesiac

    dni = sekundy // dzien
    sekundy %= dzien

    godziny = sekundy // godzina
    sekundy %= godzina

    minuty = sekundy // minuta
    sekundy %= minuta

    return lata, miesiace, dni, godziny, minuty, sekundy
def gra():
    pygame.init()
    pygame.display.set_caption("Artefakty")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # ładowanie tła
    tlo = pygame.image.load("tlo.png").convert()
    tlo1 = pygame.image.load("tlo1.png").convert()
    tlo2 = pygame.image.load("tlo2.png").convert()
    tlo3 = pygame.image.load("tlo3.png").convert()
    tlo4 = pygame.image.load("tlo4.png").convert()
    tlo5 = pygame.transform.rotate(tlo3, 180)
    
    tlo1 = pygame.transform.scale(tlo1, (800, 600))
    tlo = pygame.transform.scale(tlo, (800, 600))
    tlo2 = pygame.transform.scale(tlo2, (800, 600))
    tlo3 = pygame.transform.scale(tlo3, (800, 600))
    tlo4 = pygame.transform.scale(tlo4, (800, 600))
    tlo5 = pygame.transform.scale(tlo5, (800, 600))
    speed = 3  # pixel po pixelu
    stamina = 100.0
    frame = 0
    player_idle1 = pygame.image.load("Tomek.png").convert_alpha()
    player_idle2 = pygame.image.load("Tomek5.png").convert_alpha()
    player_idle3 = pygame.image.load("Tomek8.png").convert_alpha()
    player_idle4 = pygame.image.load("Tomek9.png").convert_alpha()
    player_walk1 = pygame.image.load("Tomek1.png").convert_alpha()
    player_walk2 = pygame.image.load("Tomek2.png").convert_alpha()
    player_walk3 = pygame.image.load("Tomek3.png").convert_alpha()
    player_walk4 = pygame.image.load("Tomek4.png").convert_alpha()
    player_walk5 = pygame.image.load("Tomek6.png").convert_alpha()
    player_walk6 = pygame.image.load("Tomek7.png").convert_alpha()
    player_walk7 = pygame.image.load("Tomek10.png").convert_alpha()
    player_walk8 = pygame.image.load("Tomek11.png").convert_alpha()
    

    player_idle1 = pygame.transform.scale(player_idle1, (200, 200))
    player_idle2 = pygame.transform.scale(player_idle2, (200, 200))
    player_idle3 = pygame.transform.scale(player_idle3, (200, 200))
    player_idle4 = pygame.transform.scale(player_idle4, (200, 200))
    player_walk1 = pygame.transform.scale(player_walk1, (200, 200))
    player_walk2 = pygame.transform.scale(player_walk2, (200, 200))
    player_walk3 = pygame.transform.scale(player_walk3, (200, 200))
    player_walk4 = pygame.transform.scale(player_walk4, (200, 200))
    player_walk5 = pygame.transform.scale(player_walk5, (200, 200))
    player_walk6 = pygame.transform.scale(player_walk6, (200, 200))
    player_walk7 = pygame.transform.scale(player_walk7, (200, 200))
    player_walk8 = pygame.transform.scale(player_walk8, (200, 200))
    font = pygame.font.SysFont(None, 36)
    player = player_idle1

    # licznik czasu
    ostatnia_aktualizacja = time.time()

    lata = 390006
    miesiace = 5
    dni = 24
    godziny = 17
    minuty = 26
    sekundy = 36

    # Przeliczenie na sekundy (rok = 365 dni, miesiąc = 30 dni)
    calkowite_sekundy = (
        sekundy +
        (minuty * 60) +
        (godziny * 3600) +
        (dni * 86400) +
        (miesiace * 30 * 86400) +
        (lata * 365 * 86400)
    )

    lata, miesiace, dni, godziny, minuty, sekundy = zamien_czas(calkowite_sekundy) # Wyświetli: 12301244312396
    while True:
        a = 10  # domyślna szybkość animacji

        # aktualizacja co 60 sekund realnego czasu
        aktualny_czas = int(time.time())

        # aktualizacja co 60 sekund realnego czasu
        if aktualny_czas - ostatnia_aktualizacja >= 1:
            calkowite_sekundy += 1
            ostatnia_aktualizacja = aktualny_czas

            lata, miesiace, dni, godziny, minuty, sekundy = zamien_czas(calkowite_sekundy)
        camera_x = pos1.x - 280
        camera_y = pos1.y - 220
        keys = pygame.key.get_pressed()
        lista = [
            keys[pygame.K_w],
            keys[pygame.K_UP],
            keys[pygame.K_s],
            keys[pygame.K_DOWN],
            keys[pygame.K_a],
            keys[pygame.K_RIGHT],
            keys[pygame.K_d],
            keys[pygame.K_LEFT]
        ]
        moving = any(lista)

        if moving:
            frame += 1
        if keys[pygame.K_LSHIFT] and stamina > 1:
            a = 4
        b = a*2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if not moving:
            frame = 0
            if player in [player_walk1, player_walk2]:
                player = player_idle1
            if player in [player_walk3, player_walk4]:
                player = player_idle2
            if player in [player_walk5, player_walk6]:
                player = player_idle3
            if player in [player_walk7, player_walk8]:
                player = player_idle4
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos1.x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos1.x += speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos1.y += speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos1.y -= speed
        else:
            pass
        pos1.aktualizuj_hitbox()
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if frame < a/2:
                player = player_walk3
            if frame > a/2:
                player = player_walk4
            if frame >= a:
                player = player_walk3
                frame = 0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if frame < a/2:
             player = player_walk1
            if frame > a/2:
                player = player_walk2
            if frame >= a:
                frame = 0
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if frame <= b/4:
                player = player_walk7
            if frame > b/4 and frame < b/2:
                player = player_idle4
            if frame >= b/2 and frame < b:
                player = player_walk8
            if frame >= b:
                player = player_walk7
                frame = 0               
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if frame <= b/5:
                player = player_walk5
            if frame > b/5 and frame < b/2:
                player = player_idle3
            if frame >= b/2 and frame < b:
                player = player_walk6
            elif frame >= b:
                player = player_walk5
                frame = 0
        else:
            pass

        if keys[pygame.K_q]:
            pygame.quit()
            exit()
        else:
            pass
        if keys[pygame.K_LSHIFT] and stamina > 0 and any(lista):
            speed = pos1.szybkość+5            
            stamina -= 0.05
        elif (not keys[pygame.K_LSHIFT] or stamina <= 0):
            speed = pos1.szybkość
            stamina += 0.001
        else:
            pass    
        if stamina > 100:
            stamina = 100
        elif stamina <= -1:
            stamina = -1
        # czarne tło mapy
        screen.fill((0, 0, 0))

        # pozycja jednego tła na mapie
        tlo_x = -280
        tlo_y = -220
        tlo_y1 = tlo_y + 600
        tlo_y2 = tlo_y1 + 600
        tlo_y3 = tlo_y2 + 600
        tlo_y4 = tlo_y3 + 600
        tlo_x1 = tlo_x + 800
        tlo_x2 = tlo_x - 800
        # rysowanie jednego tła
        screen.blit(tlo, (tlo_x - camera_x, tlo_y - camera_y))
        screen.blit(tlo1, (tlo_x - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo3, (tlo_x - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo4, (tlo_x - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x1 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo5, (tlo_x2 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo2, (tlo_x2 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x1 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x - camera_x, tlo_y4 - camera_y))
        screen.blit(player, (pos1.x - camera_x, pos1.y - camera_y))
        
        pygame.draw.rect(screen,(100, 100, 100), (10, 50, 200, 20))

        tekst_czas = font.render(f"czas: {lata} l. {miesiace} mies. {dni} d. {godziny} godz. {minuty} min. {sekundy} sek.", True, (255, 255, 255)) 
        położenie_gracza = font.render(f"pozycja: ({pos1.x}, {pos1.y})", True, (255, 255, 255)) 
        screen.blit(tekst_czas, (10, 10))
        screen.blit(położenie_gracza, (10, 80))

        # aktualna stamina
        pygame.draw.rect(screen, (0, 0, 255), (10, 50, 2 * stamina, 20))
        pygame.display.update()
        clock.tick(60)
gra()