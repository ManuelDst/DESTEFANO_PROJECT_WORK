
import cv2
import numpy as np


def apply_normal(frame):
    """Restituisce il frame originale senza modifiche."""
    return frame.copy()


def apply_grayscale(frame):
    """Converte il frame in scala di grigi."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_negative(frame):
    """Inverte i valori di tutti i pixel — effetto negativo fotografico."""
    return cv2.bitwise_not(frame.copy())


def apply_sepia(frame):
    """Applica una tonalità seppia """
    img = frame.copy().astype(np.float64)
    r, g, b = img[:,:,2], img[:,:,1], img[:,:,0]
    result = img.copy()
    result[:,:,2] = np.clip(r*0.393 + g*0.769 + b*0.189, 0, 255)
    result[:,:,1] = np.clip(r*0.349 + g*0.686 + b*0.168, 0, 255)
    result[:,:,0] = np.clip(r*0.272 + g*0.534 + b*0.131, 0, 255)
    return result.astype(np.uint8)


def apply_heatmap(frame):
    """Scala di grigi + colormap JET per simulare una visione termica."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)


def apply_cartoon(frame):
    """Effetto fumetto"""
    img = frame.copy()
    for _ in range(5):
        img = cv2.bilateralFilter(img, 9, 75, 75)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=2)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.bitwise_and(img, edges_bgr)


def apply_pixelate(frame, pixel_size=16):
    """Effetto pixel art: rimpicciolisce e riingrandisce con nearest neighbor."""
    h, w = frame.shape[:2]
    small = cv2.resize(frame, (w // pixel_size, h // pixel_size),
                       interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def apply_vignette(frame):
    """Vignettatura."""
    img = frame.copy()
    h, w = img.shape[:2]
    sigma = min(h, w) * 0.5
    Y = np.linspace(-h/2, h/2, h)
    X = np.linspace(-w/2, w/2, w)
    Xg, Yg = np.meshgrid(X, Y)
    mask = np.exp(-(Xg**2 + Yg**2) / (2 * sigma**2))
    mask = (mask / mask.max()).astype(np.float32)
    mask_3ch = np.stack([mask, mask, mask], axis=2)
    return (img.astype(np.float32) * mask_3ch).astype(np.uint8)


def apply_solarize(frame):
    """Solarizzazione: inverte solo i pixel sopra soglia 128."""
    img = frame.copy()
    mask = img > 128
    img[mask] = 255 - img[mask]
    return img


def apply_motion_blur(frame):
    """Motion blur simulato."""
    size = 20
    kernel = np.zeros((size, size))
    kernel[size // 2, :] = np.ones(size) / size
    return cv2.filter2D(frame.copy(), -1, kernel)