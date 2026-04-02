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
3. **Membangun Model Prediksi (Machine Learning):** Menggunakan model klasifikasi (Random Forest) untuk memprediksi probabilitas siswa akan *dropout* berdasarkan fitur-fitur yang disediakan dari 2 database universitas.
4. **Deploy Aplikasi Prediktif Interaktif:** Mengembangkan purwarupa web interaktif dengan Streamlit yang dapat diakses oleh konselor akademik untuk memasukkan data siswa guna melihat rekomendasi statusnya (*Dropout*, *Enrolled*, atau *Graduate*).

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

**Link Dashboard Looker Studio:**
*(Tautan menuju Google Looker Studio yang akan disiapkan oleh Anda, atau cek tangkapan layarnya pada `username_dicoding-dashboard.jpg` di folder ini)*

Catatan Tambahan: Fitur *fallback* dashboard interaktif juga telah ditanamkan ke dalam tab 1 purwarupa Web Streamlit di `app.py`.

## Menjalankan Sistem Machine Learning
Prototype sistem Machine Learning telah dibangun menggunakan framework web Streamlit. Sistem mereduksi ratusan fitur dan berfokus pada fitur krusial agar konselor dapat mendeteksi ancaman *dropout* dengan mudah. 

Aplikasi juga bisa diakses via Cloud secara publik pada tautan (silahkan tautkan link Streamlit Community Cloud di sini setelah Anda mendeploynya ke GitHub): 
**Link Streamlit Community Cloud:** https://jaya-institute-12.streamlit.app/

Cara menjalankan dari sistem lokal:
```bash
# 1. Buka terminal atau command prompt dan arahkan ke path folder proyek (submission)
cd submission

# 2. Jalankan framework streamlit pada file app.py
streamlit run app.py

# 3. Browser akan terbuka otomatis (biasanya http://localhost:8501)
```

## Conclusion
Dari proyek *Data Science* yang telah dikerjakan, kami dapat merangkum kesimpulan berikut ini:
1. **Faktor Finansial merupakan Determinan Utama:** Data secara jelas menunjukkan bahwa siswa dengan status *Tuition fees up to date* = 0 (menunggak SPP) dan bukan penerima beasiswa memiliki peluang untuk *dropout* dengan margin yang sangat luar biasa tinggi dibandingkan pemegang beasiswa dan siswa lunas.
2. **Performa Akademik di Tahun Pertama Sangat Kritis:** Tingkat *curricular units approved* serta *grades* (nilai) mahasiswa di pendaftaran semester pertama dan kedua begitu berbanding terbalik dan memiliki korelasi kuat terhadap putus sekolah. Mahasiswa yang banyak gagal di tahun pertama sering berakhir dengan *dropout*.
3. **Akurasi Model Prediksi:** Model **Random Forest Classifier** yang dilatih berhasil belajar secara tangguh dari himpunan fitur data tersebut (accuracy mendakati/melebihi 78% untuk skenario *multi-class*). Hal ini membantu mendeteksi risiko dan memberikan probabilitas secara tajam.

### Rekomendasi Action Items
Berdasarkan hasil analisis dan pemodelan, kami merekomendasikan hal berikut untuk Jaya Jaya Institut guna mencapai target (*zero warning risk dropout*):
- **Sistem *Early Warning* Akademik (Mentoring Wajib):** Mahasiswa yang mengalami kegagalan (*not approved*) pada mata kuliah semester 1, atau masuk dalam kategori prediksi Risiko Tinggi oleh aplikasi ini harus diharuskan mengambil sesi konseling wajib dan ditawarkan program mentoring rekan sejawat (Peer Tutoring) sebelum masuk semester 3.
- **Bantuan Edukasi / Relaksasi Finansial:** Karena tingginya hubungan gagal bayar SPP (*not up to date*) dengan putus sekolah, kampus perlu membuka pintu komunikasi proaktif menawarkan rencana cicilan, pekerjaan paruh waktu di dalam kampus, atau beasiswa darurat jika sistem mendeteksi mereka terlambat membayar dua bulan beturut-turut.
- **Adaptasi Mahasiswa "Tua" atau Pekerja:** Mahasiswa yang baru mengambil program saat usianya sudah lebih matang (lebih dari 22 tahun) atau malam hari memiliki pola rintangan beda. Pihak Manajemen disarankan menambah fleksibilitas kursus secara daring (hybrid) agar tak membebani waktu atau tenaga kerja mereka.
