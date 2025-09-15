"""
Testing Performance: Deteksi Warna vs Bentuk
============================================
File ini untuk menganalisis performa deteksi warna dan bentuk secara terpisah
untuk mengetahui mana yang kurang bagus dan perlu diperbaiki.
"""

# Import library yang diperlukan
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2
import numpy as np
import time
from collections import defaultdict, deque
import json


class DetectionTester:
    def __init__(self):
        self.sd = ShapeDetector()
        self.cl = ColorLabeler()
        
        # Statistics tracking
        self.color_stats = defaultdict(lambda: {"correct": 0, "total": 0, "confidence": []})
        self.shape_stats = defaultdict(lambda: {"correct": 0, "total": 0, "confidence": []})
        
        # Detection history untuk analisis temporal
        self.detection_history = deque(maxlen=100)
        self.ground_truth = None
        
        # Testing modes
        self.test_modes = {
            "color_only": "Test hanya deteksi warna",
            "shape_only": "Test hanya deteksi bentuk", 
            "combined": "Test gabungan warna + bentuk",
            "comparison": "Bandingkan semua method"
        }
        
        self.current_test_mode = "comparison"
        
    def set_ground_truth(self, expected_color, expected_shape):
        """Set ground truth untuk objek yang sedang ditest"""
        self.ground_truth = {
            "color": expected_color,
            "shape": expected_shape
        }
        print(f"Ground truth set: {expected_color} {expected_shape}")
        
    def analyze_contour(self, frame, contour, lab_frame):
        """Analisis detail satu kontur"""
        results = {}
        
        # Shape detection
        detected_shape = self.sd.detect(contour)
        results["shape"] = detected_shape
        
        # Color detection
        detected_color = self.cl.label(lab_frame, contour)
        results["color"] = detected_color
        
        # Confidence metrics
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Shape confidence (berdasarkan aspek ratio dan circularity)
        if area > 0 and perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            results["shape_confidence"] = min(circularity * 2, 1.0) if detected_shape == "circle" else (1.0 - circularity)
            
            # Aspect ratio untuk rectangle/square
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if detected_shape in ["rectangle", "square"]:
                if detected_shape == "square":
                    results["shape_confidence"] = 1.0 - abs(1.0 - aspect_ratio)
                else:
                    results["shape_confidence"] = min(abs(aspect_ratio - 1.5), 1.0)
        else:
            results["shape_confidence"] = 0.0
            
        # Color confidence (berdasarkan area dan posisi)
        results["color_confidence"] = min(area / 1000.0, 1.0)
        
        return results
        
    def evaluate_detection(self, results):
        """Evaluasi hasil deteksi dengan ground truth"""
        if not self.ground_truth:
            return None
            
        evaluation = {
            "color_correct": results["color"].startswith(self.ground_truth["color"]),
            "shape_correct": results["shape"] == self.ground_truth["shape"],
            "color_confidence": results["color_confidence"],
            "shape_confidence": results["shape_confidence"]
        }
        
        # Update statistics
        color_key = self.ground_truth["color"]
        shape_key = self.ground_truth["shape"]
        
        self.color_stats[color_key]["total"] += 1
        self.shape_stats[shape_key]["total"] += 1
        
        if evaluation["color_correct"]:
            self.color_stats[color_key]["correct"] += 1
        if evaluation["shape_correct"]:
            self.shape_stats[shape_key]["correct"] += 1
            
        self.color_stats[color_key]["confidence"].append(evaluation["color_confidence"])
        self.shape_stats[shape_key]["confidence"].append(evaluation["shape_confidence"])
        
        return evaluation
        
    def get_performance_summary(self):
        """Dapatkan ringkasan performa"""
        summary = {
            "color_performance": {},
            "shape_performance": {},
            "overall": {}
        }
        
        # Color performance
        total_color_correct = total_color_tests = 0
        for color, stats in self.color_stats.items():
            if stats["total"] > 0:
                accuracy = stats["correct"] / stats["total"]
                avg_confidence = np.mean(stats["confidence"]) if stats["confidence"] else 0
                summary["color_performance"][color] = {
                    "accuracy": accuracy,
                    "avg_confidence": avg_confidence,
                    "total_tests": stats["total"]
                }
                total_color_correct += stats["correct"]
                total_color_tests += stats["total"]
                
        # Shape performance  
        total_shape_correct = total_shape_tests = 0
        for shape, stats in self.shape_stats.items():
            if stats["total"] > 0:
                accuracy = stats["correct"] / stats["total"]
                avg_confidence = np.mean(stats["confidence"]) if stats["confidence"] else 0
                summary["shape_performance"][shape] = {
                    "accuracy": accuracy,
                    "avg_confidence": avg_confidence,
                    "total_tests": stats["total"]
                }
                total_shape_correct += stats["correct"]
                total_shape_tests += stats["total"]
                
        # Overall performance
        summary["overall"] = {
            "color_accuracy": total_color_correct / total_color_tests if total_color_tests > 0 else 0,
            "shape_accuracy": total_shape_correct / total_shape_tests if total_shape_tests > 0 else 0,
            "total_tests": max(total_color_tests, total_shape_tests)
        }
        
        return summary
        
    def draw_analysis_overlay(self, frame, results, evaluation=None):
        """Gambar overlay analisis di frame"""
        h, w = frame.shape[:2]
        
        # Background untuk text
        overlay = frame.copy()
        cv2.rectangle(overlay, (w-300, 0), (w, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Detection results
        y_offset = 25
        cv2.putText(frame, "DETECTION ANALYSIS", (w-290, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        y_offset += 25
        cv2.putText(frame, f"Shape: {results['shape']}", (w-290, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        y_offset += 20
        cv2.putText(frame, f"Color: {results['color']}", (w-290, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        y_offset += 20
        cv2.putText(frame, f"Shape Conf: {results['shape_confidence']:.2f}", (w-290, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        
        y_offset += 15
        cv2.putText(frame, f"Color Conf: {results['color_confidence']:.2f}", (w-290, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        
        if evaluation:
            y_offset += 25
            shape_color = (0, 255, 0) if evaluation["shape_correct"] else (0, 0, 255)
            color_color = (0, 255, 0) if evaluation["color_correct"] else (0, 0, 255)
            
            cv2.putText(frame, f"Shape: {'CORRECT' if evaluation['shape_correct'] else 'WRONG'}", 
                       (w-290, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, shape_color, 1)
            
            y_offset += 15
            cv2.putText(frame, f"Color: {'CORRECT' if evaluation['color_correct'] else 'WRONG'}", 
                       (w-290, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color_color, 1)
        
        return frame


def main():
    # Inisialisasi
    tester = DetectionTester()
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # CLAHE untuk preprocessing
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    
    print("=== DETECTION PERFORMANCE TESTER ===")
    print("Controls:")
    print("1-6: Set ground truth (1=red circle, 2=blue square, etc.)")
    print("s: Save performance report")
    print("r: Reset statistics")
    print("q: Quit")
    print("=====================================")
    
    ground_truth_options = {
        ord('1'): ("red", "circle"),
        ord('2'): ("blue", "square"), 
        ord('3'): ("orange", "circle"),
        ord('4'): ("red", "square"),
        ord('5'): ("orange", "rectangle"),
        ord('6'): ("blue", "circle"),
    }
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = imutils.resize(frame, width=800)
        
        # Preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = clahe.apply(gray)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] = clahe.apply(hsv[:,:,2])
        corrected_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        lab_frame = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2LAB)
        
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        canny_edges = cv2.Canny(blurred, 30, 150)
        combined = cv2.morphologyEx(canny_edges, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(combined.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Ambil kontur terbesar
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > 200:
                # Analisis kontur
                results = tester.analyze_contour(frame, largest_contour, lab_frame)
                evaluation = tester.evaluate_detection(results)
                
                # Gambar kontur dan analisis
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                frame = tester.draw_analysis_overlay(frame, results, evaluation)
        
        # Display ground truth
        if tester.ground_truth:
            cv2.putText(frame, f"Expected: {tester.ground_truth['color']} {tester.ground_truth['shape']}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Display performance summary
        summary = tester.get_performance_summary()
        if summary["overall"]["total_tests"] > 0:
            cv2.putText(frame, f"Color Acc: {summary['overall']['color_accuracy']:.2f}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Shape Acc: {summary['overall']['shape_accuracy']:.2f}", 
                       (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("Detection Performance Test", frame)
        cv2.imshow("Preprocessing", combined)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in ground_truth_options:
            color, shape = ground_truth_options[key]
            tester.set_ground_truth(color, shape)
        elif key == ord('s'):
            # Save performance report
            summary = tester.get_performance_summary()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"Performance report saved to {filename}")
        elif key == ord('r'):
            # Reset statistics
            tester.color_stats.clear()
            tester.shape_stats.clear()
            print("Statistics reset!")
    
    # Final report
    final_summary = tester.get_performance_summary()
    print("\n=== FINAL PERFORMANCE REPORT ===")
    print(f"Overall Color Accuracy: {final_summary['overall']['color_accuracy']:.2%}")
    print(f"Overall Shape Accuracy: {final_summary['overall']['shape_accuracy']:.2%}")
    print(f"Total Tests: {final_summary['overall']['total_tests']}")
    
    if final_summary['overall']['color_accuracy'] < final_summary['overall']['shape_accuracy']:
        print("📊 CONCLUSION: Color detection needs improvement!")
    elif final_summary['overall']['shape_accuracy'] < final_summary['overall']['color_accuracy']:
        print("📊 CONCLUSION: Shape detection needs improvement!")
    else:
        print("📊 CONCLUSION: Both detections perform similarly!")
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()