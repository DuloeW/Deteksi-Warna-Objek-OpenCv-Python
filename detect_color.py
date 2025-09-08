
# Import library yang diperlukan
from pyimagesearch.shapedetector import ShapeDetector  # Untuk deteksi bentuk
from pyimagesearch.colorlabeler import ColorLabeler    # Untuk deteksi warna
import imutils
import cv2

# Inisialisasi
cap = cv2.VideoCapture(0) 
sd = ShapeDetector()
cl = ColorLabeler()

# Loop utama
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Ini membuat semua proses selanjutnya lebih cepat
    frame = imutils.resize(frame, width=600)

    # Dapatkan dimensi frame (setelah di-resize) untuk menentukan pusatnya
    (h, w) = frame.shape[:2]
    centerX_frame, centerY_frame = w // 2, h // 2

    # --- Preprocessing Gambar ---
    lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    canny_edges = cv2.Canny(blurred, 50, 150)

    # Temukan kontur
    contours, _ = cv2.findContours(canny_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop melalui setiap kontur
    for c in contours:
        # Nilai area minimum mungkin perlu disesuaikan karena frame lebih kecil
        if cv2.contourArea(c) < 500: # Sedikit diturunkan dari 800
            continue

        shape = sd.detect(c)

        if shape in ["circle", "square", "rectangle"]:
            color = cl.label(lab_frame, c)
            text = f"{color} {shape}"

            M = cv2.moments(c)
            if M["m00"] == 0: continue
            cX_obj = int(M["m10"] / M["m00"])
            cY_obj = int(M["m01"] / M["m00"])

            # --- Cek Posisi Objek ---
            tolerance = 35 
            in_horizontal_center = (centerX_frame - tolerance) < cX_obj < (centerX_frame + tolerance)
            in_vertical_center = (centerY_frame - tolerance) < cY_obj < (centerY_frame + tolerance)

            if in_horizontal_center and in_vertical_center:
                cv2.putText(frame, "CENTERED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1.2, (0, 255, 0), 3)

            # Gambar kontur dan label
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.putText(frame, text, (cX_obj - 40, cY_obj), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)

    # Tampilkan hasil
    cv2.imshow("Deteksi Objek (Optimasi)", frame)

    # Tekan 'q' untuk keluar
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Bersihkan resource
print("Menghentikan program...")
cap.release()
cv2.destroyAllWindows()