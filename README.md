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

- Pengguna kesulitan menemukan movie yang sesuai dengan preferensi mereka: Pengguna sering mengalami kesulitan memilih movie yang sesuai karena semakin banyak movie yang tersedia di berbagai platform digital. Proses pencarian movie dapat menjadi tidak efektif dan menurunkan pengalaman pengguna jika tidak ada sistem rekomendasi yang tepat.
- Content-Based Filtering menghasilkan rekomendasi yang monoton: Pendekatan berbasis konten hanya menyarankan item yang serupa dengan apa yang disukai pengguna sebelumnya, sehingga rekomendasi movie menjadi terlalu seragam dan tidak eksplorasi, sehingga pengguna tidak dikenalkan dengan movie yang berbeda tetapi mungkin disukai.
- Collaborative Filtering menghadapi masalah cold-start dan data sparsity: Data interaksi pengguna, seperti penilaian, diperlukan untuk filter kolaboratif. Sistem tidak memiliki cukup data untuk membuat rekomendasi yang akurat jika movie atau pengguna masih baru. Ini disebut masalah start dingin. Selain itu, data sparsity—atau jarang interaksi—disebabkan oleh fakta bahwa sebagian besar pengguna hanya memberikan rating yang sedikit. Akibatnya, sulit bagi sistem untuk menemukan pola yang tepat.

### Goals

- Membantu pengguna menemukan movie yang sesuai dengan preferensi mereka: Sistem ini bertujuan untuk memberikan rekomendasi movie yang personal dan relevan sehingga pengguna tidak perlu mencari ribuan judul secara manual. Ini akan meningkatkan kenyamanan dan efektivitas dalam memilih tontonan.
- Menghindari rekomendasi yang monoton dari sistem berbasis konten: Diharapkan sistem akan dapat merekomendasikan movie yang sebanding dengan preferensi pengguna sebelumnya dan juga dapat memperluas daftar rekomendasi ke movie yang berbeda dan relevan, sehingga meningkatkan pengalaman pengguna.
- Collaborative Filtering menghadapi masalah cold-start dan data sparsity: Data interaksi pengguna, seperti penilaian, diperlukan untuk collaborative filtering. Sistem tidak memiliki cukup data untuk membuat rekomendasi yang akurat jika movie atau pengguna masih baru.

### Solution statements

- Implementasi Content-Based Filtering: Content-Based Filtering akan menggunakan informasi konten movie, khususnya genre, untuk memberikan rekomendasi berdasarkan kesamaan konten.
- Implementasi Collaborative Filtering: Collaborative Filtering akan menggunakan interaksi antara pengguna dan movie seperti rating (tanpa melihat isi movie).

## Data Understanding

### Informasi Dataset

- Terdiri dari 2 variabel: movies dan ratings
- Jumlah data
  - movies: 62.423 baris dan 3 kolom (movieId, title, genres)
  - ratings: 25.000.095 baris dan 4 kolom (userId, movieId, rating, timestamp)
- Sumber data: [Movie Recommendation System](https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system)

Variabel-variabel pada Movie Recommendation System dataset adalah sebagai berikut:

- movieId : merupakan identitas unik movie.
- title: merupakan judul movie.
- genres: merupakan genre-genre yang dimiliki suatu movie.
- userId : merupakan identitas unik pengguna yang memberikan rating terhadap movie.
- rating: merupakan penilaian yang diberikan pengguna terhadap movie.
- timestamp: merupakan rentang waktu penilaian diberikan oleh pengguna.

Pada proyek ini, beberapa tahapan Exploratory Data Analysis yang dilakukan adalah:

- Menganalisis univariate variable
- Menangani missing value

## Data Preparation

Adapun beberapa teknik data preparation yang dilakukan pada proyek ini adalah sebagai berikut.

  1. Mengatasi Missing value. (Content-Based Filtering)
  2. Membuat Data duplikat. (Content-Based Filtering)
  3. Melakukan one-hot encoding pada fitur genres. (Content-Based Filtering)
  4. Menghitung derajat kesamaan antar movie dengan cosine similarity. (Content-Based Filtering)
  5. Melakukan encoding pada fitur userId dan movieId. (Collaborative Filtering)
  6. Melakukan train-test split. (Collaborative Filtering)

Penjelasan data preparation yang dilakukan:

  1. Mengatasi Missing value: Baris data yang memiliki fitur atau kolom yang kosong akan dihilangkan.
  2. Membuang data duplikat: Berdasarkan fitur movieId, jika ada data yang memiliki id yang sama akan dihilangkan.
  3. Melakukan one-hot encoding: Fitur genre diubah menjadi representasi vektor biner.
  4. Menghitung derajat kesamaan: Mengukur seberapa mirip dua vektor dengan menghitung cosinus dari sudut di antara keduanya.
  5. Melakukan encoding pada userId dan movieId: Mengubah nilai kategorikal (id unik) menjadi format numerik.
  6. Melakukan train-test split: Memisahkan data training dan data test dengan rasio 80:20 agar model dapat belajar dari sebagian besar data training dan diuji menggunakan data test yang   belum pernah dilihat model sebelumnya.

Alasan mengapa diperlukan tahapan data preparation tersebut:

  1. Mengatasi missing value: Data yang memiliki missing value dapat menurunkan performa model yang sedang dilatih karena mengakibatkan bias. Sehingga data yang memiliki missing value harus diatasi.
  2. Membuang data duplikat: Data duplikat dapat membuat model memberikan bobot yang berlebihan terhadap suatu item. Hal ini mengakibatkan bias dalam sistem rekomendasi jika tidak diatasi.
  3. Melakukan one-hot encoding: Algoritma seperti Content-Based Filtering memerlukan representasi fitur dalam bentuk vektor numerik agar bisa menghitung kemiripan antar movie.
  4. Menghitung derajat kesamaan: Menghitung derajat kesamaan diperlukan agar sistem dapat menemukan movie yang paling mirip dengan yang disukai pengguna. Dalam Content-Based Filtering, sistem mencocokkan fitur seperti genre, lalu merekomendasikan movie lain yang memiliki kemiripan tinggi.
  5. Melakukan encoding pada userId dan movieId: Memetakan ID ke posisi dalam matriks rating, yang digunakan oleh algoritma serta memastikan konsistensi dan efisiensi dalam pemrosesan data.
  6. Melakukan train-test split: Memastikan bahwa model diuji dengan data yang tidak digunakan selama training sehingga dapat memberikan gambaran nyata tentang kinerja model saat digunakan menggunakan data baru.

## Modeling

Tahapan dan parameter yang digunakan dalam proses pemodelan adalah sebagai berikut.

1. Inisialisasi model: Model yang digunakan dalam proyek ini adalah RecommenderNet dari Keras, yang merupakan model rekomendasi berbasis neural network yang dirancang untuk mempelajari preferensi pengguna terhadap item (seperti movie) dengan menggunakan embedding layer untuk merepresentasikan userId dan movieId

2. Pelatihan model: Setelah model selesai diinisialisasi, dilakukan pelatihan menggunakan data training. Proses ini melibatkan pemberian input (x_train) dan target (y_train) ke dalam model.

3. Evaluasi awal model: Sebelum melakukan tuning, model dievaluasi menggunakan metrik root mean squared error (RMSE) untuk mengukur seberapa jauh nilai prediksi dengan nilai sebenarnya.

---

Solusi rekomendasi dan algoritma yang digunakan sebagai berikut.

- Content-Based Filtering menggunakan algoritma Cosine Similarity
    Metode ini menampilkan setiap film sebagai vektor fitur yang didasarkan pada genrenya. Ketika teknik One-Hot Encoding digunakan, genre diubah menjadi representasi numerik. Selanjutnya, metode Cosine Similarity digunakan untuk menghitung tingkat kemiripan antara dua movie. Ini menghasilkan nilai antara 0 dan 1, dan semakin tinggi nilainya, semakin mirip kontennya. Berikut adalah contoh outputnya:

  ![Screenshot 2025-04-24 142035](https://github.com/user-attachments/assets/381cc03b-7eb5-472f-a87a-e60be87f82ee)

- Collaborative Filtering menggunakan model Deep Learning, RecommenderNet  
    RecommenderNet adalah model berbasis deep learning yang menggunakan lapisan embedding untuk memetakan pengguna dan item (movie) ke dalam ruang vektor berdimensi rendah. Setiap pengguna dan item diwakili oleh vektor, dan prediksi nilai dibuat dengan menghitung dot product dari kedua lapisan. Model dilatih dengan loss function seperti Root Mean Squared Error, dan Adam optimizer digunakan untuk mengoptimasikannya. Dan pada pendekatan ini, rekomendasi movie yang diberikan adalah berdasarkan penilaian yang diberikan pengguna. Berikut adalah contoh outputnya:

  ![Screenshot 2025-04-24 142949](https://github.com/user-attachments/assets/64f1e874-5e32-4318-bce7-2babc51ae7a1)


---

Kelebihan dan kekurangan dari Cosine Similarity.

Kelebihan:

1. Efektif untuk data berdimensi tinggi
2. Mengukur kemiripan berdasarkan arah, bukan besar nilai
3. Mudah diimplementasikan

Kekurangan:

1. Tidak mempertimbangkan besarnya rating
2. Kurang akurat jika semua nilai rendah atau nol
3. Tidak memperhitungkan bias pengguna

## Evaluation

- Metrik yang digunakan.
  Metrik yang digunakan dalam proyek ini adalah root mean squared error (RMSE). Root Mean Squared Error (RMSE) adalah metrik evaluasi yang digunakan untuk mengukur seberapa jauh prediksi sistem rekomendasi dari nilai rating yang sebenarnya.

  ![Screenshot 2025-04-21 113631](https://github.com/user-attachments/assets/05d4b9d6-f8c0-4bfc-91b7-1a9d8b25225e)



- Formula metrik dan bagaimana metrik tersebut bekerja.

  RMSE didefinisikan dengan rumus berikut:
  
  ![rmse2](https://github.com/user-attachments/assets/6f20e44c-0e02-4586-898c-b08894af7d02)


di mana:

- yi = rating aktual sebenarnya ke-i
- pi = rating yang diprediksi ke-i
- n = jumlah total data prediksi
- (yi - pi)^2 = kuadrat dari selisih antara rating aktual dan prediksi

- Cara kerja RMSE.

  - Mengukur error: Untuk setiap pasangan prediksi dan nilai aktual, sistem menghitung selisihnya.
  - Mengkuadratkan selisih: Memberi penalti lebih besar terhadap kesalahan besar (karena error dikuadratkan).
  - Mengambil rata-rata dari seluruh kuadrat error: Ini menghasilkan nilai MSE (Mean Squared Error).
  - Mengakarkan hasil MSE: Supaya satuannya kembali ke skala asli rating (misalnya 1–5), maka digunakan akar kuadrat.

- Hasil proyek berdasarkan metrik evaluasi terhadap setiap problem statement, goals dan solution statement

  - Problem Statement

    - Pengguna kesulitan menemukan movie yang sesuai dengan preferensi mereka: Penurunan nilai RMSE menunjukkan bahwa model dapat memprediksi rating dengan lebih akurat, yang membuat sistem rekomendasi lebih relevan dan membantu pengguna menemukan movie yang sesuai tanpa mencari secara manual.
    - Content-Based Filtering menghasilkan rekomendasi yang monoton: Dengan prediksi yang semakin akurat (RMSE turun signifikan), model dapat menggabungkan informasi tentang fitur movie, seperti genre, dengan preferensi pengguna. Dengan demikian, sistem dapat menyarankan movie yang berbeda namun relevan meskipun berbasis konten.
    - Collaborative Filtering menghadapi masalah cold-start dan data sparsity: Meskipun ada sedikit data interaksi pengguna, nilai RMSE pada data uji tetap rendah dan stabil. Ini menunjukkan bahwa model masih dapat membuat prediksi yang layak bahkan dalam situasi di mana ada sedikit data pengguna atau item baru.

  - Goals

    - Membantu pengguna menemukan movie yang sesuai dengan preferensi mereka: Prediksi rating yang akurat dengan nilai RMSE yang rendah diberikan oleh sistem rekomendasi yang berhasil, sehingga rekomendasi yang ditampilkan lebih personal dan sesuai dengan minat pengguna, sehingga pengguna tidak perlu mencari daftar movie secara manual.
    - Menghindari rekomendasi yang monoton dari sistem berbasis konten: Sistem dapat memberikan rekomendasi yang tidak hanya sebanding dengan preferensi sebelumnya tetapi juga mencakup movie-movie lain yang relevan namun belum pernah ditonton, meningkatkan keanekaragaman tontonan dengan menggunakan Content-Based Filtering berdasarkan genre dan Collaborative Filtering berdasarkan rating.
    - Collaborative Filtering menghadapi masalah cold-start dan data sparsity: Sistem menunjukkan kinerja prediksi yang baik (berdasarkan metrik RMSE). Ini menunjukkan bahwa model dapat menangani situasi cold-start secara moderat sambil tetap memberikan rekomendasi awal yang layak untuk pengguna atau movie baru.
