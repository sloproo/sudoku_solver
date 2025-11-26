import time
import itertools

def ratkaise_sudoku(sisaan_sudoku: list) -> list:
    global yrityksia
    yrityksia = 0
    mahdolliset = alusta_mahdolliset()
    sudoku = alusta_sudoku()
    for y in range(9):
        for x in range(9):
            if sisaan_sudoku[y][x] != 0:
                lisaa_sudokuun(sudoku, y, x, sisaan_sudoku[y][x], mahdolliset, True)
                
    while True:
        edistysta = 0
        edistysta += tarkasta_vaajaamattomat(sudoku, mahdolliset)
        edistysta += syvatarkasta_blokeista(sudoku, mahdolliset)
        edistysta += syvatarkasta_rivilta(sudoku, mahdolliset)
        edistysta += syvatarkasta_sarakkeesta(sudoku, mahdolliset)
        
        
        if edistysta == 0:
            edistysta += alaston_pari(sudoku, mahdolliset)
            edistysta += alaston_tripla(sudoku, mahdolliset)
            edistysta += alaston_nelikko(sudoku, mahdolliset)
            edistysta += piiloutunut_pari(sudoku, mahdolliset)
            edistysta += piiloutunut_tripla(sudoku, mahdolliset)
            edistysta += piiloutunut_nelikko(sudoku, mahdolliset)
            edistysta += lukitut_kandidaatit_1(sudoku, mahdolliset)
            edistysta += lukitut_kandidaatit_2(sudoku, mahdolliset)
            edistysta += x_wing(sudoku, mahdolliset)
            edistysta += miekkakala(sudoku, mahdolliset)
            
        if edistysta == 0:
            print("Taitaa olla jumissa")
            raaka = input("Mennäänkö raa'alla voimalla? [k/E]?: ")
            if raaka.lower() == "k":
                viive = 0
                puhelias_vastaus = input("Näytetäänkö välivaiheet? [k/E]: ")
                puhelias = True if puhelias_vastaus.lower() == "k" else False
                if puhelias:
                    viive = input("Kuinka pitkä viive millisekunteina tulostusten välillä, max 250? ")
                    try:
                        viive = int(viive.strip())
                        viive = 250 if viive > 250 else viive
                    except (TypeError, ValueError) as _:
                        pass
                lahtoaika = time.time()
                sudoku = brute_force(sudoku, mahdolliset, puhelias, viive)
                loppuaika = time.time()
                kesto = loppuaika - lahtoaika
                
        
        edistysta = 0

        if onko_ratkaistu(sudoku):
            print("\n\n\n\n\n\nSudoku ratkaistu!\n")
            loppuaika = time.time()
            kesto = loppuaika - lahtoaika
            print(f"Aikaa kului {kesto:.3f} sekuntia")
            if yrityksia != 0:
                print(f"Raa'alla voimalla sijoitettiin {yrityksia} numeroa tauluun")
            tulosta_sudoku(sudoku)
            print("oikeinkin vielä" if onko_kelvollinen_sudoku(sudoku) else "nyt vaan meni jotenkin väärin")
            # ylläolevan pitäisi korvata nämä rivit
            # if onko_kelvollinen_sudoku(sudoku):
            #     print("oikeinkin vielä")
            # else:
            #     print("nyt vaan meni jotenkin väärin")
            time.sleep(5)
            return sudoku

def onko_ratkaistu(sudoku: list) -> bool:
    nollia_jaljella = False
    for y in range(9):
            for x in range(9):
                if sudoku[y][x] == 0:
                    return False
    if not nollia_jaljella:
        # print("Sudoku ratkaistu:")
        return True

def tulosta_sudoku(sudoku: list):
    tulostettava = ""
    for i in range(9):
        for j in range(0, len(sudoku[i]), 3):
            tulostettava += f"{viivan_tulostus(sudoku[i][j])} "
            tulostettava += f"{viivan_tulostus(sudoku[i][j + 1])} "
            tulostettava += f"{viivan_tulostus(sudoku[i][j + 2])}  "
        tulostettava += "\n"
        if (i) % 3 == 2:
            tulostettava += "\n"
    print(tulostettava)
			
def viivan_tulostus(i: int):
    if i == 0:
        return "_"
    else:
        return i

def lisaa_sudokuun(sudoku: list, rivi: int, sarake: int, nro: int, mahdolliset: list, nopeasti=False):
    sudoku[rivi][sarake] = nro
    poista_mahdollisista_ruuduissa(nro, rivin_ruudut(rivi), mahdolliset)
    poista_mahdollisista_ruuduissa(nro, sarakkeen_ruudut(sarake), mahdolliset)
    poista_mahdollisista_ruuduissa(nro, blokin_ruudut(ruudun_blokki(rivi, sarake)), mahdolliset)
    
    mahdolliset[rivi][sarake] = []
    if not nopeasti:
        # time.sleep(0.45)
        pass

def kelpaako_ruutuun(rivi: int, sarake: int, nro: int, sudoku: list) -> bool:
    for y, x in talon_ruudut(rivi, "r"):
        if nro == sudoku[y][x]:
            return False
    for y, x in talon_ruudut(sarake, "s"):
        if nro == sudoku[y][x]:
            return False
    for y, x in talon_ruudut(ruudun_blokki(rivi, sarake), "b"):
        if nro == sudoku[y][x]:
            return False
    return True

def ota_sudoku():
    palautettava = []
    rivinro = 0
    while True:    
        while len(palautettava) < 9:
            palautettava.append(ota_rivi(rivinro))
            rivinro = len(palautettava)
        print("Sudokusi alla. Jos olet tyytyväinen, paina Enter, muuten anna korjattavan rivin numero (1 - 9)")
        print("Käskyllä i# sijoitetaan riville # uusi rivi ja siirretään muita 1 alaspäin\n")
        tulosta_sudoku(palautettava)
        try:
            komento = input("Korjattavan rivin numero tai tyhjä = OK: ")
            if komento == "":
                print("\n")
                if not onko_kelvollinen_sudoku(palautettava):
                    continue
                return palautettava
            
            elif komento[0].lower() == "i":
                if len(komento) < 2:
                    raise ValueError
                rivinro = int(komento[1]) - 1
                if rivinro > 8 or rivinro < 0:
                    raise ValueError
                elif rivinro == 8:
                    palautettava[8] = ota_rivi(rivinro)
                else:
                    for i in range(7, rivinro - 1, -1):
                        palautettava[i+1] = palautettava[i]
                    palautettava[rivinro] = ota_rivi(rivinro)

            else:
                rivinro = int(komento) - 1
                if rivinro < 0 or rivinro > 8:
                    print()
                    print("Rivinumeron oltava väliltä 0 - 8")
                    raise ValueError
                palautettava[rivinro] = ota_rivi(rivinro)
                continue
        except (KeyError, ValueError):
            continue

def ota_rivi(rivinro: int) -> list:
    while True:
        try:
            syote = input(f"Syötä rivi #{rivinro + 1} numeroita, erottimena välilyönti.\n{'# ' * 3}{'* ' * 3}# # #\n")
            if len(syote) > 17:
                syote = syote[:17]
            if len(syote) < 17:
                syote += " " * (17 - len(syote))
            for i in range(0, 18, 2):
                if syote[i] == " ":
                    syote = syote[:i] + "0" + syote[i+1:]
                if syote[i] not in "0123456789":
                    syote = syote[:i] + "0" + syote[i+1:]
            for i in range(1, 17, 2):
                if syote[i] != " ":
                    syote = syote[:i] + " " + syote[i+1:]
            rivi = syote.strip().split(" ")
            rivi = [int(i) for i in rivi]
            for i in rivi:
                if i != 0 and rivi.count(i) != 1:
                    raise ValueError
                if i < 0 or i > 9:
                    raise ValueError
            print("\nSiivottu rivi:")
            for i in rivi:
                print(str(i).replace("0", "_"), end=" ")
            print("\n\n")

            return rivi
        except (KeyError, ValueError, IndexError):
            print()
            print("*** Virheellinen rivi, yritä uudestaan ***")
            print()
            continue

def onko_kelvollinen_sudoku(sudoku: list) -> bool:
    for nro_talo in range(9):
        blokki = [sudoku[y][x] for (y, x) in blokin_ruudut(nro_talo)]
        rivi = [sudoku[y][x] for (y, x) in rivin_ruudut(nro_talo)]
        sarake = [sudoku[y][x] for (y, x) in sarakkeen_ruudut(nro_talo)]

        for i in range(1,10):
            if blokki.count(i) > 1:
                print(f"Blokissa {nro_talo} virhe: enemmän kuin yksi {i}")
                return False
            if rivi.count(i) > 1:
                print(f"Rivillä {nro_talo} virhe: enemmän kuin yksi {i}")
                time.sleep(2)
                return False
            if sarake.count(i) > 1:
                print(f"Sarakkeessa {nro_talo} virhe: enemmän kuin yksi {i}")
                return False
    
    print("Kelpaa")
    time.sleep(1)
    return True

def alusta_sudoku() -> list:
    palautettava = []    
    for i in range(9):
        palautettava.append([])
        for _ in range(9):
            palautettava[i].append(0)
    return palautettava

def alusta_mahdolliset() -> list:
    mahdolliset = []
    for i in range(9):
        mahdolliset.append([])
        for _ in range(9):
            mahdolliset[i].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return mahdolliset


# apufunktiot

def ruudun_blokki(rivi: int, sarake: int) -> int:
    return rivi // 3 * 3 + sarake // 3 * 1
        
def talon_ruudut(talon_nro: int, tyyppi: str) -> list:
    tyyppi = tyyppi.lower()
    if tyyppi not in ["r", "s", "b"]:
        raise ValueError("Talon tyypin pitää olla r, s tai b")
    if tyyppi == "r":
        return rivin_ruudut(talon_nro)
    elif tyyppi == "s":
        return sarakkeen_ruudut(talon_nro)
    elif tyyppi == "b":
        return blokin_ruudut(talon_nro)
    else:
        print("Mitä helvettiä @ talon ruudut")
        time.sleep(2)
        raise ValueError

def blokin_ruudut(blokki: int) -> list:
    i = blokki // 3 * 3
    j = blokki % 3 * 3
    palautettavat_ruudut = []
    for rivi in range(i, i + 3):
        for sarake in range(j, j + 3):
            palautettavat_ruudut.append((rivi, sarake))
    return palautettavat_ruudut

def sarakkeen_ruudut(sarake: int) -> list:
    palautettavat_ruudut = [(i, sarake) for i in range(9)]
    return palautettavat_ruudut

def rivin_ruudut(rivi: int) -> list:
    palautettavat_ruudut = [(rivi, i) for i in range(9)]
    return palautettavat_ruudut

def muut_linjat(*linjat) -> list:
    karsittavat_linjat = [i for i in range(9)]
    for linja in linjat:
        karsittavat_linjat.remove(linja)
    return karsittavat_linjat

def muut_linjat_blokissa(linja: int) -> tuple:
    if linja < 0 or linja > 8:
        raise ValueError("Pitää olla 0 - 8")
    levea = [i for i in range((linja // 3 * 3), ((linja // 3 * 3) + 3))]
    levea.remove(linja)
    return tuple(levea)

def muiden_kaistojen_linjat(kaista: int) -> list:
    if kaista not in range(3):
        raise ValueError("Kaistan oltava väliltä 0 - 2")
    palautettavat_linjat = []
    siivotut_kaistat = [0, 1, 2]
    siivotut_kaistat.remove(kaista)
    for kaista in siivotut_kaistat:
        palautettavat_linjat += [kaista * 3, kaista * 3 + 1, kaista * 3 + 2]
    return palautettavat_linjat

def muut_numerot(*numerot) -> list:
    karsittavat_numerot = [i for i in range(1, 10)]
    for numero in numerot:
        karsittavat_numerot.remove(numero)
    return karsittavat_numerot

def etsi_mahdollisista_ruuduissa(nro: int, pengottavat_ruudut: list, mahdolliset: list) -> list:
    nro_mahdollinen_ruuduissa = []
    for y, x in pengottavat_ruudut:
        if nro in mahdolliset[y][x]:
            nro_mahdollinen_ruuduissa.append((y, x))
    return nro_mahdollinen_ruuduissa

def talon_mahdolliset_ruuduittain(talon_nro: int, tyyppi: str, mahdolliset: list) -> list:
    tyyppi = tyyppi.lower()
    if tyyppi not in ["r", "s", "b"]:
        raise ValueError("Talon tyypin pitää olla r, s tai b")
    return [mahdolliset[y][x] for y, x in talon_ruudut(talon_nro, tyyppi)]

def numeron_mahdolliset_sudokussa(nro: int, mahdolliset: list) -> list:
    nron_paikat = []
    for y in range(9):
        for x in range(9):
            if nro in mahdolliset[y][x]:
                nron_paikat.append((x,y))
    return nron_paikat

def numeron_mahdolliset_ruudut_talossa(nro: int, talon_nro: int, tyyppi: int, mahdolliset: list) -> list:
    tyyppi = tyyppi.lower()
    if tyyppi not in ["r", "s", "b"]:
        raise ValueError("Talon tyypin pitää olla 'r', 's' tai 'b'")
    numero_mahdollinen_ruuduissa = []
    for y, x in talon_ruudut(talon_nro, tyyppi):
        if nro in mahdolliset[y][x]:
            numero_mahdollinen_ruuduissa.append((y, x))
    return numero_mahdollinen_ruuduissa

def poista_mahdollisista_ruuduissa(numero: int, siivottavat_ruudut: list, mahdolliset: list):
    for y, x in siivottavat_ruudut:
        if numero in mahdolliset[y][x]:
            mahdolliset[y][x].remove(numero)

# ratkaisufunktiot

def tarkasta_vaajaamattomat(sudoku:list, mahdolliset: list) -> int:
    eteni = 0
    for y in range(9):
        for x in range(9):
            if len(mahdolliset[y][x]) == 1:
                # print(f"Nonniih: ruudussa [{y}][{x}] ei voi olla mitään muuta kuin {mahdolliset[y][x][0]}")
                # print("lisätään siis luku sudokuun")
                lisaa_sudokuun(sudoku, y, x, mahdolliset[y][x][0], mahdolliset)
                print("\n\n")
                eteni += 1
                tulosta_sudoku(sudoku)
                
    return eteni

def syvatarkasta_blokeista(sudoku:list, mahdolliset: list) -> int:
    eteni = 0
    for blokki in range(9):
        talon_mahdolliset = []
        for y, x in blokin_ruudut(blokki):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in blokin_ruudut(blokki):
                    if nro in mahdolliset[y][x]:
                        # print(f"Nonniih: ruutu [{y}][{x}] on blokin perusteella ainoa ruutu jossa voi olla numero {nro}")
                        # print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        print("\n\n")
                        tulosta_sudoku(sudoku)
                        eteni += 1
    return eteni

def syvatarkasta_rivilta(sudoku:list, mahdolliset: list) -> int:
    eteni = 0
    for rivi in range(9):
        talon_mahdolliset = []
        for y, x in rivin_ruudut(rivi):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in rivin_ruudut(rivi):
                    if nro in mahdolliset[y][x]:
                        # print(f"Nonniih: ruutu [{y}][{x}] on rivin perusteella ainoa ruutu jossa voi olla numero {nro}")
                        # print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        print("\n\n")
                        tulosta_sudoku(sudoku)
                        eteni += 1
    return eteni

def syvatarkasta_sarakkeesta(sudoku:list, mahdolliset: list) -> int:
    eteni = 0
    for sarake in range(9):
        talon_mahdolliset = []
        for y, x in sarakkeen_ruudut(sarake):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in sarakkeen_ruudut(sarake):
                    if nro in mahdolliset[y][x]:
                        # print(f"Nonniih: ruutu [{y}][{x}] on sarakkeen perusteella ainoa ruutu jossa voi olla numero {nro}")
                        # print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        print("\n\n")
                        tulosta_sudoku(sudoku)
                        eteni += 1
    return eteni

def alaston_pari(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi in ("r", "s", "b"):
        for talon_nro in range(9):
            for nro_1, nro_2 in itertools.combinations(range(1, 10), 2):
                parien_ruudut = []
                kasiteltavat_talon_ruudut = talon_ruudut(talon_nro, tyyppi)
                for y, x in kasiteltavat_talon_ruudut:
                    if len(mahdolliset[y][x]) == 2:
                        if nro_1 in mahdolliset[y][x] and nro_2 in mahdolliset[y][x]:
                            parien_ruudut.append((y, x))
                if len(parien_ruudut) == 2:
                    for ruutu in parien_ruudut:
                        kasiteltavat_talon_ruudut.remove(ruutu)
                    for y, x in kasiteltavat_talon_ruudut:
                        if nro_1 in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(nro_1)
                            # print(f"poistettu {nro_1} ruudusta {y}, {x} alastoman parin {parien_ruudut} vuoksi talossa {tyyppi}")
                        if nro_2 in kasiteltavat_talon_ruudut:
                            mahdolliset[y][x].remove(nro_2)
                            # print(f"poistettu {nro_2} ruudusta {y}, {x} alastoman parin {parien_ruudut} vuoksi talossa {tyyppi}")
    return eteni

def piiloutunut_pari(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi in ("r", "s", "b"):
        for talon_nro in range(9):
            for kaksi_numeroa in itertools.combinations(range(1, 10), 2):
                ruudut = talon_ruudut(talon_nro, tyyppi)
                ruudut_joissa_pari = []
                for y, x in ruudut:
                    if kaksi_numeroa[0] in mahdolliset[y][x] and kaksi_numeroa[1] in mahdolliset[y][x]:
                        ekan_mahdolliset = etsi_mahdollisista_ruuduissa(kaksi_numeroa[0], talon_ruudut(talon_nro, tyyppi), mahdolliset)
                        tokan_mahdolliset = etsi_mahdollisista_ruuduissa(kaksi_numeroa[1], talon_ruudut(talon_nro, tyyppi), mahdolliset)
                        if len(ekan_mahdolliset) != 2 or len(tokan_mahdolliset) != 2:
                            continue
                        elif ekan_mahdolliset != tokan_mahdolliset:
                            continue
                        else:
                            ruudut_joissa_pari.append((y, x))
                if len(ruudut_joissa_pari) == 2:
                    for y, x in ruudut_joissa_pari:
                        if len(mahdolliset[y][x]) > 2:
                            loput_numerot = muut_numerot(kaksi_numeroa[0], kaksi_numeroa[1])
                            for poistettava_numero in loput_numerot:
                                if poistettava_numero in mahdolliset[y][x]:
                                    mahdolliset[y][x].remove(poistettava_numero)
                            # print(f"poistettu joukosta {mahdolliset[y][x]} ruudussa {y}, {x} muut kuin {kaksi_numeroa} piiloutuneen parin takia, tyyppi {tyyppi}.")
                            eteni += 1
    return eteni

def piiloutunut_tripla(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi in ("r", "s", "b"):
        for talon_nro in range(9):
            for kolme_numeroa in itertools.combinations(range(1, 10), 3):
                ruudut_joissa_triplaa = []
                numeroita_triplasta_mahdollisia = 0
                for numero in kolme_numeroa:
                    if len(etsi_mahdollisista_ruuduissa(numero, talon_ruudut(talon_nro, tyyppi), mahdolliset)) == 0:
                        # print(f"Triplan numeroa {numero} ei ollut yhdenkään ruudun mahdollisissa joukossa {tyyppi} {talon_nro}")
                        break
                    else:
                        numeroita_triplasta_mahdollisia += 1
                    for ruutu in etsi_mahdollisista_ruuduissa(numero, talon_ruudut(talon_nro, tyyppi), mahdolliset):
                        if ruutu not in ruudut_joissa_triplaa:
                            ruudut_joissa_triplaa.append(ruutu)
                if numeroita_triplasta_mahdollisia != 3 or len(ruudut_joissa_triplaa) != 3:
                    continue
                loput_numerot = muut_numerot(kolme_numeroa[0], kolme_numeroa[1], kolme_numeroa[2])
                for y, x in ruudut_joissa_triplaa:
                    for poistettava in loput_numerot:
                        if poistettava in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(poistettava)
                            # print(f"Poistettu piiloutuneella triplalla {poistettava} ruudusta {y}, {x} , tyypillä {tyyppi}.")
                            # print(f"Tripla oli {kolme_numeroa}")
                            eteni += 1
    return eteni

def piiloutunut_nelikko(sudoku: list, mahdolliset: list) -> int: # testaamatta mutta toiminee
    eteni = 0
    for tyyppi in ("r", "s", "b"):
        for talon_nro in range(9):
            for nelja_numeroa in itertools.combinations(range(1, 10), 4):
                ruudut_joissa_nelikkoa = []
                numeroita_nelikosta_mahdollisissa = 0

                for numero in nelja_numeroa:
                    if len(etsi_mahdollisista_ruuduissa(numero, talon_ruudut(talon_nro, tyyppi), mahdolliset)) == 0:
                        # print(f"Nelikon numeroa {numero} ei ollut yhdenkään ruudun mahdollisissa joukossa {tyyppi} {talon_nro}")
                        break
                    else:
                        numeroita_nelikosta_mahdollisissa += 1
                    for ruutu in etsi_mahdollisista_ruuduissa(numero, talon_ruudut(talon_nro, tyyppi), mahdolliset):
                        if ruutu not in ruudut_joissa_nelikkoa:
                            ruudut_joissa_nelikkoa.append(ruutu)
                if numeroita_nelikosta_mahdollisissa != 4 or len(ruudut_joissa_nelikkoa) != 4:
                    continue
                loput_numerot = muut_numerot(nelja_numeroa[0], nelja_numeroa[1], nelja_numeroa[2], nelja_numeroa[3])
                for y, x in ruudut_joissa_nelikkoa:
                    for poistettava in loput_numerot:
                        if poistettava in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(poistettava)
                            # print(f"Poistettu piiloutuneella nelikolla {poistettava} ruudusta {y}, {x} , tyypillä {tyyppi}.")
                            # print(f"Nelikko oli {nelja_numeroa}")
                            eteni += 1
    return eteni

def alaston_tripla(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi in ["r", "s", "b"]:
        for talo in range(0, 9):
            for kolme_numeroa in itertools.combinations(range(1, 10), 3):
                ruudut_joissa_triplaa = []
                
                for numero in kolme_numeroa:
                    numeron_ruudut = etsi_mahdollisista_ruuduissa(numero, talon_ruudut(talo, tyyppi), mahdolliset)
                    for ruutu in numeron_ruudut:
                        if ruutu not in ruudut_joissa_triplaa:
                            ruudut_joissa_triplaa.append(ruutu)
                kielletyt_numerot = [i for i in range(1, 10)]
                for numero in kolme_numeroa:
                    kielletyt_numerot.remove(numero)
                
                for y, x in talon_ruudut(talo, tyyppi):
                    for kielletty in kielletyt_numerot:
                        if (y, x) not in ruudut_joissa_triplaa:
                            break
                        if kielletty in mahdolliset[y][x] or len(mahdolliset[y][x]) == 0:
                            ruudut_joissa_triplaa.remove((y, x))
                if len(ruudut_joissa_triplaa) == 3:
                    # print(f"{tyyppi} {talo}: ruudut {ruudut_joissa_triplaa} pitävät kaikki sisällään vain numeroita {numero for numero in kolme_numeroa}.")
                    kasiteltavat_talon_ruudut = talon_ruudut(talo, tyyppi)
                    for ruutu in ruudut_joissa_triplaa:
                        kasiteltavat_talon_ruudut.remove(ruutu)
                    for y, x in kasiteltavat_talon_ruudut:
                        for poistettava_numero in kolme_numeroa:
                            if poistettava_numero in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(poistettava_numero)
                                eteni += 1
                                # print(f"Poistettu {poistettava_numero} ruudusta {y}, {x} alastoman triplan vuoksi tyypissä {tyyppi}")
                    
    return eteni
                        
def alaston_nelikko(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi in ["r", "s", "b"]:
        for talo in range(0, 9):
            for nelja_numeroa in itertools.combinations(range(1, 10), 4):
                kielletyt_numerot = [i for i in range(1, 10)]
                for numero in nelja_numeroa:
                    kielletyt_numerot.remove(numero)
                ruudut = talon_ruudut(talo, tyyppi)
                ruudut_joissa_nelikko = ruudut[:]
                for y, x in ruudut:
                    for kielletty in kielletyt_numerot:
                        if (y, x) not in ruudut_joissa_nelikko:
                            break
                        if kielletty in mahdolliset[y][x] or len(mahdolliset[y][x]) == 0:
                            ruudut_joissa_nelikko.remove((y, x))
                if len(ruudut_joissa_nelikko) == 4:
                    # print(f"{tyyppi} {talo}: ruudut {ruudut_joissa_nelikko} pitävät kaikki sisällään vain numeroita {numero for numero in nelja_numeroa}.")
                    kasiteltavat_talon_ruudut = talon_ruudut(talo, tyyppi)
                    for ruutu in ruudut_joissa_nelikko:
                        kasiteltavat_talon_ruudut.remove(ruutu)
                    for y, x in kasiteltavat_talon_ruudut:
                        for poistettava_numero in nelja_numeroa:
                            if poistettava_numero in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(poistettava_numero)
                                eteni += 1
                                # print(f"Poistettu {poistettava_numero} ruudusta {y}, {x} alastoman nelikon vuoksi tyypissä {tyyppi}")
                    
    return eteni

def lukitut_kandidaatit_1(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for blokki in range(0,9):
        blokin_mahdolliset = [mahdolliset[y][x] for y, x in blokin_ruudut(blokki)]
        for nro in range(1, 10):
            esiintymia = 0
            for solun_mahdolliset in blokin_mahdolliset:
                if nro in solun_mahdolliset:
                    esiintymia += 1
            if esiintymia > 0 and esiintymia <= 3 :
                esiintymien_indeksit = []
                esiintymien_hakukohta = 0
                while len(esiintymien_indeksit) < esiintymia:
                    if nro in blokin_mahdolliset[esiintymien_hakukohta]:
                        esiintymien_indeksit.append(esiintymien_hakukohta)
                    esiintymien_hakukohta += 1
                esiintymien_rivit_blokissa = [i // 3 for i in esiintymien_indeksit]
                esiintymien_sarakkeet_blokissa = [i % 3 for i in esiintymien_indeksit]
                
                absoluuttiset_koordinaatit = []
                for j in range(esiintymia):
                    absoluuttiset_koordinaatit.append(((blokki // 3) * 3 + esiintymien_rivit_blokissa[j], (blokki % 3) * 3 + esiintymien_sarakkeet_blokissa[j]))
                if esiintymien_rivit_blokissa.count(esiintymien_rivit_blokissa[0]) == len(esiintymien_rivit_blokissa):
                    for x in range(9):
                        if (absoluuttiset_koordinaatit[0][0], x) not in absoluuttiset_koordinaatit and \
                            nro in mahdolliset[absoluuttiset_koordinaatit[0][0]][x]:
                            mahdolliset[absoluuttiset_koordinaatit[0][0]][x].remove(nro)
                            # print(f"Rivillä {absoluuttiset_koordinaatit[0][0]}: on blokin {blokki} kaikki {nro}:n esiintymät" + \
                                # f"poistetaan siis se mahdollisista kohdasta {mahdolliset[absoluuttiset_koordinaatit[0][0]][x]}")
                            eteni += 1
                if esiintymien_sarakkeet_blokissa.count(esiintymien_sarakkeet_blokissa[0]) == len(esiintymien_sarakkeet_blokissa):
                    for y in range(9):
                        if (y, absoluuttiset_koordinaatit[0][1]) not in absoluuttiset_koordinaatit and \
                            nro in mahdolliset[y][absoluuttiset_koordinaatit[0][1]]:
                            mahdolliset[y][absoluuttiset_koordinaatit[0][1]].remove(nro)
                            # print(f"Sarakkeessa {absoluuttiset_koordinaatit[0][1]}: on blokin {blokki} kaikki {nro}:n esiintymät" + \
                                # f"poistetaan siis se mahdollisista kohdasta {mahdolliset[absoluuttiset_koordinaatit[0][0]][x]}")
                            eteni += 1
                    
                # print("Lukitut kandidaatit kertaalleen laskettu")
    return eteni

def lukitut_kandidaatit_2(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for nro in range(1, 10):
        for rivi in range(0,9):
            mahdollisen_paikat_rivilla = []
            for ruutu in rivin_ruudut(rivi):
                if nro in mahdolliset[ruutu[0]][ruutu[1]]:
                    mahdollisen_paikat_rivilla.append(ruutu)
            if len(mahdollisen_paikat_rivilla) > 1:
                osumien_sarakkeet = []
                for osuma in mahdollisen_paikat_rivilla:
                    osumien_sarakkeet.append(osuma[1])
                osumien_kaistat = [sarake // 3 for sarake in osumien_sarakkeet]
                if len(set(osumien_kaistat)) == 1:
                    siivottava_blokki = ruudun_blokki(mahdollisen_paikat_rivilla[0][0], mahdollisen_paikat_rivilla[0][1])
                    for y, x in blokin_ruudut(siivottava_blokki):
                        if (y, x) not in mahdollisen_paikat_rivilla and nro in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(nro)
                            eteni += 1
                            # print(f"Poistettu {nro} mahdollisista ruudussa {y},{x} (lukitut kandidaatit 2)")
                            
        for sarake in range(0,9):
            mahdollisen_paikat_sarakkeessa = []
            for ruutu in sarakkeen_ruudut(sarake):
                if nro in mahdolliset[ruutu[0]][ruutu[1]]:
                    mahdollisen_paikat_sarakkeessa.append(ruutu)
            if len(mahdollisen_paikat_sarakkeessa) > 1:
                osumien_rivit = []
                for osuma in mahdollisen_paikat_sarakkeessa:
                    osumien_rivit.append(osuma[0])
                osumien_kaistat = [rivi // 3 for rivi in osumien_rivit]
                if len(set(osumien_kaistat)) == 1:
                    siivottava_blokki = ruudun_blokki(mahdollisen_paikat_sarakkeessa[0][0], mahdollisen_paikat_sarakkeessa[0][1])
                    for y, x in blokin_ruudut(siivottava_blokki):
                        if (y, x) not in mahdollisen_paikat_sarakkeessa and nro in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(nro)
                            eteni += 1
                            # print(f"Poistettu {nro} mahdollisista ruudussa {y},{x} (lukitut kandidaatit 2)")
                          
    return eteni

def x_wing(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for nro in range(1,10):
        # rivi
        for talon_nro in range(9):
            pari = etsi_mahdollisista_ruuduissa(nro, rivin_ruudut(talon_nro), mahdolliset)
            if len(pari) == 2:
                parin_sarakkeet = (pari[0][1], pari[1][1])
                for toka_talon_nro in range(talon_nro + 1, 9):
                    toka_pari = etsi_mahdollisista_ruuduissa(nro, rivin_ruudut(toka_talon_nro), mahdolliset)
                    if len(toka_pari) == 2 and (toka_pari[0][1], toka_pari[1][1]) == parin_sarakkeet:
                        # print(f"Löytyi X-wingin pari numerolla {nro}, riveiltä {pari[0][0]} ja {toka_pari[0][0]}, sarakkeista {pari[0][1]} ja {pari[1][1]}.")
                        # print(f"Numero löytyy riveittäin hakiessa täsmälleen kohdista {pari} ja {toka_pari}")
                        for poiston_rivi in range(9):
                            if poiston_rivi != pari[0][0] and poiston_rivi != toka_pari[0][0]:
                                for poiston_sarake in parin_sarakkeet:
                                    if nro in mahdolliset[poiston_rivi][poiston_sarake]:
                                        mahdolliset[poiston_rivi][poiston_sarake].remove(nro)
                                        # print(f"X-wingin perusteella poistettu {nro} ruudun [{poiston_rivi}, {poiston_sarake}] mahdollisista.")
                                        eteni += 1
        # sarake
        for talon_nro in range(9):
            pari = etsi_mahdollisista_ruuduissa(nro, sarakkeen_ruudut(talon_nro), mahdolliset)
            if len(pari) == 2:
                parin_rivit = (pari[0][0], pari[1][0])
                for toka_talon_nro in range(talon_nro + 1, 9):
                    toka_pari = etsi_mahdollisista_ruuduissa(nro, sarakkeen_ruudut(toka_talon_nro), mahdolliset)
                    if len(toka_pari) == 2 and (toka_pari[0][0], toka_pari[1][0]) == parin_rivit:
                        # print(f"Löytyi X-wingin pari numerolla {nro}, sarakkeista {pari[0][1]} ja {toka_pari[0][1]}, riveiltä {pari[0][0]} ja {pari[1][0]}.")
                        # print(f"Numero löytyy sarakkeitain hakiessa täsmälleen kohdista {pari} ja {toka_pari}")
                        for poiston_sarake in range(9):
                            if poiston_sarake != pari[0][1] and poiston_sarake != toka_pari[0][1]:
                                for poiston_rivi in parin_rivit:
                                    if nro in mahdolliset[poiston_rivi][poiston_sarake]:
                                        mahdolliset[poiston_rivi][poiston_sarake].remove(nro)
                                        # print(f"X-wingin perusteella poistettu {nro} ruudun [{poiston_rivi}, {poiston_sarake}] mahdollisista.")
                                        eteni += 1
    return eteni
     
def miekkakala(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for tyyppi_1, tyyppi_2 in [("r", "s"), ("s", "r")]:
        for nro in range(1, 10):
            ehdokkaat_linjoiksi = []
            for linja in range(9):
                linjan_ruudut = talon_ruudut(linja, tyyppi_1)
                osumat_linjalla = etsi_mahdollisista_ruuduissa(nro, linjan_ruudut, mahdolliset)
                if len(osumat_linjalla) > 0 and len(osumat_linjalla) <= 3:
                    ehdokkaat_linjoiksi.append(linja)
            
            if len(ehdokkaat_linjoiksi) >= 3:
                ehdokkaat_kakkoslinjoiksi = []
                for linja in ehdokkaat_linjoiksi:
                    for kakkoslinja in range(9):
                        if tyyppi_1 == "r":
                            if nro in mahdolliset[linja][kakkoslinja]:
                                if kakkoslinja not in ehdokkaat_kakkoslinjoiksi:
                                    ehdokkaat_kakkoslinjoiksi.append(kakkoslinja)
                        elif tyyppi_1 == "s":
                            if nro in mahdolliset[kakkoslinja][linja]:
                                if kakkoslinja not in ehdokkaat_kakkoslinjoiksi:
                                    ehdokkaat_kakkoslinjoiksi.append(kakkoslinja)                            
                ehdokkaat_kakkoslinjoiksi.sort()
                ykkoslinjojen_kombot = []
                for i in itertools.combinations(ehdokkaat_linjoiksi, 3):
                    ykkoslinjojen_kombot.append(i)
                kakkoslinjojen_kombot = []
                for i in itertools.combinations(ehdokkaat_kakkoslinjoiksi, 3):
                    kakkoslinjojen_kombot.append(i)
                for ykkoslinjojen_trio in ykkoslinjojen_kombot:
                    for kakkoslinjojen_trio in kakkoslinjojen_kombot:
                        mahdolliset_linjoilla = []
                        for linja in ykkoslinjojen_trio:
                            for ruutu in numeron_mahdolliset_ruudut_talossa(nro, linja, tyyppi_1, mahdolliset):
                                mahdolliset_linjoilla.append(ruutu)
                        karsittava_mahdolliset_linjoilla = mahdolliset_linjoilla[:]
                        for kakkoslinja in kakkoslinjojen_trio:
                            for ruutu in mahdolliset_linjoilla:
                                if tyyppi_1 == "r":
                                    if ruutu[1] == kakkoslinja:
                                        karsittava_mahdolliset_linjoilla.remove(ruutu)
                                elif tyyppi_1 == "s":
                                    if ruutu[0] == kakkoslinja:
                                        karsittava_mahdolliset_linjoilla.remove(ruutu)
                        if len(karsittava_mahdolliset_linjoilla) == 0:
                            suojellut_ruudut = []
                            if tyyppi_1 == "r":
                                for y in ykkoslinjojen_trio:
                                    for x in kakkoslinjojen_trio:
                                        suojellut_ruudut.append((y, x))
                            elif tyyppi_1 == "s":
                                for x in ykkoslinjojen_trio:
                                    for y in kakkoslinjojen_trio:
                                        suojellut_ruudut.append((y, x))
                            for kakkoslinja in kakkoslinjojen_trio: 
                                for (y, x) in talon_ruudut(kakkoslinja, tyyppi_2):
                                    if nro in mahdolliset[y][x] and (y, x) not in suojellut_ruudut:
                                        mahdolliset[y][x].remove(nro) #
                                        # print(f"poistettu {nro} ruudusta {(y, x)}")
                                        eteni += 1
    return eteni

def brute_force(sudoku:list, mahdolliset: list, puhelias: bool = False, viive: int = 0) -> list:
    global yrityksia
    ratkaisemattomat_ruudut = []
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                ratkaisemattomat_ruudut.append((y, x))
    if len(ratkaisemattomat_ruudut) == 0:
        return sudoku
    for y, x in ratkaisemattomat_ruudut:
        for nro in mahdolliset[y][x]:
            if kelpaako_ruutuun(y, x, nro, sudoku):
                sudoku[y][x] = nro
                yrityksia += 1
                if puhelias:
                    print(chr(27) + "[2J")
                    tulosta_sudoku(sudoku)
                    if viive != 0:
                        time.sleep(viive / 1000)
                sudoku = brute_force(sudoku, mahdolliset, puhelias, viive)
            if onko_ratkaistu(sudoku):
                return sudoku
            sudoku[y][x] = 0
        return sudoku
        



if __name__ == "__main__":
    sudoku = ota_sudoku()
    nimi = input("Anna sudokullesi nimi: ")
    with open("sudokut.txt", "a") as kokoelma:
        kokoelma.write(f"\n{nimi} = {sudoku}\n")
    time.sleep(2)
    ratkaise_sudoku(sudoku)

    with open("sudokut.txt", "a") as kokoelma:
        kokoelma.write("Ratkesi\n")
    
