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

ikut revisi Data Preparation dalam format .md:

markdown
Copy
Edit
# 📍 Data Preparation

## ✅ Tahapan Data Preparation

### Menggabungkan Dataset Movies dan Ratings
- Dataset `movies` digabungkan dengan dataset `ratings` berdasarkan kolom `movieId`.
- Hasil penggabungan membentuk dataset `rated_movies` dengan kolom `movieId`, `title`, `genres`, `userId`, `rating`, dan `timestamp`.

### Memeriksa dan Mengatasi Missing Value
- Dilakukan pengecekan missing value dengan `.isnull().sum()` pada dataset `rated_movies`.
- Ditemukan 3.376 missing value pada kolom `userId`, `rating`, dan `timestamp`.
- Missing value dihapus menggunakan `rated_movies.dropna()`.
- Setelah penghapusan, dicek kembali untuk memastikan tidak ada missing value yang tersisa.

### Mengubah Tipe Data Kolom `userId`
- Kolom `userId` diubah dari `float` menjadi `int` dengan `rated_movies['userId'] = rated_movies['userId'].astype('int')`.
- Langkah ini penting agar kolom `userId` sesuai dengan input model Collaborative Filtering.

### Menghapus Data dengan Genre Tidak Tersedia
- Data film dengan genre `(no genres listed)` diidentifikasi dan dihapus.
- Proses dilakukan menggunakan `rated_movies[rated_movies['genres'] != '(no genres listed)']`.

### Sampling Data (Penghapusan 99.9% Baris Data Secara Acak)
- Untuk mempercepat pemrosesan, dilakukan penghapusan 99.9% baris data secara acak dengan `sample(frac=0.999, random_state=42)`.
- Langkah ini ditujukan untuk mengurangi ukuran dataset agar lebih ringan pada tahap Content-Based Filtering.

### Menghapus Data Duplikat
- Data duplikat berdasarkan `movieId` dihapus agar tidak terjadi duplikasi informasi film.

### Membuat DataFrame `movie_new` untuk Content-Based Filtering dan membuat pasangan key-value pada movie_id, movie_name dan movie_genre
- Data kolom `movieId`, `title`, dan `genres` diubah menjadi list:
  - `movie_id = preparation_df['movieId'].tolist()`
  - `movie_title = preparation_df['title'].tolist()`
  - `movie_genre = preparation_df['genres'].tolist()`
- Data ini digabungkan menjadi DataFrame `movie_new` dengan kolom `id`, `title`, dan `genre` untuk tahap Content-Based Filtering.
- - Membuat dictionary untuk data `'movie_id'`, `'movie_title',` `'movie_genre'` dengan `movie_new = pd.DataFrame({
    'id': movie_id,
    'title': movie_title,
    'genre': movie_genre
})`

## ✅ Tahapan Data Preparation Content-Based Filtering

### Konversi Kolom `genres` Menjadi List (Pra-One-Hot Encoding)
- Pada `movie_new`, kolom `genre` diubah dari format string menjadi list genre menggunakan `apply(lambda x: x.split('|'))`.

### One-Hot Encoding pada Kolom `genres`
- Menggunakan `MultiLabelBinarizer` dari `sklearn.preprocessing`, kolom `genres` diubah menjadi vektor biner.
- Hasil one-hot encoding digabungkan dengan `movie_new` untuk menghasilkan DataFrame `df_final`.

### Perhitungan Cosine Similarity untuk Content-Based Filtering
- Cosine similarity dihitung menggunakan `sklearn.metrics.pairwise.cosine_similarity` pada hasil one-hot encoding genre.
- Hasil cosine similarity disimpan dalam DataFrame `cosine_sim_df` dengan baris dan kolom berupa `title` film.

### Pembuatan Fungsi Rekomendasi
- Fungsi `movie_recommendations()` dibuat untuk memberikan rekomendasi film berdasarkan kemiripan genre.
- Fungsi ini menggunakan `cosine_sim_df` sebagai input untuk mencari film dengan kemiripan tertinggi.

## ✅ Tahapan Data Preparation Collaborative Filtering

### Encoding Kolom `userId` dan `movieId` menjadi Integer
- Kolom `userId` dan `movieId` diubah menjadi integer agar dapat digunakan sebagai input pada model Collaborative Filtering.
- Tahapan:
  - **Mendapatkan unique `userId` dan `movieId`**:
    ```python
    user_ids = df['userId'].unique().tolist()
    movie_ids = df['movieId'].unique().tolist()
    ```
  - **Melakukan encoding `userId` dan `movieId`**:
    ```python
    user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
    movie_to_movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    ```
  - **Melakukan mapping encoding ke DataFrame**:
    ```python
    df['user'] = df['userId'].map(user_to_user_encoded)
    df['movie'] = df['movieId'].map(movie_to_movie_encoded)
    ```

### Membuat Mapping Reverse (Integer ke `userId` / `movieId`)
- Untuk keperluan interpretasi hasil model:
  ```python
  user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
  movie_encoded_to_movie = {i: x for i, x in enumerate(movie_ids)}

### Normalisasi Kolom `rating`
- Kolom `rating` dinormalisasi dengan rumus `(rating - min_rating) / (max_rating - min_rating)` agar berada dalam skala 0–1.
- Langkah tersebut memastikan model bekerja pada skala rating yang konsisten:
- `min_rating = min(df['rating'])
max_rating = max(df['rating'])
df['rating'] = df['rating'].astype(np.float32)
y = df['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values`

### Membuat Input Features (x) untuk Model
- Variabel x berisi pasangan (user, movie): `x = df[['user', 'movie']].values`

### Train-Test Split
- Dataset diacak terlebih dahulu menggunakan: `df = df.sample(frac=1, random_state=42)`
- Data kemudian dibagi menjadi 80% untuk training dan 20% untuk validation: `train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)`
- Pembagian ini memastikan evaluasi dilakukan pada data yang belum pernah dilihat oleh model.

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
  - **RMSE (train)**: 0.1804
  - **RMSE (validation)**: 0.2562

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
