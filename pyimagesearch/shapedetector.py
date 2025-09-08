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
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # Cek apakah bentuk adalah segi empat
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # Tentukan apakah itu persegi atau persegi panjang
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        
        # Cek apakah bentuk adalah lingkaran
        # Kita anggap lingkaran jika memiliki banyak sisi (>8) dan sirkularitas tinggi
        elif len(approx) > 8:
            area = cv2.contourArea(c)
            if peri > 0:
                circularity = (4 * np.pi * area) / (peri * peri)
                if circularity > 0.85:
                    shape = "circle"
        
        # Bentuk lain seperti segitiga, pentagon, dll. akan diabaikan (tetap "unidentified")
        return shape
