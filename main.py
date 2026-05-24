
import cv2
import numpy as np
import time, datetime, os, sys

import filters, effects, ui

#  Configurazione
WEBCAM_INDEX    = 0
WINDOW_NAME     = "Webcam Filtri  |  ← → cambia filtro  |  H aiuto  |  Q esci"
SCREENSHOTS_DIR = "screenshots"
RECORDINGS_DIR  = "recordings"
VIDEO_FPS       = 20.0

#  Lista UNICA di tutti i filtri
ALL_FILTERS = [
    ("Normale",    filters.apply_normal),
    ("Grigio",     filters.apply_grayscale),
    ("Negativo",   filters.apply_negative),
    ("Sepia",      filters.apply_sepia),
    ("Heatmap",    filters.apply_heatmap),
    ("Cartoon",    filters.apply_cartoon),
    ("Pixelate",   filters.apply_pixelate),
    ("Vignetta",   filters.apply_vignette),
    ("Solarize",   filters.apply_solarize),
    ("Blur BG",    effects.apply_background_blur),
    ("Cappello",   effects.apply_hat_overlay),
    ("Occhiali",   effects.apply_glasses_overlay),
    ("Six Seven",  effects.apply_mask_overlay),
]

FILTER_NAMES = [f[0] for f in ALL_FILTERS]


def ensure_dirs():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(RECORDINGS_DIR,  exist_ok=True)


def ts():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    ensure_dirs()

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print(f"[ERRORE] Webcam non trovata (indice {WEBCAM_INDEX}).")
        sys.exit(1)

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    active    = 0
    recording = False
    writer    = None
    rec_file  = ""
    flash     = 0
    show_help = False
    prev_t    = time.time()
    fps       = 0.0

    print("[INFO] Avviato. Premi H per i comandi.")

    while True:
        ret, raw = cap.read()
        if not ret:
            print("[ERRORE] Frame non disponibile")
            break

        # Flip specchio sempre attivo
        raw = cv2.flip(raw, 1)

        # Applica l'unico filtro attivo
        _, fn = ALL_FILTERS[active]
        frame = fn(raw)

        # FPS
        now    = time.time()
        fps    = 1.0 / (now - prev_t) if (now - prev_t) > 0 else fps
        prev_t = now

        # Conteggio facce per HUD
        faces   = effects.detect_faces(raw)
        n_faces = len(faces) if hasattr(faces, '__len__') else 0

        # UI
        frame = ui.draw_hud(frame, FILTER_NAMES[active], n_faces, fps, recording)
        frame = ui.draw_filter_bar(frame, FILTER_NAMES, active)
        if show_help:
            frame = ui.draw_help_overlay(frame)
        if flash > 0:
            frame = ui.draw_screenshot_flash(frame)
            flash -= 1

        # Registrazione
        if recording and writer is not None:
            writer.write(frame)

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        if key in (ord('q'), ord('Q'), 27):
            break
        elif key in (ord('a'), ord('A')):
            active = (active - 1) % len(ALL_FILTERS)
        elif key in (ord('d'), ord('D')):
            active = (active + 1) % len(ALL_FILTERS)
        elif key in (ord('s'), ord('S')):
            fname = os.path.join(SCREENSHOTS_DIR, f"screenshot_{ts()}.jpg")
            cv2.imwrite(fname, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"[SCREENSHOT] {fname}")
            flash = 4
        elif key in (ord('r'), ord('R')):
            if not recording:
                h, w     = frame.shape[:2]
                rec_file = os.path.join(RECORDINGS_DIR, f"rec_{ts()}.mp4")
                fourcc   = cv2.VideoWriter_fourcc(*"mp4v")
                writer   = cv2.VideoWriter(rec_file, fourcc, VIDEO_FPS, (w, h))
                recording= True
                print(f"[REC] Avviata: {rec_file}")
            else:
                writer.release()
                writer    = None
                recording = False
                print(f"[REC] Salvata: {rec_file}")
        elif key in (ord('h'), ord('H')):
            show_help = not show_help

    if recording and writer:
        writer.release()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Chiuso.")


if __name__ == "__main__":
    main()