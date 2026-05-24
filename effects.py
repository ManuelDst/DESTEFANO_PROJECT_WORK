
import cv2
import numpy as np
import os


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Percorso cartella assets
_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def detect_faces(frame):
    """
    Rileva i volti nel frame usando
    """
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(60, 60))
    return faces if len(faces) > 0 else []


def _load_asset(filename):
    """
    Carica un PNG dalla cartella assets con tutti i canali.
    Restituisce None se il file non esiste.
    """
    path = os.path.join(_ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)


def _overlay_png(background, overlay_img, x, y, target_w, target_h):

    if overlay_img is None or target_w <= 0 or target_h <= 0:
        return background

    ov     = cv2.resize(overlay_img, (target_w, target_h), interpolation=cv2.INTER_AREA)
    bg     = background.copy()
    bh, bw = bg.shape[:2]
    oh, ow = ov.shape[:2]

    x1, y1 = max(0, x),       max(0, y)
    x2, y2 = min(bw, x + ow), min(bh, y + oh)
    ox1     = x1 - x
    oy1     = y1 - y
    ox2     = ox1 + (x2 - x1)
    oy2     = oy1 + (y2 - y1)

    if x2 <= x1 or y2 <= y1:
        return bg

    roi     = bg[y1:y2, x1:x2]
    ov_crop = ov[oy1:oy2, ox1:ox2]


    if len(ov_crop.shape) == 2:
        bg[y1:y2, x1:x2] = cv2.cvtColor(ov_crop, cv2.COLOR_GRAY2BGR)


    elif ov_crop.shape[2] == 4:
        alpha   = ov_crop[:,:,3:4].astype(np.float32) / 255.0
        fg      = ov_crop[:,:,:3].astype(np.float32)
        blended = fg * alpha + roi.astype(np.float32) * (1.0 - alpha)
        bg[y1:y2, x1:x2] = blended.astype(np.uint8)


    else:
        bg[y1:y2, x1:x2] = ov_crop[:,:,:3]

    return bg


# Carica gli asset PNG una sola volta all'avvio del programma
_hat_img     = _load_asset("cappello.png")
_glasses_img = _load_asset("occhiali.png")
_mask_img    = _load_asset("six_seven.png")


def apply_background_blur(frame):
    """
    sfoca fortemente tutto il frame,
    poi ripristina nitida solo la regione del viso rilevato.

    """
    img     = frame.copy()
    blurred = cv2.GaussianBlur(img, (55, 55), 0)
    faces   = detect_faces(frame)
    if len(faces) == 0:
        return blurred
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    for (x, y, w, h) in faces:
        margin = int(0.15 * w)
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(img.shape[1], x + w + margin)
        y2 = min(img.shape[0], y + h + margin)
        mask[y1:y2, x1:x2] = 255
    mask   = cv2.GaussianBlur(mask, (21, 21), 0)
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0
    result = img.astype(np.float32) * mask_3 + blurred.astype(np.float32) * (1.0 - mask_3)
    return result.astype(np.uint8)


def apply_hat_overlay(frame):
    """
    Sovrappone cappello.png sopra il rettangolo del viso rilevato.
    Il cappello viene scalato alla larghezza del viso e posizionato
    immediatamente sopra di esso.
    """
    if _hat_img is None:
        img = frame.copy()
        cv2.putText(img, "cappello.png mancante in assets/",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return img
    img = frame.copy()
    for (x, y, w, h) in detect_faces(frame):
        hat_w = w
        hat_h = int(_hat_img.shape[0] * (hat_w / _hat_img.shape[1]))
        img   = _overlay_png(img, _hat_img, x, y - hat_h, hat_w, hat_h)
    return img


def apply_glasses_overlay(frame):
    """
    Sovrappone occhiali.png all'altezza degli occhi del viso rilevato.
    Usa la eye cascade per posizionamento preciso; se gli occhi non vengono
    rilevati, cade in un posizionamento di fallback al terzo superiore del viso.

    """
    if _glasses_img is None:
        img = frame.copy()
        cv2.putText(img, "occhiali.png mancante in assets/",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return img
    img  = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for (fx, fy, fw, fh) in detect_faces(frame):
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        eyes     = eye_cascade.detectMultiScale(roi_gray, 1.1, 5, minSize=(20, 20))
        if len(eyes) >= 2:
            eyes_sorted = sorted(eyes, key=lambda e: e[0])
            ex  = fx + eyes_sorted[0][0]
            ey  = fy + eyes_sorted[0][1]
            ew  = (eyes_sorted[-1][0] + eyes_sorted[-1][2]) - eyes_sorted[0][0]
            eh  = int(ew * _glasses_img.shape[0] / _glasses_img.shape[1])
            img = _overlay_png(img, _glasses_img, ex, ey - eh // 4, ew, eh)
        else:
            gw  = fw
            gh  = int(fw * _glasses_img.shape[0] / _glasses_img.shape[1])
            img = _overlay_png(img, _glasses_img, fx, fy + fh // 4, gw, gh)
    return img


def apply_mask_overlay(frame):
    """
    Sovrappone six_seven.png sopra la testa di ogni volto rilevato.
    L'immagine viene scalata alla larghezza del viso e posizionata
    immediatamente sopra il rettangolo del viso.

    """
    if _mask_img is None:
        img = frame.copy()
        cv2.putText(img, "six_seven.png mancante in assets/",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return img
    img = frame.copy()
    for (x, y, w, h) in detect_faces(frame):
        img_w = w
        img_h = int(_mask_img.shape[0] * (img_w / _mask_img.shape[1]))
        pos_x = x
        pos_y = y - img_h  # sopra il rettangolo del viso
        img   = _overlay_png(img, _mask_img, pos_x, pos_y, img_w, img_h)
    return img