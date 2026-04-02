# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech (Jaya Jaya Institut)

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan terus mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, masalah utama yang saat ini sedang dihadapi adalah tingginya *dropout rate* (tingkat siswa putus sekolah/tidak menyelesaikan pendidikannya). Jumlah dropout yang tinggi ini menjadi kerugian besar untuk sebuah institusi. Oleh karena itu, Jaya Jaya Institut berupaya mengidentifikasi profil siswa yang rentan melakukan dropout agar bisa dibantu lebih cepat melalui intervensi akademis maupun finansial.

### Permasalahan Bisnis
1. Bagaimana cara mendeteksi secara dini siswa yang memiliki probabilitas tinggi akan melakukan *dropout* sebelum mereka benar-benar keluar dari institusi?
2. Faktor-faktor utama apa saja yang secara signifikan berdampak terhadap keputusan siswa untuk *dropout*? (Kinerja akademik, faktor sosial-ekonomi, atau riwayat edukasi)?
3. Langkah pencegahan (action items) apa yang bisa dijalankan manajemen kampus untuk secara efektif menekan tingkat *dropout*?

### Cakupan Proyek
1. **Eksplorasi dan Analisis Data (EDA):** Menganalisis karakteristik demografis, latar belakang sosial-ekonomi, dan performa akademik awal para siswa.
2. **Pembuatan Dashboard Analitik (Looker Studio):** Memvisualisasikan *key indicators* seperti persentase *dropout* dari total siswa, hubungan antara usia pendaftaran mahasiswa, status beasiswa, tunggakan SPP dengan status *dropout*.
3. **Membangun Model Prediksi (Machine Learning):** Menggunakan model klasifikasi (Random Forest) dengan pendekatan *binary classification* untuk memprediksi apakah siswa akan *Dropout* atau *Graduate*. Data siswa berstatus *Enrolled* tidak dilibatkan dalam training karena belum memiliki label akhir, sehingga model lebih valid dan relevan.
4. **Deploy Aplikasi Prediktif Interaktif:** Mengembangkan purwarupa web interaktif dengan Streamlit yang dapat diakses oleh konselor akademik untuk memasukkan data siswa guna melihat rekomendasi statusnya (*Dropout* atau *Graduate*).

### Persiapan

Sumber data: Data performa akademik siswa Jaya Jaya Institut 
(Disadur dari UCI Machine Learning Repository - *Predict students' dropout and academic success* by Realinho, et al. 2021) 
Tautan: [dataset github](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

Setup environment:
```bash
# 1. Pastikan python 3.9+ sudah terinstall
# 2. Opsional: buat virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Instal semua requirements (pandas, scikit-learn, streamlit, dll)
pip install -r requirements.txt

# 4. Folder 'model/' berisi model Random Forest yang diekspor ('rf_model.joblib') dan fitur. 
# Jika ingin melatih ulang, jalankan notebook.ipynb menggunakan Jupyter.
```

## Business Dashboard
Telah dibuat sebuah dashboard interaktif berbasis *Looker Studio* untuk mengecek metrik utama terkait performa siswa dan mengeksplorasi hubungan *dropout* dengan faktor-faktor akademis dan finansial.

**Link Dashboard Looker Studio:** https://lookerstudio.google.com/reporting/81e38b1f-e5b7-4bf2-8e1b-0835db5ce784

Catatan Tambahan: Fitur *fallback* dashboard interaktif juga telah ditanamkan ke dalam tab 1 purwarupa Web Streamlit di `app.py`.

## Menjalankan Sistem Machine Learning
Prototype sistem Machine Learning telah dibangun menggunakan framework web Streamlit. Sistem mereduksi ratusan fitur dan berfokus pada fitur krusial agar konselor dapat mendeteksi ancaman *dropout* dengan mudah. 

Aplikasi juga bisa diakses via Cloud secara publik pada tautan **Link Streamlit Community Cloud:** https://jaya-institute-12.streamlit.app/

Cara menjalankan dari sistem lokal:
```bash
# 1. Buka terminal atau command prompt dan arahkan ke path folder proyek (submission)
cd submission

# 2. Jalankan framework streamlit pada file app.py
streamlit run app.py

# 3. Browser akan terbuka otomatis (biasanya http://localhost:8501)
```

## Conclusion

Dari proyek *Data Science* yang telah dikerjakan, telah dirangkum dua jenis kesimpulan berikut:

### Kesimpulan 1: Faktor-Faktor dan Karakteristik Dropout (Berdasarkan EDA & Dashboard)

Berdasarkan hasil analisis eksplorasi data (EDA) pada notebook dan visualisasi dashboard Looker Studio, ditemukan faktor-faktor dan karakteristik utama yang berkaitan dengan terjadinya *dropout*:

1. **Faktor Finansial merupakan Determinan Paling Dominan:** Data secara jelas menunjukkan bahwa siswa yang menunggak SPP (`Tuition_fees_up_to_date = 0`) memiliki proporsi *dropout* yang sangat tinggi dibandingkan siswa yang lunas. Demikian pula, siswa yang **bukan** penerima beasiswa (`Scholarship_holder = 0`) dan siswa yang berstatus *debtor* (`Debtor = 1`) lebih rentan untuk keluar dari institusi.

2. **Performa Akademik di Tahun Pertama Sangat Kritis:** Jumlah mata kuliah yang disetujui (`Curricular_units_1st_sem_approved` dan `Curricular_units_2nd_sem_approved`) serta nilai rata-rata (`grade`) di semester 1 dan 2 memiliki perbedaan yang sangat signifikan antara kelompok Dropout dan Graduate. Mahasiswa yang banyak gagal atau mendapatkan nilai rendah di tahun pertama sangat rentan untuk tidak menyelesaikan pendidikan. Korelasi antara fitur-fitur akademik ini juga terkonfirmasi kuat melalui heatmap korelasi.

3. **Usia Pendaftaran Berpengaruh:** Analisis boxplot menunjukkan bahwa mahasiswa yang mendaftar pada usia lebih matang (di atas 25 tahun) memiliki pola dropout yang berbeda, kemungkinan disebabkan oleh faktor pekerjaan atau tanggung jawab keluarga yang bersaing dengan waktu studi.

### Kesimpulan 2: Performa Model Machine Learning

Model yang digunakan adalah **Random Forest Classifier** dengan pendekatan **binary classification** (Dropout vs Graduate). Data siswa berstatus `Enrolled` tidak dilibatkan dalam proses training karena belum memiliki label akhir, sehingga model lebih valid dan relevan.

**Metrik utama yang digunakan adalah Recall (kelas Dropout)**, bukan accuracy, karena dalam konteks *early warning system*:
- **False Negative** (gagal mendeteksi siswa yang benar-benar dropout) jauh lebih berbahaya daripada **False Positive** (salah mendeteksi siswa yang sebenarnya aman)
- Memaksimalkan Recall Dropout berarti model mampu menangkap sebanyak mungkin siswa berisiko untuk diberikan intervensi dini

Performa model pada data testing (20% dari total data Dropout + Graduate):

| Metrik | Dropout | Graduate | Overall |
|--------|---------|----------|---------|
| **Precision** | 88% | 90% | — |
| **Recall** ⭐ | **85%** | 92% | — |
| **F1-Score** | 86% | 91% | — |
| **Accuracy** | — | — | 89% |

- **Training Recall (Dropout)**: 86.72% | **Testing Recall (Dropout)**: 84.51% | Gap: 2.21%
- **Training Accuracy**: 90.46% | **Testing Accuracy**: 89.26% | Gap: 1.21%
- Gap yang kecil dan konsisten menunjukkan model tergolong **GOOD FIT** (tidak overfitting)

**Fitur-fitur paling berpengaruh** (berdasarkan Feature Importance):
1. `Curricular_units_2nd_sem_approved` (37.26%) — Jumlah MK disetujui Semester 2
2. `Curricular_units_1st_sem_approved` (21.52%) — Jumlah MK disetujui Semester 1
3. `Curricular_units_2nd_sem_grade` (12.95%) — Nilai Semester 2
4. `Curricular_units_1st_sem_grade` (8.85%) — Nilai Semester 1
5. `Tuition_fees_up_to_date` (8.03%) — Status Pembayaran SPP

Hasil ini mengkonfirmasi bahwa **performa akademik di tahun pertama** dan **status finansial** adalah prediktor terkuat terhadap risiko dropout.

### Rekomendasi Action Items

Berdasarkan hasil analisis dan pemodelan, direkomendasikan hal berikut untuk Jaya Jaya Institut guna mencapai target (*zero warning risk dropout*):
- **Sistem *Early Warning* Akademik (Mentoring Wajib):** Mahasiswa yang mengalami kegagalan (*not approved*) pada mata kuliah semester 1, atau masuk dalam kategori prediksi Risiko Tinggi oleh aplikasi ini harus diharuskan mengambil sesi konseling wajib dan ditawarkan program mentoring rekan sejawat (Peer Tutoring) sebelum masuk semester 3.
- **Bantuan Edukasi / Relaksasi Finansial:** Karena tingginya hubungan gagal bayar SPP (*not up to date*) dengan putus sekolah, kampus perlu membuka pintu komunikasi proaktif menawarkan rencana cicilan, pekerjaan paruh waktu di dalam kampus, atau beasiswa darurat jika sistem mendeteksi mereka terlambat membayar dua bulan berturut-turut.
- **Adaptasi Mahasiswa "Tua" atau Pekerja:** Mahasiswa yang baru mengambil program saat usianya sudah lebih matang (lebih dari 22 tahun) atau malam hari memiliki pola rintangan beda. Pihak Manajemen disarankan menambah fleksibilitas kursus secara daring (hybrid) agar tak membebani waktu atau tenaga kerja mereka.
