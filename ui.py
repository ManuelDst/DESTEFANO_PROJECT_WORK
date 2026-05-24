
import cv2
import numpy as np
import time

FONT        = cv2.FONT_HERSHEY_DUPLEX
FONT_SMALL  = cv2.FONT_HERSHEY_SIMPLEX
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (80, 220, 80)
COLOR_CYAN  = (255, 220, 0)
COLOR_ACCENT= (0, 200, 255)
ALPHA_BG    = 0.45


def _shadow_text(img, text, pos, font=FONT, scale=0.55, color=COLOR_WHITE, thickness=1):

    x, y = pos
    cv2.putText(img, text, (x+1, y+1), font, scale, COLOR_BLACK, thickness+1, cv2.LINE_AA)
    cv2.putText(img, text, (x,   y),   font, scale, color,       thickness,   cv2.LINE_AA)


def _rect_alpha(img, x1, y1, x2, y2, color=(20,20,20), alpha=ALPHA_BG):

    ov = img.copy()
    cv2.rectangle(ov, (x1,y1), (x2,y2), color, -1)
    cv2.addWeighted(ov, alpha, img, 1-alpha, 0, img)


def draw_hud(frame, filter_name, face_count, fps, recording=False):

    h, w = frame.shape[:2]


    _rect_alpha(frame, 8, 8, 310, 115)

    _shadow_text(frame, f"FILTRO : {filter_name.upper()}", (16, 30),  color=COLOR_ACCENT)
    _shadow_text(frame, f"FACCE  : {face_count}",          (16, 54),  color=COLOR_GREEN)
    _shadow_text(frame, f"FPS    : {fps:.1f}",             (16, 78),  color=COLOR_WHITE)
    _shadow_text(frame, "H = istruzioni",                  (16, 102), color=COLOR_CYAN, scale=0.48)

    # Indicatore REC lampeggiante in alto a destra
    if recording:
        _rect_alpha(frame, w-130, 8, w-8, 38, color=(0,0,160))
        if int(time.time() * 2) % 2 == 0:
            cv2.circle(frame, (w-110, 23), 7, (50,50,255), -1)
        _shadow_text(frame, "REC", (w-95, 28), color=(80,80,255))

    return frame


def draw_filter_bar(frame, filter_list, active_index):
    """
    Disegna nella parte bassa del frame una barra orizzontale con tutti i filtri.
    Il filtro attivo è evidenziato in arancione.

    """
    h, w   = frame.shape[:2]
    bar_h  = 38
    y0     = h - bar_h
    _rect_alpha(frame, 0, y0, w, h, color=(10,10,10), alpha=0.65)

    n      = len(filter_list)
    slot_w = w // n

    for i, name in enumerate(filter_list):
        x         = i * slot_w
        is_active = (i == active_index)
        if is_active:
            cv2.rectangle(frame, (x+2, y0+2), (x+slot_w-2, h-2), (0,180,255), -1)
            col = COLOR_BLACK
        else:
            col = COLOR_WHITE
        label = name[:9]
        sz    = cv2.getTextSize(label, FONT_SMALL, 0.40, 1)[0]
        tx    = x + (slot_w - sz[0]) // 2
        ty    = y0 + 25
        cv2.putText(frame, label, (tx, ty), FONT_SMALL, 0.40, col, 1, cv2.LINE_AA)

    return frame


def draw_screenshot_flash(frame):
    """
    Sovrappone un flash bianco semi-trasparente per simulare
    lo scatto di una foto quando si preme S.
    """
    ov = np.ones_like(frame, dtype=np.uint8) * 255
    return cv2.addWeighted(frame, 0.35, ov, 0.65, 0)


def draw_help_overlay(frame):
    """
    Mostra una schermata di aiuto semi-trasparente con tutti i comandi
    disponibili.
    """
    h, w = frame.shape[:2]
    ov   = frame.copy()
    cv2.rectangle(ov, (30,30), (w-30, h-30), (15,15,15), -1)
    cv2.addWeighted(ov, 0.82, frame, 0.18, 0, frame)

    cmds = [
        ("COMANDI",            None),
        ("",                   None),
        ("A / D",              "Cambia filtro"),
        ("S",                  "Screenshot"),
        ("R",                  "Avvia/Ferma registrazione"),
        ("H",                  "Mostra/Nascondi istruzioni"),
        ("Q / ESC",            "Esci"),
    ]
    y = 80
    for key, desc in cmds:
        if desc is None:
            cv2.putText(frame, key, (60, y), FONT, 0.8, COLOR_ACCENT, 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, key,  (60,  y), FONT_SMALL, 0.52, COLOR_CYAN,  1, cv2.LINE_AA)
            cv2.putText(frame, desc, (320, y), FONT_SMALL, 0.52, COLOR_WHITE, 1, cv2.LINE_AA)
        y += 35
    return frame