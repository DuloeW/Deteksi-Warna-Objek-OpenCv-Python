# TESTING FRAMEWORK GUIDE
## Cara Menggunakan Tool Testing Performa Deteksi

### 🧪 File: test_detection_performance.py
Tool ini untuk menguji performa deteksi warna dan bentuk secara real-time.

**Cara Menggunakan:**
```bash
python test_detection_performance.py
```

**Fitur Utama:**
- Real-time testing dengan overlay
- Setting ground truth untuk objek yang sedang ditest
- Tracking akurasi warna dan bentuk secara terpisah
- Export hasil ke file JSON
- Statistik detail per warna dan bentuk

**Controls:**
- **R**: Set Red ground truth
- **G**: Set Green ground truth  
- **B**: Set Blue ground truth
- **O**: Set Orange ground truth
- **C**: Set Circle ground truth
- **S**: Set Square ground truth
- **T**: Set Triangle ground truth
- **E**: Set Rectangle ground truth
- **SPACE**: Mark detection as correct
- **X**: Mark detection as incorrect
- **Q**: Quit and save report

### 📊 File: analyze_detection.py
Tool ini untuk menganalisis hasil testing dan memberikan rekomendasi.

**Cara Menggunakan:**
```bash
python analyze_detection.py
```

**Menu Options:**
1. **Analyze Performance Report** - Analisis detail dari file JSON
2. **Create Performance Chart** - Buat chart teks performa
3. **Generate Improvement Report** - Buat laporan rekomendasi
4. **Exit**

### 📋 Workflow Penggunaan:

#### Step 1: Jalankan Testing
```bash
python test_detection_performance.py
```
- Siapkan objek yang akan ditest
- Set ground truth sesuai objek (tekan R untuk red, C untuk circle, dll)
- Lakukan testing dengan menekan SPACE (benar) atau X (salah)
- Tekan Q untuk selesai dan save report

#### Step 2: Analisis Hasil
```bash
python analyze_detection.py
```
- Pilih option 1 untuk analisis detail
- Masukkan nama file JSON yang baru dibuat
- Lihat hasil analisis lengkap

#### Step 3: Buat Chart dan Report
- Option 2: Buat chart visual performa
- Option 3: Generate improvement report dengan rekomendasi

### 📄 Contoh Output Files:
- `detection_performance_YYYYMMDD_HHMMSS.json` - Raw data hasil testing
- `performance_chart.txt` - Chart ASCII performa
- `improvement_report_YYYYMMDD_HHMMSS.txt` - Rekomendasi perbaikan

### 🎯 Tips Penggunaan:
1. **Testing Sistematis**: Test tiap warna/bentuk minimal 10 kali
2. **Variasi Kondisi**: Test di berbagai lighting dan background
3. **Konsistensi**: Gunakan jarak kamera yang sama
4. **Dokumentasi**: Catat kondisi lingkungan saat testing

### 🔧 Troubleshooting:
- **Webcam tidak terdeteksi**: Cek apakah kamera sudah terhubung
- **Error import**: Pastikan OpenCV dan numpy sudah terinstall
- **File tidak tersave**: Cek permission write di folder
- **Unicode error**: Gunakan text editor yang support UTF-8

### 📈 Interpretasi Hasil:
- **Accuracy > 80%**: Excellent
- **Accuracy 60-80%**: Good, butuh minor improvement
- **Accuracy < 60%**: Needs major improvement
- **Shape vs Color**: Yang lebih rendah perlu diprioritaskan