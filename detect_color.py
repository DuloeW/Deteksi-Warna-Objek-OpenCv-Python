
# Import library yang diperlukan
from pyimagesearch.shapedetector import ShapeDetector  # Untuk deteksi bentuk
from pyimagesearch.colorlabeler import ColorLabeler    # Untuk deteksi warna
import imutils
import cv2


def get_detection_rules(mode):
    # (Fungsi ini sama seperti yang Anda buat)
    if mode == "object_indoor":
        return [{"label": "Object indoor", "shape": "circle", "color": "orange"}]
    elif mode == "drop_indoor":
        return [{"label": "Drop indoor", "shape": "circle", "color": "red"}]
    elif mode == "exit_gate":
        return [{"label": "Exit Gate", "shape": "rectangle", "color": "orange"}]
    elif mode == "drop_outdoor":
        return [{"label": "Drop outdoor", "shape": "square", "color": "orange", "child_shape": "circle", "child_color": "white"}]
    elif mode == "finish_start_right":
        return [{"label": "Finish Start Right", "shape": "square", "color": "blue"}]
    elif mode == "finish_start_left":
        return [{"label": "Finish Start Left", "shape": "square", "color": "red"}]
    else:
        return []

# --- Inisialisasi ---
cap = cv2.VideoCapture(1) 
sd = ShapeDetector()
cl = ColorLabeler()
current_mode = "object_indoor" 
detection_rules = get_detection_rules(current_mode)
print(f"Mode deteksi aktif: {current_mode}")

# --- BARU: Variabel untuk Filter Temporal ---
last_known_label = None
last_known_position = None
frames_since_disappeared = 0
DISAPPEARANCE_THRESHOLD = 10 

# --- Loop Utama ---
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = imutils.resize(frame, width=600)
    
    # --- Preprocessing (Menggunakan pipeline Anda yang sudah teruji) ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = clahe.apply(hsv[:,:,2])
    corrected_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lab_frame = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2LAB)
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
    canny_edges = cv2.Canny(blurred, 30, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    combined = cv2.morphologyEx(canny_edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # --- TAHAP 1: DETEKSI OBJEK (Mencari) ---
    contours, hierarchy = cv2.findContours(combined.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    object_detected_this_frame = False

    if hierarchy is not None:
        hierarchy = hierarchy[0]
        used_child = set()
        for i, c in enumerate(contours):
            if object_detected_this_frame: break # Jika sudah ketemu, stop
            if cv2.contourArea(c) < 150: continue
            
            shape = sd.detect(c)
            color = cl.label(lab_frame, c)

            for rule in detection_rules:
                # Mengembalikan logika deteksi asli Anda yang sudah detail
                if "child_shape" in rule:
                    child_index = hierarchy[i][2]
                    if (shape == rule["shape"] and color.startswith(rule["color"]) and
                        child_index != -1 and child_index not in used_child):
                        # ... Logika deteksi anak/child ...
                        pass # Dibiarkan kosong sesuai kode asli Anda
                elif (shape == rule["shape"] and color.startswith(rule["color"])):
                    # --- MODIFIKASI: Jika objek ditemukan, update state filter ---
                    object_detected_this_frame = True
                    frames_since_disappeared = 0 
                    M = cv2.moments(c)
                    if M["m00"] > 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        last_known_label = rule["label"]
                        last_known_position = (cX, cY, c)
                    break # Keluar dari loop 'for rule'

    # --- TAHAP 2: TAMPILAN (Menggambar) ---
    if not object_detected_this_frame:
        frames_since_disappeared += 1

    # Menggunakan "ingatan" untuk menampilkan hasil secara stabil
    if last_known_label is not None and frames_since_disappeared < DISAPPEARANCE_THRESHOLD:
        (cX, cY, last_contour) = last_known_position
        cv2.drawContours(frame, [last_contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, last_known_label, (cX - 50, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

    # Tampilkan window hasil
    cv2.imshow("Deteksi Objek Stabil", frame)
    cv2.imshow("Threshold (Hasil Preprocessing)", combined)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resource
cap.release()
cv2.destroyAllWindows()