#jest 21040 Goblinów, 754 wróżek, 27504 ludzi i 25357 elfów na całym świecie. grze będzie mniej. 
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
        self.nazwa = nazwa.split("|")
        self.obrona = obrona
        self.atak = atak
        self.tury = tury
        self.wytrzymałość = wytrzymałość

    def po(self):
        return {"nazwa": self.nazwa,
                "obrona": self.obrona,
                "atak": self.atak,
                "tury": self.tury,
                "wytrzymałość": self.wytrzymałość}

    def wczytaj(self, wnazwa, wobrona, watak, wtury, wwytrzymałość):
        self.nazwa = wnazwa
        self.obrona = wobrona
        self.atak = watak
        self.tury = wtury
        self.wytrzymałość = wwytrzymałość

zbroje_def = {
    "czarno_zbroja": ("czarno zbroja", {"głowa":0, "klatka":20, "lręka":5, "pręka":5, "brzuch":20, "lrzebro":10, "przebro":10, "lnoga":0, "pnoga":0}, (5,10), 0, (100, 150)),
    "brak_zbroi": ("brak zbroi", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (0,0), 0, (0, 0)),
    "jasno_zbroja": ("jasno zbroja", {"głowa":20, "klatka":20, "lręka":10, "pręka":10, "brzuch":30, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (0,0), 0, (100, 120)),
    "łuska_smoka": ("łuska smoka", {"głowa":0, "klatka":300, "lręka":0, "pręka":0, "brzuch":500, "lrzebro":50, "przebro":50, "lnoga":0, "pnoga":0}, (400,500), 0, (500, 500)),
    "sdz_metalowa_zbroja": ("sdz metalowa zbroja", {"głowa":40, "klatka":50, "lręka":10, "pręka":10, "brzuch":50, "lrzebro":40, "przebro":40, "lnoga":60, "pnoga":60}, (0,0), 0, (10, 50)),
    "metalowa_zbroja": ("metalowa zbroja", {"głowa":50, "klatka":100, "lręka":70, "pręka":70, "brzuch":120, "lrzebro":100, "przebro":100, "lnoga":80, "pnoga":80}, (0,0), 0, (100, 150)),
    "zbroja_z_błota_i_liści": ("zbroja z błota i liści", {"głowa":0, "klatka":5, "lręka":0, "pręka":0, "brzuch":10, "lrzebro":1, "przebro":1, "lnoga":5, "pnoga":5}, (0,0), 0, (10, 20))
}

bronie_def = {
    "brak_broni": ("brak broni", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (0, 0), 0, (0, 0)),
    "łuk": ("łuk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (30,50), 0, (50, 100)),
    "topur": ("topur", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (450,500), 0, (500, 500)),
    "włócznia": ("włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (20, 60), 0, (100, 200)),
    "ostra_włócznia": ("ostra włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (50, 100), 0, (100, 150)),
    "cięki_patyk": ("cięki patyk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, (20, 30), 0, (10, 20))
}

def stworz_przedmiot(definicja):
    nazwa, obrona, (min_atak, max_atak), tury, (min_w, max_w) = definicja
    atak = randint(min_atak, max_atak)
    wytrzymałość = randint(min_w, max_w)
    return dodanie_stat(nazwa, obrona, atak, tury, wytrzymałość)

def daj_zbroje(nazwa):
    return stworz_przedmiot(zbroje_def[nazwa])

def daj_bron(nazwa):
    return stworz_przedmiot(bronie_def[nazwa])

class Postać:
    wróżki = {"ludność wróżek": 0}
    ludzie = {"ludność ludzi": 0, "Ludność ludzi dołączonych do spiczastych jastrzębi": 0,"Ludność ludzi dołączonych do skalnych rycerzy/wędrowców": 0, "ludność ludzi dołączonych do obu szkół": 0}
    elfy = {"ludność elfów": 0}
    gobliny = {"ludność goblinów": 0, "ludność ocalonych goblinów": 0, "ludność cyklistów": 0, "cała ludność ocalonych goblinów": 0, "ludność przeklętych goblinów": 0, "ludność łowców": 0, "ludność ocalonych poprostu żyjących goblinów": 0, "ludność naiwnych łowców": 0, "ludność nie naiwnych łowców": 0, "ludność łowców z sensem": 0, "ludność przeklętych łowców": 0, "ludność przeklętych goblinów nie będących łowcami": 0}
    żywi = []
    polegli = []

    def __init__(self, istota, typ, materiał, imie, Nazwisko, głowa, klatka, lręka, pręka, brzuch, lrzebro, przebro, lnoga, pnoga, napojenie, mnapojenie, głód, mgłód, atak, obrona, zbroja, broń, chce_zatakować, musi, x, y, szybkość, szybkość_ataku, hitbox_w, hitbox_h, offset_x, offset_y):
        self.lista_typów = [t.strip() for t in typ.split(",")]
        self.imie = imie
        self.Nazwisko = Nazwisko
        self.głód = głód
        self.mgłód = mgłód
        self.napojenie = napojenie
        self.mnapojenie = mnapojenie
        self.istota = istota
        
        self.życie = {
            "głowa": głowa,
            "klatka": klatka,
            "lręka": lręka,
            "pręka": pręka,
            "brzuch": brzuch,
            "lrzebro": lrzebro,
            "przebro": przebro,
            "lnoga": lnoga,
            "pnoga": pnoga
        }
        
        self.artefakty = {1: None, 2: None, 3: None}
        self.za_atak = atak
        self.za_obrona = obrona
        self.atak = atak
        self.obrona = obrona
        self.zbroja = zbroja
        self.broń = broń
        self.umiejętności = []
        
        self.ciało = sum(self.życie.values())
        self.części_ciała = list(self.życie.keys())
        
        self.ogłuszony = False
        self.czas_ogłuszenia = 0
        self.chce = chce_zatakować
        self.musi = musi
        self.tury = broń.tury
        self.drużyna = []
        self.wrogowie = []
        self.ekwipunek = {"ciękie patyki": 0, "kamienie": 0, "kawałki metalu": 0, "siekiera": 0}
        self.oszczędzenie = 0
        self.relacje = {}
        
        self.wochuk_uses = {}
        self.cozwoj_uses = 0
        
        self.x = x
        self.y = y
        self.szybkość = szybkość
        self.szybkość_ataku = szybkość_ataku
        
        self.hitbox_w = hitbox_w
        self.hitbox_h = hitbox_h
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.hitbox = pygame.Rect(self.x + self.offset_x, self.y + self.offset_y, self.hitbox_w, self.hitbox_h)
        self.maska = pygame.Mask((self.hitbox_w, self.hitbox_h), fill=True)

        gęstość = 1000
        if materiał == "kreda":
            gęstość = 2800
        elif materiał == "Tytan":
            gęstość = 4500
        elif materiał == "lód":
            gęstość = 920
        elif materiał == "Popiół":
            gęstość = 500
        elif materiał == "Kamień":
            gęstość = 2650

        self.kg = 0.0
        self.objętość_części = {}

        for część, hp in self.życie.items():
            def_punkty = self.za_obrona.get(część, 0)
            kg_części = (hp / 100) + (def_punkty / 10)

            m3 = kg_części / gęstość
            cm3 = m3 * 1_000_000
            km3 = m3 / 1_000_000_000

            self.objętość_części[część] = {
                "kg": kg_części,
                "m3": m3,
                "cm3": cm3,
                "km3": km3
            }

            self.kg += kg_części

        self.objętość = self.kg / gęstość
        
        self.N = self.atak * 20
        Postać.żywi.append(self)
        if istota == "wróżka":
            Postać.wróżki["ludność wróżek"] += 1
        elif istota == "elf":
            Postać.elfy["ludność elfów"] += 1
        elif istota == "człowiek":
            Postać.ludzie["ludność ludzi"] += 1
            if "szkoła spiczastych jastrząbi" in self.lista_typów:
                Postać.ludzie["Ludność ludzi dołączonych do spiczastych jastrzębi"] += 1
            if "szkoła skalnych rycerzy/wędrowców" in self.lista_typów:
                Postać.ludzie["Ludność ludzi dołączonych do skalnych rycerzy/wędrowców"] += 1
            if "oba szkoły" in self.lista_typów:
                Postać.ludzie["ludność ludzi dołączonych do obu szkół"] += 1
                Postać.ludzie["Ludność ludzi dołączonych do spiczastych jastrzębi"] += 1
                Postać.ludzie["Ludność ludzi dołączonych do skalnych rycerzy/wędrowców"] += 1
        elif istota == "Goblin":
            Postać.gobliny["ludność goblinów"] += 1
            if "ocalały" in self.lista_typów:
                Postać.gobliny["ludność ocalonych goblinów"] += 1
            if "cyklista" in self.lista_typów:
                Postać.gobliny["ludność cyklistów"] += 1
                Postać.gobliny["cała ludność ocalonych goblinów"] += 1

    def aktualizuj_hitbox(self):
        self.hitbox.x = self.x + self.offset_x
        self.hitbox.y = self.y + self.offset_y

    def synchronizacja(self, protokuł: int):
        if protokuł == 3:
            self.ciało = sum(self.życie.values())
        elif protokuł == 2:
            self.głód = max(0, min(self.głód, self.mgłód))
            self.napojenie = max(0, min(self.napojenie, self.mnapojenie))
            self.oszczędzenie = max(0, min(self.oszczędzenie, 100))
        elif protokuł == 1:
            self.obrona = self.za_obrona.copy()
            self.atak = self.za_atak
            if self.istota == "goblin":
                if self.zbroja.nazwa not in ["łuska smoka", "brak zbroi"]:
                    return
            else:
                if self.zbroja.nazwa == "łuska smoka":
                    return
            if self.zbroja is not None:
                for część in self.obrona:
                    self.obrona[część] += self.zbroja.obrona.get(część, 0)
                self.atak += self.zbroja.atak
            if self.broń is not None:
                self.atak += self.broń.atak

w = 400
k = 50
pos1 = Postać(
    "człowiek", "oba szkoły","kreda", "Tomek", "Kowalski",
    200.0, 250.0, 50.0, 10.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    25, {"głowa": 10, "klatka": 10, "lręka": 5, "pręka": 0, "brzuch": 10, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("zbroja_z_błota_i_liści"),
    daj_bron("cięki_patyk"),
    True, False,
    45784.0*w, 25620.0*-1*w,
    2,7,
    50, 50, -25, -25
)
pos2 = Postać(
    "Goblin", "cyklista, typ4", "Tytan", "Buzg", "Zigug",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    300.0, {"głowa": 100, "klatka": 200, "lręka": 150, "pręka": 150, "brzuch": 200, "lrzebro": 50, "przebro": 50, "lnoga": 300, "pnoga": 300, "ogon": 500},
    daj_zbroje("brak_zbroi"),
    daj_bron("topur"),
    False, True,
    0,0,
    2.5,4,
    100, 100, -50, -50
)
pos3 = Postać(
    "elf","nie ma typu", "lód", "Elenor", "Lindholm",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    20,7,
    50, 50, -25, -25
)
pos4 = Postać(
    "elf","nie ma typu", "Romeo", "Monteculsi",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("czarno_zbroja"),
    daj_bron("łuk"),
    True, False,
    0,0,
    20,8,
    50, 50, -25, -25
)
pos5 = Postać(
    "elf","nie ma typu", "Rukur", "Ragnarsson",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True,
    0,0,
    20,8,
    50, 50, -25, -25
)
pos6 = Postać(
    "elf","nie ma typu", "Rokil", "Ragnarsson",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True,
    0,0,
    20,8,
    50, 50, -25, -25
)
pos7 = Postać(
    "Goblin","cyklista, typ2", "Azyl","Lazur",
    400.0, 500.0, 100.0, 100.0, 150.0, 25.0, 25.0, 350.0, 350.0,
    200.0, 300.0, 50.0, 100,
    100.0, {"głowa": 20, "klatka":40, "lręka": 30, "pręka": 30, "brzuch": 50, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    20,8,
    50, 50, -25, -25
)
pos8 = Postać(
    "Goblin", "ocalały", "Zazul", "Zigug",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    300.0, {"głowa": 20, "klatka":40, "lręka": 30, "pręka": 30, "brzuch": 50, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    20,8,
    50, 50, -25, -25
)
pos9 = Postać(
    "człowiek", "szkoła spiczastych jastrząbi", "Koralina", "Kowalska",
    5000.0, 6250.0, 1250.0, 1250.0, 1875.0, 312.5, 312.5, 4375.0, 4375.0,
    100.0, 100.0, 100.0, 100.0,
    125.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    10,7,
    50, 50, -25, -25
)
pos10 = Postać(
    "człowiek", "szkoła skalnych rycerzy/wędrowców", "Kamil", "Radziński",
    5000.0, 6250.0, 1250.0, 1250.0, 1875.0, 312.5, 312.5, 4375.0, 4375.0,
    100.0, 100.0, 100.0, 100.0,
    125.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False,
    0,0,
    10,7,
    50, 50, -25, -25
)

pos1.dodaj_relacje(pos3.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos1.dodaj_relacje("gracz", {"zaufanie": 0, "decyzje": []})
pos1.synchronizacja(1)
pos1.ekwipunek["ciękie patyki"] += 1
pos1.ekwipunek["kawałki metalu"] += 10

# Obsługa dodania nowej części ciała w słowniku
pos2.życie["ogon"] = 1000000.0
pos2.części_ciała.append("ogon")
pos2.synchronizacja(3)
pos2.synchronizacja(1)
pos2.ekwipunek["siekiera"] += 1

pos3.dodaj_relacje(pos1.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos4.synchronizacja(1)
pos5.synchronizacja(1)
pos6.synchronizacja(1)
pos1.synchronizacja(1)

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

class Przeszkoda:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.maska = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.points = self.maska.outline()

    def sprawdz_kolizje(self, postac):
        offset = (int(self.x - postac.hitbox.x), int(self.y - postac.hitbox.y))
        return postac.maska.overlap(self.maska, offset) is not None

    def rysuj_obrys(self, screen, camera_x, camera_y):
        if len(self.points) > 1:
            punkty_ekranowe = [(p[0] + self.x - camera_x, p[1] + self.y - camera_y) for p in self.points]
            pygame.draw.lines(screen, (0, 255, 0), True, punkty_ekranowe, 2)

# --- KLASA ŚCIANA DLA NIEWIDZIALNYCH SKOŚNYCH BARIER ---
class Ściana:
    def __init__(self, punkty):
        self.punkty = punkty
        
        min_x = min(p[0] for p in punkty)
        max_x = max(p[0] for p in punkty)
        min_y = min(p[1] for p in punkty)
        max_y = max(p[1] for p in punkty)
        
        self.x = min_x
        self.y = min_y
        szerokosc = max_x - min_x
        wysokosc = max_y - min_y

        punkty_lokalne = [(p[0] - min_x, p[1] - min_y) for p in punkty]

        powierzchnia = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
        pygame.draw.polygon(powierzchnia, (255, 255, 255), punkty_lokalne)

        self.maska = pygame.mask.from_surface(powierzchnia)

    def sprawdz_kolizje(self, postac):
        offset = (int(self.x - postac.hitbox.x), int(self.y - postac.hitbox.y))
        return postac.maska.overlap(self.maska, offset) is not None

    def rysuj_obrys(self, screen, camera_x, camera_y):
        punkty_ekranowe = [(p[0] - camera_x, p[1] - camera_y) for p in self.punkty]
        pygame.draw.polygon(screen, (0, 255, 0), punkty_ekranowe, 2)

def gra():
    pygame.init()
    pygame.display.set_caption("Artefakty")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    def rozmiar_boxu(rozb, nazwa):
        box1 = pygame.image.load("box.png").convert_alpha()
        box1 = pygame.transform.scale(box1, (rozb, rozb))
        box = {
            "box1": pygame.transform.scale(box1, (rozb, rozb)),
            "box2": pygame.transform.rotate(box1, 45),
            "box3": pygame.transform.rotate(box1, 90),
            "box4": pygame.transform.rotate(box1, 135),
            "box5": pygame.transform.rotate(box1, 180),
            "box6": pygame.transform.rotate(box1, 225),
            "box7": pygame.transform.rotate(box1, 270)
        }
        return box[nazwa]
        
    def rozmiar_deski(rozd, nazwa):
        deska1 = pygame.image.load("deska.png").convert_alpha()
        deska1 = pygame.transform.scale(deska1, (rozd, rozd/2))
        deska = {
            "deska1": pygame.transform.scale(deska1, (rozd, rozd/2)),
            "deska2": pygame.transform.rotate(deska1, 45),
            "deska3": pygame.transform.rotate(deska1, 90),
            "deska4": pygame.transform.rotate(deska1, 135),
            "deska5": pygame.transform.rotate(deska1, 180),
            "deska6": pygame.transform.rotate(deska1, 225),
            "deska7": pygame.transform.rotate(deska1, 270)
        }
        return deska[nazwa]

    deska1 = rozmiar_deski(388, "deska1")
    deska2 = rozmiar_deski(216, "deska7")
    deska3 = rozmiar_deski(384, "deska4")
    
    img_box1 = rozmiar_boxu(252.252, "box1")
    img_box2 = rozmiar_boxu(251.5, "box2")
    img_box3 = rozmiar_boxu(252.452, "box4")
    img_box4 = rozmiar_boxu(250.1, "box1")
    img_box5 = rozmiar_boxu(253.645, "box1")
    
    tlo = pygame.image.load("tlo.png").convert()
    tlo1 = pygame.image.load("tlo1.png").convert()
    tlo2 = pygame.image.load("tlo2.png").convert()
    tlo3 = pygame.image.load("tlo3.png").convert()
    tlo4 = pygame.image.load("tlo4.png").convert()
    tlo5 = pygame.transform.rotate(tlo3, 180)
    tlo6 = pygame.image.load("tlo5.png").convert()
    tlo7 = pygame.image.load("tlo6.png").convert()
    tlo8 = pygame.transform.rotate(tlo7, 180)
    tlo9 = pygame.image.load("tlo7.png").convert()
    tlo10 = pygame.transform.rotate(tlo7, 90)
    tlo11 = pygame.transform.rotate(tlo9, 90)
    tlo12 = pygame.transform.rotate(tlo9, 270)
    tlo13 = pygame.transform.rotate(tlo7, 270)
    tlo14 = pygame.transform.rotate(tlo9, 180)
    tlo15 = pygame.image.load("tlo8.png").convert()
    tlo16 = pygame.image.load("tlo9.png").convert()
    tlo17 = pygame.transform.rotate(tlo15, 90)
    tlo18 = pygame.transform.rotate(tlo15, 180)
    tlo19 = pygame.transform.rotate(tlo15, 270)
    
    tlo = pygame.transform.scale(tlo, (800, 600))
    tlo1 = pygame.transform.scale(tlo1, (800, 600))
    tlo2 = pygame.transform.scale(tlo2, (800, 600))
    tlo3 = pygame.transform.scale(tlo3, (800, 600))
    tlo4 = pygame.transform.scale(tlo4, (800, 600))
    tlo5 = pygame.transform.scale(tlo5, (800, 600))
    tlo6 = pygame.transform.scale(tlo6, (800, 600))
    tlo7 = pygame.transform.scale(tlo7, (800, 600))
    tlo8 = pygame.transform.scale(tlo8, (800, 600))
    tlo9 = pygame.transform.scale(tlo9, (800, 600))
    tlo10 = pygame.transform.scale(tlo10, (800, 600))
    tlo11 = pygame.transform.scale(tlo11, (800, 600))
    tlo12 = pygame.transform.scale(tlo12, (800, 600))
    tlo13 = pygame.transform.scale(tlo13, (800, 600))
    tlo14 = pygame.transform.scale(tlo14, (800, 600))
    tlo15 = pygame.transform.scale(tlo15, (800, 600))
    tlo16 = pygame.transform.scale(tlo16, (800, 600))
    tlo17 = pygame.transform.scale(tlo17, (800, 600))
    tlo18 = pygame.transform.scale(tlo18, (800, 600))
    tlo19 = pygame.transform.scale(tlo19, (800, 600))
    
    speed = pos1.szybkość * w / k
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

    ostatnia_aktualizacja = time.time()
    lata, miesiace, dni, godziny, minuty, sekundy = 390006, 5, 24, 17, 26, 35

    calkowite_sekundy = (
        sekundy + (minuty * 60) + (godziny * 3600) +
        (dni * 86400) + (miesiace * 30 * 86400) + (lata * 365 * 86400)
    )

    wx = pos1.x
    wy = pos1.y
    
    tb_x = wx - 280
    tb_y = wy - 220
    tb_y1 = tb_y + 600
    tb_y2 = tb_y1 + 600
    tb_y3 = tb_y2 + 600
    tb_y4 = tb_y3 + 600
    tb_x3 = tb_x - 1600
    tb_x4 = tb_x + 1600

    przeszkody = [
        Przeszkoda(tb_x3 + 250, tb_y1 + 300, img_box1),
        Przeszkoda(tb_x3 + 230, tb_y3 - 150, img_box2),
        Przeszkoda(tb_x3 + 240, tb_y4 + 56,  img_box3),
        Przeszkoda(tb_x4 + 310, tb_y1 + 300, img_box4),
        Przeszkoda(tb_x4 + 310, tb_y3 - 300, img_box5),
    ]

    # --- DEFINIOWANIE NIEWIDZIALNYCH ŚCIAN NA MAPIE ---
    # Prosta pionowa ściana (lewy górny róg w punkcie X=500, Y=300)
    sciany = [
    # Ściana odsunięta o 600 px w prawo i 100 px w dół od lewego rogu kamery
    Ściana([
        (tb_x + 640, tb_y + 380), 
        (tb_x + 650, tb_y + 380), 
        (tb_x + 650, tb_y + 600), 
        (tb_x + 640, tb_y + 600)
    ]),
    Ściana([
        (tb_x + 160, tb_y + 400), 
        (tb_x + 190, tb_y + 400), 
        (tb_x + 190, tb_y + 600), 
        (tb_x + 160, tb_y + 600)
    ])
    ]
    
    while True:
        a = 10
        aktualny_czas = int(time.time())

        if aktualny_czas - ostatnia_aktualizacja >= 0.5:
            calkowite_sekundy += 1
            ostatnia_aktualizacja = aktualny_czas
            lata, miesiace, dni, godziny, minuty, sekundy = zamien_czas(calkowite_sekundy)
            
        camera_x = pos1.x - 280
        camera_y = pos1.y - 220
        keys = pygame.key.get_pressed()
        moving = any([keys[k] for k in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_LEFT)])

        if moving:
            frame += 1
        if keys[pygame.K_LSHIFT] and stamina > 1:
            a = 4
        b = a * 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if not moving:
            frame = 0
            if player in [player_walk1, player_walk2]: player = player_idle1
            if player in [player_walk3, player_walk4]: player = player_idle2
            if player in [player_walk5, player_walk6]: player = player_idle3
            if player in [player_walk7, player_walk8]: player = player_idle4

        stara_x = pos1.x
        stara_y = pos1.y

        # Ruch X + sprawdzanie kolizji ze skrzynkami i ścianami
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: pos1.x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: pos1.x += speed
        pos1.aktualizuj_hitbox()

        for p in przeszkody:
            if p.sprawdz_kolizje(pos1):
                pos1.x = stara_x
                pos1.aktualizuj_hitbox()
                break

        for s in sciany:
            if s.sprawdz_kolizje(pos1):
                pos1.x = stara_x
                pos1.aktualizuj_hitbox()
                break

        # Ruch Y + sprawdzanie kolizji ze skrzynkami i ścianami
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: pos1.y += speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: pos1.y -= speed
        pos1.aktualizuj_hitbox()

        for p in przeszkody:
            if p.sprawdz_kolizje(pos1):
                pos1.y = stara_y
                pos1.aktualizuj_hitbox()
                break

        for s in sciany:
            if s.sprawdz_kolizje(pos1):
                pos1.y = stara_y
                pos1.aktualizuj_hitbox()
                break

        # Animacje
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player = player_walk3 if frame < a/2 else player_walk4
            if frame >= a: frame = 0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player = player_walk1 if frame < a/2 else player_walk2
            if frame >= a: frame = 0
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if frame <= b/4: player = player_walk7
            elif frame < b/2: player = player_idle4
            elif frame < b: player = player_walk8
            else: player = player_walk7; frame = 0
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if frame <= b/5: player = player_walk5
            elif frame < b/2: player = player_idle3
            elif frame < b: player = player_walk6
            else: player = player_walk5; frame = 0

        if keys[pygame.K_q]:
            pygame.quit()
            exit()

        if keys[pygame.K_LSHIFT] and stamina > 0 and moving:
            speed = pos1.szybkość + 1 * (w / k)
            stamina -= 0.05
        elif not moving:
            speed = pos1.szybkość * w / k
            stamina += 0.01
        elif moving:
            stamina += 0.005
            
        stamina = max(-1.0, min(100.0, stamina))

        screen.fill((0, 0, 0))

        tlo_x = wx - 280
        tlo_y = wy - 220
        tlo_y1 = tlo_y + 600
        tlo_y2 = tlo_y1 + 600
        tlo_y3 = tlo_y2 + 600
        tlo_y4 = tlo_y3 + 600
        tlo_y5 = tlo_y4 + 600
        tlo_y6 = tlo_y5 + 600
        tlo_y7 = tlo_y5 + 300
        tlo_y8 = tlo_y6 + 600
        tlo_x1 = tlo_x + 800
        tlo_x2 = tlo_x - 800
        tlo_x3 = tlo_x2 - 800
        tlo_x4 = tlo_x1 + 800
        tlo_x5 = tlo_x2 + 400

        # Rysowanie tła
        screen.blit(tlo, (tlo_x - camera_x, tlo_y - camera_y))
        screen.blit(tlo1, (tlo_x - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo7, (tlo_x2 - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo7, (tlo_x1 - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo3, (tlo_x - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo4, (tlo_x - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x1 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo5, (tlo_x2 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo9, (tlo_x3 - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo10, (tlo_x3 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo10, (tlo_x3 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo11, (tlo_x3 - camera_x, tlo_y4 - camera_y))
        screen.blit(tlo12, (tlo_x4 - camera_x, tlo_y1 - camera_y))
        screen.blit(tlo13, (tlo_x4 - camera_x, tlo_y2 - camera_y))
        screen.blit(tlo14, (tlo_x4 - camera_x, tlo_y4 - camera_y))
        screen.blit(tlo13, (tlo_x4 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo8, (tlo_x2 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x2 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo2, (tlo_x1 - camera_x, tlo_y3 - camera_y))
        screen.blit(tlo6, (tlo_x - camera_x, tlo_y4 - camera_y))
        screen.blit(tlo8, (tlo_x2 - camera_x, tlo_y4 - camera_y))
        screen.blit(tlo8, (tlo_x1 - camera_x, tlo_y4 - camera_y))
        screen.blit(tlo6, (tlo_x - camera_x, tlo_y5 - camera_y))
        screen.blit(tlo8, (tlo_x - camera_x, tlo_y6 - camera_y))
        screen.blit(tlo10, (tlo_x2 - camera_x, tlo_y6 - camera_y))
        screen.blit(tlo13, (tlo_x1 - camera_x, tlo_y6 - camera_y))
        screen.blit(tlo12, (tlo_x1 - camera_x, tlo_y5 - camera_y))
        screen.blit(tlo9, (tlo_x2 - camera_x, tlo_y5 - camera_y))
        screen.blit(deska1, (tlo_x5 - camera_x, tlo_y7 - camera_y))
        screen.blit(deska3, ((tlo_x5 - 20) - camera_x, (tlo_y7 - 100) - camera_y))
        screen.blit(deska2, (tlo_x5 - camera_x, tlo_y7 - camera_y))
        screen.blit(tlo17, (tlo_x2 - camera_x, tlo_y8 - camera_y))
        screen.blit(tlo19, (tlo_x1 - camera_x, tlo_y8 - camera_y))
        screen.blit(tlo2, (tlo_x - camera_x, tlo_y8 - camera_y))
        screen.blit(tlo19, (tlo_x3 - camera_x, tlo_y8 - camera_y))

        # Rysowanie skrzynek
        for p in przeszkody:
            screen.blit(p.image, (p.x - camera_x, p.y - camera_y))

        # Rysowanie gracza
        screen.blit(player, (pos1.x - camera_x, pos1.y - camera_y))

        # Rysowanie obrysów skrzynek, gracza oraz ścian (debug)
        pygame.draw.rect(screen, (255, 0, 0), (pos1.hitbox.x - camera_x, pos1.hitbox.y - camera_y, pos1.hitbox.w, pos1.hitbox.h), 2)
        for p in przeszkody:
            p.rysuj_obrys(screen, camera_x, camera_y)

        for s in sciany:
            s.rysuj_obrys(screen, camera_x, camera_y)

        tekst_czas = font.render(f"czas: {lata} l. {miesiace} mies. {dni} d. {godziny} godz. {minuty} min. {sekundy} sek.", True, (255, 255, 255)) 
        położenie_gracza = font.render(f"pozycja: ({pos1.x/w}, {(pos1.y*-1)/w})", True, (255, 255, 255))
        screen.blit(tekst_czas, (10, 10))
        screen.blit(położenie_gracza, (10, 80))

        pygame.draw.rect(screen, (0, 0, 255), (10, 50, 2 * stamina, 20))
        pygame.display.update()
        clock.tick(k)
        pygame.display.set_caption(f"Artefakty | FPS: {int(clock.get_fps())}")

gra()