# Webcam Filtri in Real Time
### Python + OpenCV

---

## Requisiti

```bash
pip install opencv-python numpy
```

> Python 3.8+ consigliato.

---

## Avvio

```bash
# 1. Genera gli asset PNG placeholder (solo la prima volta)
python genera_assets.py

# 2. Avvia l'applicazione
python main.py
```

Sostituire i file in `assets/` con PNG reali a 4 canali (BGRA) per un risultato migliore negli overlay.

---

## Comandi tastiera

| Tasto | Azione |
|-------|--------|
| `← →` | Filtro precedente / successivo |
| `1`–`9` | Selezione diretta filtro |
| `B` | Sfondo sfocato (portrait mode) |
| `G` | Ghost effect (scia) |
| `M` | Rilevamento movimento |
| `C` | Overlay cappello |
| `O` | Overlay occhiali |
| `X` | Overlay maschera |
| `L` | Etichetta nome sopra il viso |
| `F` | Flip specchio (selfie mode) |
| `A` | Modalità auto (scorrimento filtri) |
| `S` | Screenshot (salvato in `screenshots/`) |
| `R` | Avvia/ferma registrazione (in `recordings/`) |
| `H` | Mostra/nascondi aiuto |
| `Q` / `ESC` | Esci |

---

## Filtri disponibili

| N. | Nome | Descrizione |
|----|------|-------------|
| 1 | Normale | Frame originale |
| 2 | Grigio | Scala di grigi |
| 3 | Negativo | Inversione colori |
| 4 | Sepia | Tonalità calda seppia |
| 5 | Heatmap | Visione termica (COLORMAP_JET) |
| 6 | Cartoon | Bilateral filter + bordi Canny |
| 7 | Pixelate | Effetto pixel art |
| 8 | Vignetta | Bordi scuri graduali |
| 9 | Solarize | Inversione parziale |
| 0 | MotionBlur | Mosso orizzontale simulato |

---

## Struttura progetto

```
webcam_filtri/
├── main.py           # Loop principale, tasti, orchestrazione
├── filters.py        # Filtri colore (grigio, negativo, cartoon…)
├── effects.py        # Effetti con face detection e frame-diff
├── ui.py             # HUD, barra filtri, testo on-screen
├── genera_assets.py  # Genera PNG placeholder per gli overlay
├── README.md
└── assets/
    ├── cappello.png  # PNG BGRA — sostituibile con versione reale
    ├── occhiali.png
    └── maschera.png
```

---

## HUD in tempo reale

Nell'angolo in alto a sinistra sono sempre visibili:
- **FILTRO** — nome del filtro attivo (+ effetti sovrapposti)
- **FACCE** — numero di volti rilevati via Haar Cascade
- **FPS** — frame rate calcolato in real time

Un **indicatore rosso ● REC** appare in alto a destra durante la registrazione.
Un **indicatore verde ⟳ AUTO** appare quando è attiva la modalità automatica.

---

## Note

- Gli screenshot vengono salvati in `screenshots/screenshot_YYYYMMDD_HHMMSS.jpg`
- Le registrazioni in `recordings/rec_YYYYMMDD_HHMMSS.mp4`
- La modalità automatica scorre i filtri ogni **3 secondi** (modificabile in `main.py`: `AUTO_MODE_INTERVAL`)
- L'etichetta del viso è configurabile in `main.py`: `FACE_LABEL_TEXT`
