import cv2
import numpy as np

# --- 1. Class ShapeDetector yang Disederhanakan ---
# Class ini sekarang hanya akan mengidentifikasi segi empat dan lingkaran.
class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        # 1. Epsilon diturunkan agar lebih detail
        approx = cv2.approxPolyDP(c, 0.02 * peri, True) 

        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # Cek lagi dengan len(approx) > 6 atau 7 jika perlu
        elif len(approx) > 7:
            area = cv2.contourArea(c)
            if peri > 0:
                circularity = (4 * np.pi * area) / (peri * peri)
                # 2. Ambang batas sirkularitas diturunkan
                if circularity > 0.80:
                    shape = "circle"
        return shape
