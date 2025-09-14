
# Import library yang diperlukan
from pyimagesearch.shapedetector import ShapeDetector  # Untuk deteksi bentuk
from pyimagesearch.colorlabeler import ColorLabeler    # Untuk deteksi warna
import imutils
import cv2
import numpy as np
import time

# Konfigurasi optimasi
class Config:
    FRAME_WIDTH = 600
    MIN_AREA = 150
    SKIP_FRAMES = 2  # Proses setiap 2 frame untuk meningkatkan FPS
    DISAPPEARANCE_THRESHOLD = 10
    
    # Parameter preprocessing yang sudah dioptimasi
    GAUSSIAN_KERNEL = (5, 5)
    CANNY_LOW = 30
    CANNY_HIGH = 150
    MORPH_KERNEL_SIZE = (3, 3)
    CLAHE_CLIP_LIMIT = 2.0
    CLAHE_TILE_SIZE = (8, 8)

# Fungsi utilitas menggunakan numpy
def calculate_object_stability(positions_history, max_history=10):
    """Hitung stabilitas posisi objek menggunakan standard deviation"""
    if len(positions_history) < 3:
        return 0.0
    
    positions = np.array(positions_history[-max_history:])
    std_dev = np.std(positions, axis=0)
    return np.mean(std_dev)

def get_object_velocity(positions_history):
    """Hitung kecepatan pergerakan objek"""
    if len(positions_history) < 2:
        return 0.0
    
    pos1 = np.array(positions_history[-2])
    pos2 = np.array(positions_history[-1])
    return np.linalg.norm(pos2 - pos1)


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

# --- Inisialisasi yang dioptimasi ---
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Kurangi buffer untuk latency rendah
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

sd = ShapeDetector()
cl = ColorLabeler()
current_mode = "object_indoor" 
detection_rules = get_detection_rules(current_mode)
print(f"Mode deteksi aktif: {current_mode}")

# Preprocessing objects yang di-cache untuk performa
clahe = cv2.createCLAHE(clipLimit=Config.CLAHE_CLIP_LIMIT, 
                        tileGridSize=Config.CLAHE_TILE_SIZE)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, Config.MORPH_KERNEL_SIZE)

# Variabel tracking dan filtering
last_known_label = None
last_known_position = None
frames_since_disappeared = 0
frame_count = 0

# Numpy arrays untuk tracking history
position_history = []
detection_confidence_history = []

# Performance monitoring
fps_start_time = time.time()
fps_frame_count = 0 

# --- Loop Utama Optimized ---
while True:
    ret, frame = cap.read()
    if not ret: 
        break
    
    frame_count += 1
    fps_frame_count += 1
    
    # Resize frame untuk performa
    frame = imutils.resize(frame, width=Config.FRAME_WIDTH)
    
    # Frame skipping untuk meningkatkan FPS
    process_frame = (frame_count % Config.SKIP_FRAMES == 0)
    
    if process_frame:
        # --- Preprocessing Pipeline Optimized ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = clahe.apply(gray)
        
        # Optimasi: Hanya lakukan color correction jika diperlukan
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] = clahe.apply(hsv[:,:,2])
        corrected_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        lab_frame = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2LAB)
        
        # Preprocessing yang efisien
        blurred = cv2.GaussianBlur(enhanced, Config.GAUSSIAN_KERNEL, 0)
        canny_edges = cv2.Canny(blurred, Config.CANNY_LOW, Config.CANNY_HIGH)
        combined = cv2.morphologyEx(canny_edges, cv2.MORPH_CLOSE, kernel, iterations=2)

        # --- TAHAP 1: DETEKSI OBJEK OPTIMIZED ---
        contours, hierarchy = cv2.findContours(combined.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        object_detected_this_frame = False

        if hierarchy is not None and len(contours) > 0:
            hierarchy = hierarchy[0]
            # Gunakan numpy untuk sorting yang lebih efisien
            areas = np.array([cv2.contourArea(c) for c in contours])
            sorted_indices = np.argsort(areas)[::-1]  # Descending order
            contours = [contours[i] for i in sorted_indices]
            
            for c in contours:
                if object_detected_this_frame: 
                    break  # Early exit jika sudah ketemu
                    
                area = cv2.contourArea(c)
                if area < Config.MIN_AREA: 
                    break  # Karena sudah diurutkan, yang lain pasti lebih kecil
                
                # Optimasi: Hitung shape dan color hanya jika area cukup
                shape = sd.detect(c)
                color = cl.label(lab_frame, c)

                for rule in detection_rules:
                    if (shape == rule["shape"] and color.startswith(rule["color"])):
                        # Update tracking state
                        object_detected_this_frame = True
                        frames_since_disappeared = 0 
                        
                        M = cv2.moments(c)
                        if M["m00"] > 0:
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                            
                            # Update tracking dengan numpy arrays
                            position_history.append([cX, cY])
                            if len(position_history) > 20:  # Keep only last 20 positions
                                position_history = position_history[-20:]
                            
                            # Hitung confidence berdasarkan area kontur
                            confidence = min(area / 1000.0, 1.0)  # Normalize to 0-1
                            detection_confidence_history.append(confidence)
                            if len(detection_confidence_history) > 10:
                                detection_confidence_history = detection_confidence_history[-10:]
                            
                            last_known_label = rule["label"]
                            last_known_position = (cX, cY, c.copy())
                        break
                        
    else:
        # Jika tidak ada processing frame, masih update counter
        pass

    # --- TAHAP 2: RENDERING & DISPLAY ---
    if process_frame and not object_detected_this_frame:
        frames_since_disappeared += 1

    # Stable tracking menggunakan "memory"
    if last_known_label is not None and frames_since_disappeared < Config.DISAPPEARANCE_THRESHOLD:
        (cX, cY, last_contour) = last_known_position
        
        # Border area tengah (optimasi: hitung sekali saja)
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        box_w, box_h = int(w * 0.2), int(h * 0.2)
        box_x1, box_y1 = center_x - box_w // 2, center_y - box_h // 2
        box_x2, box_y2 = center_x + box_w // 2, center_y + box_h // 2
        
        # Draw detection
        cv2.drawContours(frame, [last_contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, last_known_label, (cX - 50, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        
        # Draw center detection box
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 0, 0), 2)
        
        # Check if centered menggunakan numpy untuk perhitungan yang lebih efisien
        center_point = np.array([cX, cY])
        box_center = np.array([center_x, center_y])
        distance_from_center = np.linalg.norm(center_point - box_center)
        
        if box_x1 <= cX <= box_x2 and box_y1 <= cY <= box_y2:
            cv2.putText(frame, "CENTERED", (center_x - 80, box_y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
            cv2.putText(frame, f"Distance: {distance_from_center:.1f}px", 
                       (center_x - 80, box_y1 - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Performance monitoring
    if fps_frame_count % 30 == 0:  # Update FPS setiap 30 frame
        fps_end_time = time.time()
        fps = fps_frame_count / (fps_end_time - fps_start_time)
        fps_start_time = fps_end_time
        fps_frame_count = 0
        print(f"FPS: {fps:.1f} | Mode: {current_mode}")

    # Add status information to frame
    cv2.putText(frame, f"Mode: {current_mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Frame: {frame_count}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Numpy-based analytics display
    if len(position_history) > 2:
        stability = calculate_object_stability(position_history)
        velocity = get_object_velocity(position_history)
        avg_confidence = np.mean(detection_confidence_history) if detection_confidence_history else 0.0
        
        cv2.putText(frame, f"Stability: {stability:.1f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, f"Velocity: {velocity:.1f}px/f", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, f"Confidence: {avg_confidence:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    
    if not process_frame:
        cv2.putText(frame, "SKIPPED", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Display windows
    cv2.imshow("Deteksi Objek Optimized", frame)
    if process_frame:
        cv2.imshow("Preprocessing Result", combined)
    
    # Enhanced control keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):  # Reset tracking
        last_known_label = None
        last_known_position = None
        frames_since_disappeared = 0
        print("Tracking reset!")
    elif key == ord('1'):  # Object indoor
        current_mode = "object_indoor"
        detection_rules = get_detection_rules(current_mode)
        print(f"Mode switched to: {current_mode}")
    elif key == ord('2'):  # Drop indoor
        current_mode = "drop_indoor"
        detection_rules = get_detection_rules(current_mode)
        print(f"Mode switched to: {current_mode}")
    elif key == ord('3'):  # Exit gate
        current_mode = "exit_gate"
        detection_rules = get_detection_rules(current_mode)
        print(f"Mode switched to: {current_mode}")
    elif key == ord('4'):  # Finish start left
        current_mode = "finish_start_left"
        detection_rules = get_detection_rules(current_mode)
        print(f"Mode switched to: {current_mode}")
    elif key == ord('5'):  # Finish start right
        current_mode = "finish_start_right"
        detection_rules = get_detection_rules(current_mode)
        print(f"Mode switched to: {current_mode}")
    elif key == ord('h'):  # Help
        print("\n=== KEYBOARD CONTROLS ===")
        print("q: Quit")
        print("r: Reset tracking")
        print("1: Object indoor (orange circle)")
        print("2: Drop indoor (red circle)")
        print("3: Exit gate (orange rectangle)")
        print("4: Finish start left (red square)")
        print("5: Finish start right (blue square)")
        print("h: Show this help")
        print("==========================")

# === CLEANUP & RESOURCE MANAGEMENT ===
print("Shutting down...")
cap.release()
cv2.destroyAllWindows()

# Print final statistics
total_time = time.time() - fps_start_time
print(f"Total runtime: {total_time:.1f}s")
print(f"Total frames processed: {frame_count}")
print(f"Average FPS: {frame_count/total_time:.1f}")