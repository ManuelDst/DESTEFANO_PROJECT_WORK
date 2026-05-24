# \# Filtri Webcam in Real Time

# 

# Applicazione desktop sviluppata in Python e OpenCV che applica filtri ed effetti visivi in tempo reale alla webcam.  

# Il progetto include face detection, overlay grafici, screenshot, registrazione video e una HUD interattiva controllata da tastiera.  

# L’obiettivo è offrire un sistema stabile, modulare e facilmente eseguibile anche su Raspberry Pi.

# 

# \---

# 

# \# Requisiti

# 

# \## Software

# \- Python 3.10 o superiore

# \- pip

# \- OpenCV

# \- NumPy

# 

# \## Hardware

# \- Webcam USB o webcam integrata

# \- Tastiera

# 

# \## Sistemi Operativi supportati

# \- Windows

# \- Linux

# \- Raspberry Pi OS

# 

# \---

# 

# \# Struttura del progetto

# 

# ```text

# progetto/

# │

# ├── main.py

# ├── filters.py

# ├── effects.py

# ├── ui.py

# ├── requirements.txt

# ├── README.md

# ├── run.sh

# │

# ├── assets/

# │   ├── cappello.png

# │   ├── occhiali.png

# │   └── six\_seven.png

# │

# ├── screenshots/

# └── recordings/

# ```

# 

# \---

# 

# \# Installazione

# 

# \---

# 

# 

# \## Installare le dipendenze

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# \---

# 

# \# Avvio del progetto

# 

# \## Metodo classico

# 

# ```bash

# python main.py

# ```

# 

# oppure su Linux/Raspberry:

# 

# ```bash

# python3 main.py

# ```

# 

# \---

# 

# \## Avvio tramite script

# 

# ```bash

# ./run.sh

# ```

# 

# \---

# 

# \# Filtri disponibili

# 

# \- Normale

# \- Scala di grigi

# \- Negativo

# \- Sepia

# \- Heatmap

# \- Cartoon

# \- Pixelate

# \- Vignettatura

# \- Solarize

# \- Blur sfondo

# \- Cappello overlay

# \- Occhiali overlay

# \- Maschera overlay

# 

# \---

# 

# \# Funzionalità principali

# 

# \## Face Detection

# Il programma utilizza Haar Cascade di OpenCV per rilevare i volti in tempo reale.

# 

# \## Background Blur

# Lo sfondo viene sfocato mantenendo il volto nitido.

# 

# \## Overlay PNG

# Cappelli, occhiali e maschere vengono sovrapposti usando immagini PNG con canale alpha.

# 

# \## HUD Real Time

# Sono visualizzati:

# \- filtro attivo

# \- numero facce rilevate

# \- FPS correnti

# \- stato registrazione

# 

# \## Screenshot

# Premendo il tasto `S` viene salvata un’immagine `.jpg` con timestamp automatico.

# 

# \## Registrazione Video

# Premendo `R` si avvia o interrompe la registrazione video `.mp4`.

# 

# \---

# 

# \# Controlli da tastiera

# 

# | Tasto | Azione |

# |------|---------|

# | A | Filtro precedente |

# | D | Filtro successivo |

# | S | Salva screenshot |

# | R | Avvia/Ferma registrazione |

# | H | Mostra/Nascondi help |

# | Q | Esci dal programma |

# | ESC | Esci dal programma |

# 

# \---

# 

# \# Screenshot e registrazioni

# 

# \## Screenshot

# Le immagini vengono salvate nella cartella:

# 

# ```text

# screenshots/

# ```

# 

# Formato nome file:

# 

# ```text

# screenshot\_YYYYMMDD\_HHMMSS.jpg

# ```

# 

# \---

# 

# \## Registrazioni video

# I video vengono salvati nella cartella:

# 

# ```text

# recordings/

# ```

# 

# Formato nome file:

# 

# ```text

# rec\_YYYYMMDD\_HHMMSS.mp4

# ```

# 

# \---

# 

# \# Note per Raspberry Pi

# 

# Il progetto è compatibile con Raspberry Pi dotato di webcam USB.

# 

# Su Raspberry Pi potrebbe essere necessario installare OpenCV tramite:

# 

# ```bash

# sudo apt update

# sudo apt install python3-opencv

# ```

# 

# 

# 

# \---

# 

# \# Dipendenze principali

# 

# \- opencv-python

# \- numpy

# 

# \---

# 

# 

