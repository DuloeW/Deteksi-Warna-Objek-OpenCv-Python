
# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2

# initialize the shape detector and color labeler
sd = ShapeDetector()
cl = ColorLabeler()

# Inisialisasi video capture, shape detector, dan color labeler
cap = cv2.VideoCapture(1)
sd = ShapeDetector()
cl = ColorLabeler()

# Loop utama
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocessing untuk deteksi bentuk
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    canny_edges = cv2.Canny(blurred, 50, 150)

    # Preprocessing untuk deteksi warna (Konversi ke LAB color space)
    # Ini dilakukan sekali per frame
    lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # Temukan kontur
    contours, _ = cv2.findContours(canny_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop melalui setiap kontur
    for c in contours:
        if cv2.contourArea(c) < 800:
            continue

        # Deteksi bentuk
        shape = sd.detect(c)

        # Jika bentuknya adalah yang kita inginkan, lanjutkan deteksi warna
        if shape in ["circle", "square", "rectangle"]:
            # Deteksi warna
            color = cl.label(lab_frame, c)

            # Gabungkan label warna dan bentuk
            text = f"{color} {shape}"

            # Dapatkan koordinat untuk menggambar teks
            M = cv2.moments(c)
            if M["m00"] == 0: continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Gambar kontur dan teks gabungan pada frame
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.putText(frame, text, (cX - 40, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)

    # Tampilkan hasilnya
    cv2.imshow("Shape and Color Detection", frame)

    # Tekan 'q' untuk keluar
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()