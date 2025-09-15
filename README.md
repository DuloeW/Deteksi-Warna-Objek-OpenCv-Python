# Deteksi Warna dan Bentuk Objek Real-time dengan OpenCV

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Deskripsi
Sistem deteksi objek real-time yang dapat mengenali **warna** dan **bentuk** objek menggunakan webcam. Dilengkapi dengan framework testing untuk evaluasi performa dan tools analisis untuk optimasi sistem.

## ✨ Fitur Utama

### 🎯 Deteksi Real-time
- **6 Mode Deteksi**: Color Only, Shape Only, Both, Color Priority, Shape Priority, Adaptive
- **Multi-color Support**: Red, Blue, Orange, Green dengan variasi RGB
- **Multi-shape Support**: Circle, Rectangle, Square, Triangle
- **Center Detection**: Indikator visual apakah objek berada di tengah frame
- **Performance Monitoring**: FPS tracking dan resource monitoring

### 🧪 Testing Framework
- **Real-time Performance Testing**: Evaluasi akurasi deteksi secara langsung
- **Ground Truth Setting**: Set objek target untuk testing akurasi
- **Statistical Analysis**: Breakdown performa per warna dan bentuk
- **JSON Export**: Simpan hasil testing untuk analisis lebih lanjut

### 📊 Analysis Tools
- **Performance Analysis**: Analisis mendalam hasil testing
- **ASCII Charts**: Visualisasi performa tanpa dependencies tambahan
- **Improvement Reports**: Rekomendasi spesifik untuk optimasi
- **Comparison Tools**: Bandingkan hasil testing berbeda

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/DuloeW/Deteksi-Warna-Objek-OpenCv-Python.git
cd Deteksi-Warna-Objek-OpenCv-Python
```

### 2. Setup Environment
```bash
# Buat virtual environment (opsional)
python -m venv .venv
.venv\Scripts\Activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install opencv-python
pip install imutils
pip install numpy
```

### 3. Jalankan Aplikasi
```bash
# Deteksi real-time
python detect_color.py

# Testing framework
python test_detection_performance.py

# Analysis tools
python analyze_detection.py
```

## 🎮 Controls & Shortcuts

### Deteksi Real-time (`detect_color.py`)
| Key | Function |
|-----|----------|
| `1` | Color Only Mode |
| `2` | Shape Only Mode |
| `3` | Both Color & Shape |
| `4` | Color Priority Mode |
| `5` | Shape Priority Mode |
| `6` | Adaptive Mode |
| `Q` | Quit |
| `R` | Reset tracking |
| `H` | Toggle help overlay |

### Testing Framework (`test_detection_performance.py`)
| Key | Function |
|-----|----------|
| `R` | Set Red ground truth |
| `G` | Set Green ground truth |
| `B` | Set Blue ground truth |
| `O` | Set Orange ground truth |
| `C` | Set Circle ground truth |
| `S` | Set Square ground truth |
| `T` | Set Triangle ground truth |
| `E` | Set Rectangle ground truth |
| `SPACE` | Mark detection correct |
| `X` | Mark detection incorrect |
| `Q` | Quit and save report |

## 📁 Struktur Project

```
├── detect_color.py              # Main detection application
├── test_detection_performance.py # Testing framework
├── analyze_detection.py         # Analysis tools
├── pyimagesearch/
│   ├── __init__.py
│   ├── colorlabeler.py         # Color detection logic
│   └── shapedetector.py        # Shape detection logic
├── example_shapes.jpg          # Sample test image
├── test*.jpg/png/webp          # Test images
├── TESTING_GUIDE.md           # Detailed usage guide
└── README.md                  # This file
```

## 🔧 Konfigurasi

### Warna yang Didukung
- **Red**: Multiple RGB variations for different lighting
- **Blue**: Blue variants including dark and light blue
- **Orange**: Orange and orange-red combinations
- **Green**: Basic green detection

### Bentuk yang Didukung
- **Circle**: Using HoughCircles and contour approximation
- **Rectangle**: Rectangular shapes with aspect ratio validation
- **Square**: Square detection with side ratio checks
- **Triangle**: Triangular shapes with 3-vertex approximation

### Mode Deteksi
1. **Color Only**: Hanya deteksi warna
2. **Shape Only**: Hanya deteksi bentuk
3. **Both**: Deteksi warna dan bentuk bersamaan
4. **Color Priority**: Prioritas warna, bentuk sebagai sekunder
5. **Shape Priority**: Prioritas bentuk, warna sebagai sekunder
6. **Adaptive**: Mode adaptif berdasarkan kondisi

## 📊 Workflow Testing

### 1. Persiapan Testing
```bash
python test_detection_performance.py
```
- Siapkan objek dengan warna dan bentuk yang jelas
- Pastikan pencahayaan yang cukup
- Gunakan background kontras

### 2. Eksekusi Testing
- Set ground truth sesuai objek (tekan R untuk red, C untuk circle)
- Lakukan deteksi dan mark sebagai benar (SPACE) atau salah (X)
- Test minimal 10 sampel per kategori untuk akurasi statistik

### 3. Analisis Hasil
```bash
python analyze_detection.py
```
- Pilih option 1: Analisis performance report
- Pilih option 2: Generate ASCII chart
- Pilih option 3: Generate improvement report

## 📈 Interpretasi Hasil

### Tingkat Akurasi
- **> 85%**: Excellent performance
- **70-85%**: Good performance, minor improvements needed
- **50-70%**: Moderate performance, significant improvements needed
- **< 50%**: Poor performance, major overhaul required

### Rekomendasi Berdasarkan Hasil
- **Color Accuracy < Shape Accuracy**: Fokus improve `colorlabeler.py`
- **Shape Accuracy < Color Accuracy**: Fokus improve `shapedetector.py`
- **Low Overall Accuracy**: Check environmental factors

## 🛠️ Optimasi Performance

### Hardware Requirements
- **Webcam**: Minimal 720p untuk hasil optimal
- **CPU**: Intel i3 atau AMD Ryzen 3 ke atas
- **RAM**: Minimal 4GB
- **Python**: 3.8+ recommended

### Tips Optimasi
1. **Lighting**: Gunakan pencahayaan yang konsisten
2. **Background**: Gunakan background kontras (putih/hitam)
3. **Distance**: Jaga jarak kamera 20-40cm dari objek
4. **Stability**: Gunakan tripod untuk stabilitas kamera

## 🔍 Troubleshooting

### Common Issues
1. **Webcam tidak terdeteksi**
   ```python
   # Check available cameras
   import cv2
   for i in range(3):
       cap = cv2.VideoCapture(i)
       if cap.isOpened():
           print(f"Camera {i} available")
       cap.release()
   ```

2. **Low FPS performance**
   - Reduce frame size in `detect_color.py`
   - Enable frame skipping (sudah diimplementasi)
   - Close other applications using camera

3. **Inaccurate detection**
   - Check lighting conditions
   - Calibrate color ranges in `colorlabeler.py`
   - Adjust shape detection parameters in `shapedetector.py`

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Authors

- **DuloeW** - *Initial work* - [DuloeW](https://github.com/DuloeW)

## 📞 Support

Jika mengalami masalah atau memiliki pertanyaan:
1. Check [TESTING_GUIDE.md](TESTING_GUIDE.md) untuk panduan detail
2. Buka Issue di repository ini
3. Review troubleshooting section di atas

## 🙏 Acknowledgments

- OpenCV community untuk computer vision library
- Imutils untuk utility functions
- NumPy untuk mathematical operations


