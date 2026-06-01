# --- STAN: PRZED RZEZIĄ ---
ludność_goblinów = 21040
ludność_ocalałych_goblinów = 2099
ludność_cyklistów = 5
cała_ludność_ocalałych_goblinów = ludność_ocalałych_goblinów + ludność_cyklistów
ludność_przeklętych_goblinów = ludność_goblinów - ludność_ocalałych_goblinów - ludność_cyklistów
ludność_łowców = 435
ludność_ocalałych_poprostu_żyjących = ludność_ocalałych_goblinów - ludność_łowców
ludność_naiwnych_łowców = ludność_łowców - 53
ludność_nie_naiwnych_łowców = 3
ludność_łowców_z_sensem = ludność_naiwnych_łowców + ludność_nie_naiwnych_łowców
ludność_przeklętych_łowców = 50
ludność_przeklętych_goblinów_nie_będących_łowcami = ludność_przeklętych_goblinów - ludność_przeklętych_łowców

def pokaż_g():
    global ludność_goblinów, ludność_ocalałych_goblinów, ludność_cyklistów, cała_ludność_ocalałych_goblinów, ludność_przeklętych_goblinów, ludność_łowców, ludność_ocalałych_poprostu_żyjących, ludność_naiwnych_łowców, ludność_nie_naiwnych_łowców, ludność_łowców_z_sensem, ludność_przeklętych_łowców, ludność_przeklętych_goblinów_nie_będących_łowcami
    
    statystyki_goblinów = {
        "ludność goblinów": ludność_goblinów,
        "ludność ocalonych goblinów": ludność_ocalałych_goblinów,
        "ludność cyklistów": ludność_cyklistów,
        "cała ludność ocalonych goblinów": cała_ludność_ocalałych_goblinów,
        "ludność przeklętych goblinów": ludność_przeklętych_goblinów,
        "ludność łowców": ludność_łowców,
        "ludność ocalonych poprostu żyjących goblinów": ludność_ocalałych_poprostu_żyjących,
        "ludność naiwnych łowców": ludność_naiwnych_łowców,
        "ludność nie naiwnych łowców": ludność_nie_naiwnych_łowców,
        "ludność łowców z sensem": ludność_łowców_z_sensem,
        "ludność przeklętych łowców": ludność_przeklętych_łowców,
        "ludność przeklętych goblinów nie będących łowcami": ludność_przeklętych_goblinów_nie_będących_łowcami,
        
        "stosunek cyklistów na całą ludność": f"{ludność_cyklistów / ludność_goblinów * 100:.2f}%",
        "stosunek ocalonych goblinów na całą ludność": f"{ludność_ocalałych_goblinów / ludność_goblinów * 100:.2f}%",
        "stosunek łowców na całą ludność": f"{ludność_łowców / ludność_goblinów * 100:.2f}%",
        "stosunek łowców na ocalonych Goblinów": f"{ludność_łowców / ludność_ocalałych_goblinów * 100:.2f}%",
        "stosunek przeklętych Goblinów na całą ludność": f"{ludność_przeklętych_goblinów / ludność_goblinów * 100:.2f}%",
        "stosunek całą ludność ocalonych Goblinów na całą ludność Goblinów": f"{cała_ludność_ocalałych_goblinów / ludność_goblinów * 100:.2f}%",
        "stosunek naiwnych łowców na łowców": f"{ludność_naiwnych_łowców / ludność_łowców * 100:.2f}%",
        "stosunek nie naiwnych łowców na łowców": f"{ludność_nie_naiwnych_łowców / ludność_łowców * 100:.2f}%",
        "stosunek naiwnych łowców na całą ludność": f"{ludność_naiwnych_łowców / ludność_goblinów * 100:.2f}%",
        "stosunek nie naiwnych łowców na całą ludność": f"{ludność_nie_naiwnych_łowców / ludność_goblinów * 100:.2f}%",
        "stosunek przeklętych łowców na całą ludność": f"{ludność_przeklętych_łowców / ludność_goblinów * 100:.2f}%",
        "stosunek przeklętych łowców na łowców": f"{ludność_przeklętych_łowców / ludność_łowców * 100:.2f}%",
        "stosunek łowców z sensem na całą ludność": f"{ludność_łowców_z_sensem / ludność_goblinów * 100:.2f}%",
        "stosunek łowców z sensem na łowców": f"{ludność_łowców_z_sensem / ludność_łowców * 100:.2f}%",
        "stosunek łowców z sensem na ocalonych Goblinów": f"{ludność_łowców_z_sensem / ludność_ocalałych_goblinów * 100:.2f}%",
        "stosunek ocalonych poprostu żyjących Goblinów na całą ludność": f"{ludność_ocalałych_poprostu_żyjących / ludność_goblinów * 100:.2f}%",
        "stosunek ocalonych poprostu żyjących Goblinów na ocalonych Goblinów": f"{ludność_ocalałych_poprostu_żyjących / ludność_ocalałych_goblinów * 100:.2f}%",
        "stosunek przeklętych Goblinów nie będących łowcami na całą ludność": f"{ludność_przeklętych_goblinów_nie_będących_łowcami / ludność_goblinów * 100:.2f}%"
    }
    return statystyki_goblinów

# 1. Pobieramy statystyki PRZED rzezią
staty_przed = pokaż_g()

# --- WYDARZENIE: RZEŹ (Aktualizacja wartości podstawowych) ---
ludność_goblinów -= 863
ludność_ocalałych_goblinów -= 144
ludność_ocalałych_poprostu_żyjących -= 91
ludność_przeklętych_łowców -= 50
ludność_przeklętych_goblinów_nie_będących_łowcami -= 669

# --- AKTUALIZACJA ZALEŻNOŚCI (Żeby wzory matematyczne po rzezi się zgadzały) ---
cała_ludność_ocalałych_goblinów = ludność_ocalałych_goblinów + ludność_cyklistów
ludność_przeklętych_goblinów = ludność_przeklętych_łowców + ludność_przeklętych_goblinów_nie_będących_łowcami
ludność_łowców = ludność_ocalałych_goblinów - ludność_ocalałych_poprostu_żyjących
ludność_naiwnych_łowców = ludność_łowców - 53
ludność_łowców_z_sensem = ludność_naiwnych_łowców + ludność_nie_naiwnych_łowców

# 2. Pobieramy statystyki PO rzezi
staty_po = pokaż_g()
print("=================== PRZED RZEZIĄ ===================")
for klucz, wartosc in staty_przed.items():
    print(f"{klucz}: {wartosc}")

print("\n=================== PO RZEZI ===================")
for klucz, wartosc in staty_po.items():
    print(f"{klucz}: {wartosc}")