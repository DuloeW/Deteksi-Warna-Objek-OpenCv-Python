import cv2
import numpy as np

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # Inisialisasi nama bentuk
        shape = "unidentified"
        
        # Hitung perimeter dan lakukan aproksimasi kontur
        peri = cv2.arcLength(c, True)
        # Epsilon (parameter kedua) mungkin perlu disesuaikan, 0.02 - 0.04 adalah awal yang baik
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        # 1. Deteksi Segi Empat (Persegi atau Persegi Panjang)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
            
        # 2. Deteksi Lingkaran (menggunakan pendekatan sirkularitas)
        else:
            # Hitung area dan perimeter
            area = cv2.contourArea(c)
            
            # Hindari pembagian dengan nol jika perimeter adalah 0
            if peri > 0:
                # Hitung sirkularitas
                circularity = (4 * np.pi * area) / (peri * peri)
                
                # Tentukan ambang batas sirkularitas (misalnya, > 0.85)
                # Lingkaran cenderung memiliki > 8 sisi setelah aproksimasi
                if circularity > 0.85 and len(approx) > 8:
                    shape = "circle"

        # Kembalikan nama bentuk yang terdeteksi
        return shape