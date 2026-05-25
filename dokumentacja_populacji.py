lg = 21040
log = 2099
lc = 5
clog = log + lc
lpg = lg-log-lc
ll = 435
lopz = log-ll
lnl = ll - 53
lnnl = 3
llzs = lnl+lnnl
lpl = 50
lpgnbl = lpg - 50
def pokaż_g():
    global lg, log, lc, clog, lpg, ll, lopz, lnl, lnnl, llzs, lpl, lpgnbl
    print(f"stosunek cyklistów na całą ludność: {lc/lg*100}%")
    print(f"stosunek ocalonych goblinów na całą ludność: {log/lg*100}%")
    print(f"stosunek łowców na całą ludność: {ll/lg*100}%")
    print(f"stosunek łowców na ocalonych Goblinów: {ll/log*100}%")
    print(f"stosunek przeklętych Goblinów na całą ludność: {lpg/lg*100}%")
    print(f"stosunek całą ludność ocalonych Goblinów na całą ludność Goblinów: {clog/lg*100}%")
    print(f"stosunek naiwnych łowców na łowców: {lnl/ll*100}%")
    print(f"stosunek nie naiwnych łowców na łowców: {lnnl/ll*100}%")
    print(f"stosunek naiwnych łowców na całą ludność: {lnl/lg*100}%")
    print(f"stosunek nie naiwnych łowców na całą ludność: {lnnl/lg*100}%")
    print(f"stosunek przeklętych łowców na całą ludność: {lpl/lg*100}%")
    print(f"stosunek przeklętych łowców na łowców: {lpl/ll*100}%")
    print(f"stosunek łowców z sensem na całą ludność: {llzs/lg*100}%")
    print(f"stosunek łowców z sensem na łowców: {llzs/ll*100}%")
    print(f"stosunek łowców z sensem na ocalonych Goblinów: {llzs/log*100}%")
    print(f"stosunek ocalonych poprostu żyjących Goblinów na całą ludność: {lopz/lg*100}%")
    print(f"stosunek ocalonych poprostu żyjących Goblinów na ocalonych Goblinów: {lopz/log*100}%")
    print(f"stosunek przeklętych Goblinów nie będących łowcami na całą ludność: {lpgnbl/lg*100}%")
pokaż_g()
lg -= 863
log -= 144
clog -= 144
lopz -= 91
lpl -= 50
lpgnbl -= 669
lpg = lpl + lpgnbl
pokaż_g()
