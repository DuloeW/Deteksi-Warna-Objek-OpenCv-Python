
# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2

# initialize the shape detector and color labeler
sd = ShapeDetector()
cl = ColorLabeler()

# open webcam
cap = cv2.VideoCapture(1)

# Inisialisasi ShapeDetector
sd = ShapeDetector()

# Loop utama untuk memproses setiap frame dari video
while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil frame dari kamera.")
        break

    # Preprocessing frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    canny_edges = cv2.Canny(blurred, 50, 150)

    # Temukan kontur
    contours, _ = cv2.findContours(canny_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop melalui setiap kontur yang relevan
    for c in contours:
        # Filter kontur kecil yang kemungkinan besar adalah noise
        if cv2.contourArea(c) < 800:
            continue

        # Dapatkan nama bentuk dari kontur
        shape = sd.detect(c)

        # --- KUNCI UTAMA: Hanya gambar jika bentuknya adalah yang kita inginkan ---
        if shape in ["circle", "square", "rectangle"]:
            # Dapatkan koordinat untuk menggambar
            M = cv2.moments(c)
            if M["m00"] == 0: continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Gambar kontur dan label nama bentuk pada frame
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.putText(frame, shape, (cX - 25, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)

    # Tampilkan frame hasil deteksi
    cv2.imshow("Shape Detection (Live)", frame)

    # Tombol untuk keluar dari loop (tekan 'q')
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Hentikan video capture dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()