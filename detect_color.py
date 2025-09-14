
# Import library yang diperlukan
from pyimagesearch.shapedetector import ShapeDetector  # Untuk deteksi bentuk
from pyimagesearch.colorlabeler import ColorLabeler    # Untuk deteksi warna
import imutils
import cv2

# Inisialisasi
cap = cv2.VideoCapture(1) 
sd = ShapeDetector()
cl = ColorLabeler()

# Fungsi untuk memilih detection rules sesuai kondisi
def get_detection_rules(mode):
    if mode == "object_indoor":
        return [
            {"label": "Object indoor", "shape": "circle", "color": "orange"},
        ]
    elif mode == "drop_indoor":
        return [
            {"label": "Drop indoor", "shape": "circle", "color": "red"},
        ]
    elif mode == "exit_gate":
        return [
            {"label": "Exit Gate", "shape": "rectangle", "color": "orange"},
        ]
    elif mode == "drop_outdoor":
        return [
            {"label": "Drop outdoor", "shape": "square", "color": "orange", "child_shape": "circle", "child_color": "white"},
        ]
    elif mode == "finish_start_right":
        return [
            {"label": "Finish Start Right", "shape": "square", "color": "blue"},
        ]
    elif mode == "finish_start_left":
        return [
            {"label": "Finish Start Left", "shape": "square", "color": "red"},
        ]
    else:
        return []

# Contoh: mode awal, bisa diganti ke mode lain sesuai kebutuhan
current_mode = "object_indoor"  # Pilihan: object_indoor, drop_indoor, exit_gate, drop_outdoor, finish_start_right, finish_start_left
detection_rules = get_detection_rules(current_mode)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = imutils.resize(frame, width=600)
    # Mengurangi efek bayangan dengan histogram equalization
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Untuk color labeling, gunakan frame yang brightness-corrected
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = clahe.apply(hsv[:,:,2])  # Enhance value channel
    corrected_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lab_frame = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2LAB)
    
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)

    # Multiple thresholding untuk menangani variasi pencahayaan
    _, thresh1 = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    _, thresh2 = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV)
    adaptive = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
    
    canny_edges = cv2.Canny(blurred, 40, 120)
    
    # Gabungkan semua hasil
    combined = cv2.bitwise_or(thresh1, thresh2)
    combined = cv2.bitwise_or(combined, adaptive)
    combined = cv2.bitwise_or(combined, canny_edges)
    
    # Morphological closing untuk menyambung kontur yang terputus
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel, iterations=2)

    # --- Border area tengah ---
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    box_w, box_h = int(w * 0.2), int(h * 0.2)  # 20% area tengah
    box_x1, box_y1 = center_x - box_w // 2, center_y - box_h // 2
    box_x2, box_y2 = center_x + box_w // 2, center_y + box_h // 2
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 0, 0), 2)

    contours, hierarchy = cv2.findContours(combined.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is not None:
        hierarchy = hierarchy[0]
        used_child = set()
        for i, c in enumerate(contours):
            if cv2.contourArea(c) < 200: continue  # Turunkan threshold untuk objek 3D
            shape = sd.detect(c)
            color = cl.label(lab_frame, c)

            for rule in detection_rules:
                # Aturan parent-child (Drop outdoor)
                if rule["label"] == "Drop outdoor":
                    child_index = hierarchy[i][2]
                    if (shape == rule["shape"] and color.startswith(rule["color"]) and
                        child_index != -1 and child_index not in used_child):
                        child_c = contours[child_index]
                        child_shape = sd.detect(child_c)
                        child_color = cl.label(lab_frame, child_c)
                        if child_shape == rule["child_shape"] and child_color == rule["child_color"]:
                            M = cv2.moments(c)
                            if M["m00"] == 0: continue
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                            cv2.putText(frame, rule["label"], (cX - 40, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (255, 255, 255), 2)
                            # Cek apakah objek di tengah
                            if box_x1 <= cX <= box_x2 and box_y1 <= cY <= box_y2:
                                cv2.putText(frame, "CENTERED", (center_x - 80, box_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                            used_child.add(child_index)
                            break
                # Aturan biasa
                elif (shape == rule["shape"] and color.startswith(rule["color"])):
                    M = cv2.moments(c)
                    if M["m00"] == 0: continue
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    cv2.putText(frame, rule["label"], (cX - 40, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (255, 255, 255), 2)
                    # Cek apakah objek di tengah
                    if box_x1 <= cX <= box_x2 and box_y1 <= cY <= box_y2:
                        cv2.putText(frame, "CENTERED", (center_x - 80, box_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                    break

    # Tampilkan window kontur (outline)
    outline_frame = frame.copy()
    cv2.drawContours(outline_frame, contours, -1, (0, 255, 255), 2)
    # cv2.imshow("Outline Kamera", outline_frame)
    # cv2.imshow("Threshold Kamera", combined)
    # cv2.imshow("Enhanced Gray", enhanced)
    # cv2.imshow("Corrected Frame", corrected_frame)

    cv2.imshow("Deteksi Objek Spesifik", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()