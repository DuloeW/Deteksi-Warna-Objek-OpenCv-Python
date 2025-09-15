"""
Advanced Detection Analysis
==========================
Analisis mendalam untuk mengetahui faktor-faktor yang mempengaruhi
akurasi deteksi warna dan bentuk.
"""

import json
from datetime import datetime
from collections import defaultdict


class DetectionAnalyzer:
    def __init__(self):
        self.test_results = []
        self.environmental_factors = []
        
    def analyze_performance_report(self, json_file):
        """Analisis file report JSON dari test sebelumnya"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            print("=== DETAILED ANALYSIS ===")
            
            # Color performance breakdown
            print("\n🎨 COLOR DETECTION ANALYSIS:")
            color_perf = data.get('color_performance', {})
            for color, metrics in color_perf.items():
                print(f"  {color.upper()}:")
                print(f"    Accuracy: {metrics['accuracy']:.2%}")
                if 'avg_confidence' in metrics:
                    print(f"    Avg Confidence: {metrics['avg_confidence']:.2f}")
                tests = metrics.get('total_tests', metrics.get('total_attempts', 'N/A'))
                print(f"    Tests: {tests}")
                if 'correct_detections' in metrics:
                    print(f"    Correct: {metrics['correct_detections']}")
                if 'common_mistakes' in metrics:
                    print(f"    Issues: {', '.join(metrics['common_mistakes'])}")
                
                # Recommendations
                if metrics['accuracy'] < 0.7:
                    print(f"    ⚠️  LOW ACCURACY - Consider adjusting {color} RGB values")
                if 'avg_confidence' in metrics and metrics['avg_confidence'] < 0.5:
                    print(f"    ⚠️  LOW CONFIDENCE - Check lighting conditions")
            
            # Shape performance breakdown
            print("\n📐 SHAPE DETECTION ANALYSIS:")
            shape_perf = data.get('shape_performance', {})
            for shape, metrics in shape_perf.items():
                print(f"  {shape.upper()}:")
                print(f"    Accuracy: {metrics['accuracy']:.2%}")
                if 'avg_confidence' in metrics:
                    print(f"    Avg Confidence: {metrics['avg_confidence']:.2f}")
                tests = metrics.get('total_tests', metrics.get('total_attempts', 'N/A'))
                print(f"    Tests: {tests}")
                if 'correct_detections' in metrics:
                    print(f"    Correct: {metrics['correct_detections']}")
                if 'common_mistakes' in metrics:
                    print(f"    Issues: {', '.join(metrics['common_mistakes'])}")
                
                # Recommendations
                if metrics['accuracy'] < 0.7:
                    print(f"    ⚠️  LOW ACCURACY - Check shape detection algorithm")
                if 'avg_confidence' in metrics and metrics['avg_confidence'] < 0.5:
                    print(f"    ⚠️  LOW CONFIDENCE - Improve edge detection")
            
            # Overall comparison
            overall = data.get('overall', {})
            color_acc = overall.get('color_accuracy', 0)
            shape_acc = overall.get('shape_accuracy', 0)
            
            print(f"\n📊 OVERALL COMPARISON:")
            print(f"Color Accuracy: {color_acc:.2%}")
            print(f"Shape Accuracy: {shape_acc:.2%}")
            
            if color_acc < shape_acc:
                diff = shape_acc - color_acc
                print(f"🔍 COLOR DETECTION is {diff:.2%} worse than shape detection")
                print("   Recommendations:")
                print("   - Improve lighting conditions")
                print("   - Expand color dictionary with more variations")  
                print("   - Use better color space (HSV instead of LAB)")
                print("   - Add color calibration")
            elif shape_acc < color_acc:
                diff = color_acc - shape_acc
                print(f"🔍 SHAPE DETECTION is {diff:.2%} worse than color detection")
                print("   Recommendations:")
                print("   - Improve edge detection parameters")
                print("   - Use better contour approximation")
                print("   - Add shape filtering based on area ratios")
                print("   - Consider using template matching")
            else:
                print("✅ Both detections perform equally well!")
                
        except FileNotFoundError:
            print(f"❌ File {json_file} not found!")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in {json_file}")
    
    def create_performance_chart(self, json_file, save_path="performance_chart.txt"):
        """Buat chart performa deteksi dalam format teks"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            chart_lines = []
            chart_lines.append("PERFORMANCE CHART")
            chart_lines.append("=" * 50)
            chart_lines.append("")
            
            # Color performance
            chart_lines.append("🎨 COLOR DETECTION ACCURACY:")
            color_perf = data.get('color_performance', {})
            for color, metrics in color_perf.items():
                accuracy = metrics['accuracy']
                bar_length = int(accuracy * 40)  # Scale to 40 chars
                bar = "█" * bar_length + "░" * (40 - bar_length)
                chart_lines.append(f"{color:>10}: {bar} {accuracy:.2%}")
            
            chart_lines.append("")
            
            # Shape performance
            chart_lines.append("📐 SHAPE DETECTION ACCURACY:")
            shape_perf = data.get('shape_performance', {})
            for shape, metrics in shape_perf.items():
                accuracy = metrics['accuracy']
                bar_length = int(accuracy * 40)  # Scale to 40 chars
                bar = "█" * bar_length + "░" * (40 - bar_length)
                chart_lines.append(f"{shape:>10}: {bar} {accuracy:.2%}")
            
            chart_lines.append("")
            chart_lines.append("Legend: █ = Correct, ░ = Incorrect")
            
            # Save chart
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(chart_lines))
            
            print('\n'.join(chart_lines))
            print(f"📈 Text chart saved to {save_path}")
            
        except Exception as e:
            print(f"❌ Error creating chart: {e}")
    
    def generate_improvement_report(self, json_file):
        """Generate detailed improvement recommendations"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            report_lines = []
            report_lines.append("DETECTION IMPROVEMENT REPORT")
            report_lines.append("=" * 50)
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            
            overall = data.get('overall', {})
            color_acc = overall.get('color_accuracy', 0)
            shape_acc = overall.get('shape_accuracy', 0)
            
            # Priority analysis
            if color_acc < 0.6 or shape_acc < 0.6:
                report_lines.append("🚨 CRITICAL ISSUES DETECTED:")
                if color_acc < 0.6:
                    report_lines.append(f"  - Color detection critically low: {color_acc:.2%}")
                if shape_acc < 0.6:
                    report_lines.append(f"  - Shape detection critically low: {shape_acc:.2%}")
                report_lines.append("")
            
            # Specific recommendations
            report_lines.append("🔧 IMPROVEMENT RECOMMENDATIONS:")
            report_lines.append("")
            
            if color_acc < shape_acc:
                report_lines.append("Priority: FIX COLOR DETECTION")
                report_lines.append("1. Update colorlabeler.py:")
                report_lines.append("   - Add more color variations to RGB dictionary")
                report_lines.append("   - Test different color spaces (HSV, LAB)")
                report_lines.append("   - Implement adaptive color thresholds")
                report_lines.append("")
                report_lines.append("2. Improve preprocessing:")
                report_lines.append("   - Better histogram equalization")
                report_lines.append("   - Shadow removal techniques")
                report_lines.append("   - Color constancy algorithms")
                report_lines.append("")
                
                # Specific color issues
                color_perf = data.get('color_performance', {})
                worst_color = min(color_perf.items(), key=lambda x: x[1]['accuracy'])
                report_lines.append(f"3. Focus on {worst_color[0]} color:")
                report_lines.append(f"   - Current accuracy: {worst_color[1]['accuracy']:.2%}")
                report_lines.append(f"   - Add more {worst_color[0]} variations")
                report_lines.append("")
                
            elif shape_acc < color_acc:
                report_lines.append("Priority: FIX SHAPE DETECTION")
                report_lines.append("1. Update shapedetector.py:")
                report_lines.append("   - Improve contour approximation parameters")
                report_lines.append("   - Add more robust shape classification")
                report_lines.append("   - Implement multiple detection methods")
                report_lines.append("")
                report_lines.append("2. Improve edge detection:")
                report_lines.append("   - Optimize Canny parameters")
                report_lines.append("   - Better morphological operations")
                report_lines.append("   - Multi-scale edge detection")
                report_lines.append("")
                
                # Specific shape issues
                shape_perf = data.get('shape_performance', {})
                worst_shape = min(shape_perf.items(), key=lambda x: x[1]['accuracy'])
                report_lines.append(f"3. Focus on {worst_shape[0]} detection:")
                report_lines.append(f"   - Current accuracy: {worst_shape[1]['accuracy']:.2%}")
                report_lines.append(f"   - Improve {worst_shape[0]} detection algorithm")
                report_lines.append("")
            
            # Environmental recommendations
            report_lines.append("🌍 ENVIRONMENTAL IMPROVEMENTS:")
            report_lines.append("- Ensure consistent lighting")
            report_lines.append("- Minimize shadows and reflections")
            report_lines.append("- Use contrasting background")
            report_lines.append("- Maintain consistent camera distance")
            report_lines.append("")
            
            # Code improvements
            report_lines.append("💻 CODE OPTIMIZATIONS:")
            report_lines.append("- Implement confidence-based filtering")
            report_lines.append("- Add temporal smoothing")
            report_lines.append("- Use ensemble methods")
            report_lines.append("- Add validation checks")
            
            # Save report
            report_filename = f"improvement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            print('\n'.join(report_lines))
            print(f"\n📄 Detailed report saved to {report_filename}")
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")


def main():
    analyzer = DetectionAnalyzer()
    
    print("=== DETECTION ANALYSIS TOOL ===")
    print("1. Analyze existing performance report")
    print("2. Create performance chart")
    print("3. Generate improvement report")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            filename = input("Enter JSON report filename: ").strip()
            analyzer.analyze_performance_report(filename)
            
        elif choice == '2':
            filename = input("Enter JSON report filename: ").strip()
            chart_name = input("Enter chart filename (default: performance_chart.png): ").strip()
            if not chart_name:
                chart_name = "performance_chart.png"
            analyzer.create_performance_chart(filename, chart_name)
            
        elif choice == '3':
            filename = input("Enter JSON report filename: ").strip()
            analyzer.generate_improvement_report(filename)
            
        elif choice == '4':
            break
            
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()