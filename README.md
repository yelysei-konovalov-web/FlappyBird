# Flappy Bird

Klon klasickej arkádovej hry Flappy Bird napísaný v Python pomocou knižnice Pygame.

---

## Cieľ projektu

Cieľom projektu je vytvoriť funkčnú repliku populárnej mobilnej hry Flappy Bird. Projekt demonštruje základné princípy
vývoja 2D hier: herná slučka, fyzika pohybu, detekcia kolízií, generovanie prekážok a správa herného stavu.

---

## Cieľová skupina

Projekt je určený pre:

- **Python nováčikovia** – ideálny štart pre herný vývoj.
- **Študenti** – praktická ukážka práce s Pygame.
- **Retro gameri** – možnosť upraviť a rozšíriť legendárnu klasiku.
- **Vývojári** – čistý a modulárny kód 2D hry ako inšpirácia.

---

## Priebeh hry

1. **Úvodná obrazovka** – Vták je nehybný uprostred obrazovky. Kliknutím spustíte hru.
2. **Hra** – Klikajte myšou, aby vták letel nahor. Gravitácia ho neustále ťahá nadol.
3. **Prekážky** – Dvojice rúr sa objavujú v pravidelných intervaloch s náhodnou výškou. Preleťte medzerami medzi nimi.
4. **Skóre** – Za každú úspešne prekonanú dvojicu rúr získate 1 bod. Skóre sa zobrazuje v hornej časti obrazovky.
5. **Koniec hry** – Hra končí, ak vták narazí do rúry, dotkne sa zeme alebo vyletí mimo horný okraj obrazovky. Zobrazí
   sa tlačidlo Restart.

---

## Štruktúra projektu

```
GAME/
├── app/
│   ├── main.py        # Vstupný bod, hlavná herná slučka
│   ├── config.py      # Konštanty (rozlíšenie, rýchlosť, fyzika)
│   ├── assets.py      # Načítanie obrázkov a zvukov
│   ├── entities.py    # Vytvorenie vtáka a rúr
│   ├── state.py       # Herný stav a reset
│   ├── events.py      # Spracovanie vstupov od hráča
│   ├── update.py      # Herná logika (fyzika, kolízie, skóre)
│   └── render.py      # Vykresľovanie na obrazovku
├── images/        # Grafické assety
├── sounds/        # Zvukové assety
└── README.md          # Dokumentácia projektu
```

## Popis modulov

- **`config.py`** – Centrálne nastavenia hry (rozlíšenie 864×936 px, FPS 60, rýchlosť posúvania, medzera medzi rúrami).
- **`assets.py`** – Načíta všetky obrázky a zvuky pri štarte.
- **`entities.py`** – Funkcie na vytvorenie herných objektov (vták, pár rúr s náhodnou polohou).
- **`state.py`** – Definuje a resetuje globálny stav hry (skóre, pozícia, príznaky).
- **`events.py`** – Spracováva udalosti (zatvorenie okna, klik na štart).
- **`update.py`** – Jadro hry: pohyb vtáka, gravitácia, animácie, posúvanie rúr, detekcia kolízií, počítanie skóre.
- **`render.py`** – Vykresľuje pozadie, rúry, vtáka, zem, skóre a tlačidlo reštartu.
- **`main.py`** – Inicializuje Pygame, spúšťa hernú slučku: `udalosti → update → render`.

---
