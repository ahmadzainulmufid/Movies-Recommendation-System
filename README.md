# Laporan Proyek

## Project Overview

### Latar Belakang

Industri hiburan, khususnya movie dan serial, mengalami pertumbuhan pesat dalam era digital saat ini, dengan ribuan judul yang tersedia di berbagai platform streaming seperti Netflix, Hulu, dan Disney+. Pengguna sering mengalami kesulitan dalam memilih tampilan yang sesuai dengan preferensi mereka karena pilihan yang diblokir. Hal ini menyebabkan kebutuhan akan sistem rekomendasi yang dapat mengidentifikasi dan menampilkan konten yang relevan untuk setiap pengguna.

Berdasarkan pola perilaku atau preferensi pengguna sebelumnya, sistem rekomendasi memprediksi item yang kemungkinan besar disukai oleh pengguna. Sistem ini dapat menggunakan berbagai jenis data dalam konteks movie, seperti genre movie dan histori rating pengguna. Collaborative Filtering dan Content-Based Filtering adalah dua pendekatan utama yang paling umum digunakan ([Ricci et al., 2011](https://doi.org/10.1007/978-0-387-85820-3_1)).

Mengembangkan sistem rekomendasi movie ini akan membantu pengguna menemukan konten yang lebih baik dan meningkatkan keterlibatan dan retensi pengguna di platform penyedia layanan. Proyek ini akan membangun sistem rekomendasi movie menggunakan Content-Based Filtering dan Collaborative Filtering yang diharapkan dapat memberikan hasil yang lebih sesuai dan sesuai dengan preferensi pengguna.

---

Mengapa proyek ini penting untuk diselesaikan?

1. Meningkatkan Pengalaman Pengguna: Selesainya proyek ini sangat penting karena akan membantu pengguna menemukan movie yang sesuai dengan preferensi mereka dengan lebih mudah. Tanpa sistem rekomendasi, pengguna mungkin bingung dan tidak puas karena harus mencari ribuan pilihan secara manual.
2. Menyelesaikan Masalah Overload Informasi: Di era digital, pengguna sering mengalami overload informasi karena banyaknya pilihan konten. Rekomendasi sistem dapat berfungsi sebagai filter cerdas dan membantu menyaring konten yang relevan, sehingga mengurangi waktu pencarian dan membuat keputusan yang lebih baik.
3. Memiliki Dampak Ekonomi bagi Platform Layanan: Dalam industri, sistem rekomendasi telah terbukti dapat meningkatkan keterlibatan, retensi pengguna, dan konversi. Platform seperti Netflix dan Amazon bergantung pada sistem rekomendasi untuk meningkatkan konsumsi konten, yang berdampak pada keuntungan bisnis mereka.

Referensi Jurnal :

- [Introduction to Recommender Systems Handbook](https://link.springer.com/chapter/10.1007/978-0-387-85820-3_1)
- [Recommender systems survey](https://www.sciencedirect.com/science/article/abs/pii/S0950705113001044?via%3Dihub)

## Business Understanding

### Problem Statements

- Pengguna kesulitan menemukan film yang sesuai dengan preferensi mereka karena banyaknya pilihan.
- Content-Based Filtering cenderung menghasilkan rekomendasi yang monoton (mirip dengan preferensi sebelumnya).
- Collaborative Filtering menghadapi masalah cold-start (film/pengguna baru) dan data sparsity (data rating jarang).

### Goals

- Menghasilkan sistem rekomendasi film yang dapat membantu pengguna menemukan tontonan yang sesuai dengan preferensi mereka, berdasarkan riwayat interaksi dan konten film.
- Memperluas cakupan rekomendasi agar tidak hanya terfokus pada genre yang sama (mengatasi keterbatasan Content-Based Filtering).
- Meningkatkan kemampuan sistem dalam memberikan rekomendasi awal pada pengguna atau film baru (mengurangi dampak cold-start dan sparsity).

### Solution statements

- Implementasi Content-Based Filtering menggunakan Cosine Similarity pada data genre.
- Implementasi Collaborative Filtering menggunakan model deep learning (RecommenderNet) untuk memanfaatkan data rating pengguna.

## 📍 Data Understanding

### 📊 Dataset

1. **Movies Dataset**

   - **Jumlah Data**: 62.423 baris, 3 kolom
   - **Fitur**:
     - `movieId`: ID unik film
     - `title`: Judul film
     - `genres`: Genre film (dipisah dengan |)
   - **Kondisi Data**:
     - Missing value: Tidak ada
     - Duplikasi: Tidak ada
     - Outlier: Tidak relevan
   - **Sumber**: [Kaggle - Movie Recommendation System](https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system)

2. **Ratings Dataset**
   - **Jumlah Data**: 25.000.095 baris, 4 kolom
   - **Fitur**:
     - `userId`: ID unik pengguna
     - `movieId`: ID unik film
     - `rating`: Nilai rating (0.5 - 5.0)
     - `timestamp`: Waktu pemberian rating
   - **Kondisi Data**:
     - Missing value: Tidak ada
     - Duplikasi: Tidak ada
     - Outlier: Tidak ada

## 📍 Data Preparation

### ✅ Tahapan Data Preparation

#### 1⃣ Memeriksa dan Mengatasi Missing Value

- Mengecek adanya missing value pada dataset `rated_movies` menggunakan `.isnull().sum()`.
- Tidak ditemukan missing value, sehingga tidak ada data yang dihapus karena missing value.

#### 2⃣ Menghapus Data dengan Genre Tidak Tersedia

- Memeriksa data film yang memiliki genre `(no genres listed)`.
- Menghapus baris data dengan genre `(no genres listed)` dari dataset `rated_movies`.

#### 3⃣ Sampling Data (Penghapusan 99.9% Baris Data Secara Acak)

- Melakukan proses sampling besar-besaran dengan menghapus 99.9% baris data secara acak menggunakan `sample(frac=0.999)`.
- Langkah ini dilakukan untuk mengurangi ukuran dataset agar lebih ringan untuk diproses, terutama pada tahap Content-Based Filtering.

#### 4⃣ Menghapus Data Duplikat

- Menghapus data duplikat berdasarkan `movieId` untuk memastikan tidak ada film yang tercatat lebih dari sekali.

#### 5⃣ Menggabungkan Dataset Movies dan Ratings

- Menggabungkan dataset `movies` dengan `ratings` berdasarkan `movieId` untuk membentuk dataset `rated_movies` yang berisi `movieId`, `title`, `genres`, `userId`, dan `rating`.

#### 6⃣ Mengonversi Kolom `genres` menjadi List

- Mengubah kolom `genres` dari format string menjadi list genre untuk setiap film.

#### 7⃣ Membuat DataFrame `movie_new` untuk Content-Based Filtering

- Membuat DataFrame `movie_new` yang berisi `movieId`, `title`, dan `genre` (hasil konversi list).
- Data ini digunakan untuk proses Content-Based Filtering.

#### 8⃣ One-Hot Encoding pada Kolom `genres`

- Melakukan proses one-hot encoding pada kolom `genres` untuk menghasilkan representasi vektor biner dari genre film.

#### 9⃣ Encoding pada `userId` dan `movieId` untuk Collaborative Filtering

- Melakukan encoding pada kolom `userId` dan `movieId` menjadi integer agar dapat digunakan sebagai input model Collaborative Filtering (RecommenderNet).

#### 🔡 Train-Test Split

- Membagi data `ratings` menjadi 80% untuk training dan 20% untuk testing, memastikan evaluasi model dilakukan pada data yang belum pernah dilihat.

## 📍 Modeling

### 1️⃣ Content-Based Filtering

- **Fitur**: Genre
- **Algoritma**: Cosine Similarity
- **Output**: Rekomendasi film yang mirip dengan preferensi pengguna berdasarkan genre.

#### 📊 Contoh Top-5 Rekomendasi untuk Film "Lights Out (2016)"

| Rekomendasi Film                    | Genre  |
|------------------------------------|--------|
| Pet Sematary (1989)                 | Horror |
| Mangler, The (1995)                 | Horror |
| Amityville 3-D (1983)               | Horror |
| Amityville II: The Possession (1982)| Horror |
| Jeepers Creepers (2001)             | Horror |

### 2️⃣ Collaborative Filtering

- **Model**: RecommenderNet (Deep Learning)
- **Arsitektur**:
  - Embedding layer untuk `userId` dan `movieId`
  - Dot product untuk prediksi rating
- **Optimizer**: Adam
- **Loss**: RMSE
- **Epochs**: 20 epoch

#### 📊 Contoh Top-5 Rekomendasi untuk User 1

| movieId | Predicted Rating |
|---------|------------------|
| 750     | 0.86             |
| 1617    | 0.84             |
| 48516   | 0.84             |
| 318     | 0.83             |
| 912     | 0.83             |

#### 🔍 Visualisasi Training

Grafik berikut menunjukkan hasil training model RecommenderNet selama 20 epoch. Terlihat bahwa nilai RMSE pada data training dan validation terus menurun seiring bertambahnya epoch, dengan stabilitas model yang semakin baik pada epoch ke-15 ke atas.

![image](https://github.com/user-attachments/assets/b81fcbb9-710c-4635-b499-a8f43656feaf)

Dengan ini, bagian Modeling telah mencakup penjelasan metode, arsitektur, hasil rekomendasi (Top-N recommendation), dan metrik performa model. 🚀

## 📍 Evaluation

### 1️⃣ Collaborative Filtering

- **Metrik**: Root Mean Squared Error (RMSE)
- **Nilai RMSE Akhir**:
  - **RMSE (train)**: 0.2060
  - **RMSE (validation)**: 0.2592

### 2️⃣ Content-Based Filtering

- **Metrik**: Precision@K (K=4)
- **Hasil Evaluasi User 7002**:
  - Dari 4 rekomendasi teratas, tidak ada satupun yang relevan (tidak ada rating ≥4.0), sehingga Precision@4 = 0.0.

- **Perhitungan Precision@4**:
  - **Langkah-langkah**:
    1. Mengambil histori rating user 7002: hanya ada 1 film dengan rating 2.0.
    2. Membuat rekomendasi Top-4 berbasis Content-Based Filtering menggunakan film tersebut sebagai acuan.
    3. Tidak ada rekomendasi yang cocok dengan histori rating user (tidak ada rating ≥4.0).
    4. Sehingga, Precision@4 = 0/4 = 0.0.

### ✨ Interpretasi

- **Collaborative Filtering**: RMSE yang rendah menunjukkan prediksi rating mendekati nilai aktual.
- **Content-Based Filtering**: Precision@4 = 0.0 menunjukkan rekomendasi yang diberikan tidak sesuai dengan minat user 7002, yang mungkin disebabkan oleh jumlah histori rating user yang sangat sedikit (hanya 1 film, dengan rating rendah).
