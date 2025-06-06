# -*- coding: utf-8 -*-
"""Recommendation Sistem Rekomendasi_Ahmad Zainul Mufid.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SufiF2C0jUmmUc3fEQUvFdaPgnxcOdma

# Sistem Rekomendasi Sistem
"""

# Commented out IPython magic to ensure Python compatibility.
# Import library
import pandas as pd
# %matplotlib inline

# Menghubungkan google drive ke google colab
from google.colab import drive
drive.mount('/content/drive')

"""# **Data Understanding**"""

!unzip /content/drive/MyDrive/dataset/movies.zip

# Memuat dataset
# src https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system
movies = pd.read_csv('/content/movies.csv')
ratings = pd.read_csv('/content/ratings.csv')

print('Banyak data movies: ', movies.shape[0])
print('Banyak data ratings: ', ratings.shape[0])

movies.head()

ratings.head()

"""Variabel-variabel pada dataset proyek ini adalah sebagai berikut:

*   movies: merupakan movie yang tersedia.
*   ratings: merupakan penilaian seorang user terhadap sebuah movie.

# **Univariate Exploratory Data Analysis**

Variabel Movies


*   Pertama, kita akan melakukan eksplorasi terhadap variabel movies. Mari kita gunakan kode berikut untuk melihat 5 baris data awal dan 5 baris data akhir.
"""

movies

"""Dari tabel di atas dapat diketahui bahwa data movies terdiri dari 3 kolom, yaitu:

- movieId: merupakan identitas movie.
- title: merupakan judul movie sekaligus tahun keluar.
- genres: merupakan genre dari tiap movie.

Dan ternyata ada data yang tidak memiliki genre seperti movie "A Girl Thing (2001)" di atas.

Mari kita lihat seberapa banyak data yang tidak memiliki genre dengan kode berikut.
"""

# Melihat jumlah data movie yang tidak memiliki genre
print(f"Jumlah data movie tanpa genre adalah: {movies[movies['genres'] == '(no genres listed)'].shape[0]} dari {movies.shape[0]} data")

"""Berdasarkan output di atas, kita dapat melakukan beberapa perubahan terhadap data variabel movies, seperti:

- Memisahkan tiap genre dari tiap movie agar genre dapat memiliki struktur yang lebih baik dalam dataset.
- Melakukan perubahan pada movie yang tidak memiliki genre spesifik.

**Variabel Ratings**

Setelah selesai dengan variabel movies, mari kita lanjutkan dengan variabel ratings
"""

ratings

"""Dari tabel di atas dapat diketahui bahwa data movies terdiri dari 4 kolom, yaitu:

- userId: merupakan identitas pengguna yang memberikan penilaian.
- movieId: merupakan identitas movie yang diberi penilaian.
- rating: merupakan penilaian yang diberikan.
- timestamp: merupakan kapan penilaian diberikan oleh pengguna.
"""

# Membuat nilai hanya 2 angka di belakang koma
pd.options.display.float_format = '{:.2f}'.format
ratings.describe()

"""Dari output di atas, dapat diketahui bahwa penilaian paling rendah pada dataset ini adalah 0,5 dan paling tinggi adalah 5,0.

Sekarang, mari kita lihat berapa pengguna yang memberikan penilaian dan berapa movie yang diberikan penilaian dengan kode berikut.
"""

print('Jumlah userId: ', len(ratings.userId.unique()))
print('Jumlah movieId: ', len(ratings.movieId.unique()))

"""# **Data Preprocessing**

**Menggabungkan Data Movies Dengan Ratings**

Agar sistem rekomendasi dapat berjalan dengan baik, mari kita gabungkan kedua dataset yang dimiliki. Dengan ini, nantinya model dapat memberikan rekomendasi yang sesuai kepada pengguna. Mari kita gabungkan data movies dengan ratings dengan kode berikut.
"""

# Menggabungkan data ratings dengan movies berdasarkan movieId
rated_movies = pd.merge(movies, ratings, on='movieId', how='left')

rated_movies

"""# **Data Preparation**

**Mengatasi Missing Value Dan Movie Yang Tidak Memiliki Genre**

Setelah proses penggabungan, mari kita cek lagi datanya apakah ada missing value atau tidak dengan kode berikut.
"""

# Mengecek missing value pada dataframe rated_movies
rated_movies.isnull().sum()

"""Ternyata ada 3376 missing value pada userId, rating dan timestamp. Namun, karena kita memiliki data yang sangat banyak, tidak apa-apa jika data yang memiliki missing value kita drop. Oleh karena itu, mari kita drop dengan kode berikut."""

# Menghilangkan data berisi missing value dengan fungsi dropna()
rated_movies = rated_movies.dropna()

# Mengubah tipe data userId dari float menjadi integer
rated_movies['userId'] = rated_movies['userId'].astype('int')
rated_movies

"""Mari kita cek ulang untuk memastikan tidak ada lagi missing value pada dataset kita."""

# Mengecek kembali missing value pada dataframe rated_movies
rated_movies.isnull().sum()

"""Setelah selesai dengan missing value, selanjutnya mari kita atasi masalah movie yang tidak memiliki genre. Mari kita lihat ulang berapa movie yang tidak memiliki genre dengan kode berikut."""

# Melihat jumlah data movie yang tidak memiliki genre
print(f"Jumlah data movie tanpa genre adalah: {rated_movies[rated_movies['genres'] == '(no genres listed)'].shape[0]} dari {rated_movies.shape[0]} data")

"""Karena data kita masih dapat dibilang terlampau banyak dan genre sebuah movie itu tidak dapat diisi asal-asalan, maka lebih baik kita hapus data movie yang tidak memiliki genre. Kita akan menghapusnya dengan kode sederhana berikut."""

# Menghilangkan data yang bergenre "(no genre listed)"
clean_movies_df = rated_movies[rated_movies['genres'] != '(no genres listed)']

"""Setelah berhasil dihilangkan, mari kita pastikan sekali lagi bahwa tidak ada lagi data yang bergenre "(no genre listed)"."""

# Melihat jumlah data movie yang tidak memiliki genre
print(f"Jumlah data movie tanpa genre adalah: {clean_movies_df[clean_movies_df['genres'] == '(no genres listed)'].shape[0]} dari {clean_movies_df.shape[0]} data")

"""Setelah penghapusan data yang tidak memiliki genre, ternyata data kita masih banyak yaitu, 24.973.456 data. Data ini terlalu banyak untuk sebuah sistem rekomendasi sederhana. Maka dari itu mari kita hapus 99,9% data dari seluruh dataset."""

# Menghapus 99,9% baris data secara acak
clean_movies_df = clean_movies_df.drop(clean_movies_df.sample(frac=0.999, random_state=42).index).reset_index(drop=True)

clean_movies_df

"""Selanjutnya, kita hanya akan menggunakan data yang unik untuk diberikan pada model. Oleh karena itu, mari hapus data yang duplikat berdasarkan id movie."""

# Membuang data duplikat berdasarkan movieId
preparation_df = clean_movies_df
preparation_df = preparation_df.drop_duplicates('movieId')
preparation_df

"""Selanjutnya, kita kan mengkonversi data series menjadi list."""

# Mengonversi data series movieId menjadi dalam bentuk list
movie_id = preparation_df['movieId'].tolist()

# Mengonversi data series title menjadi dalam bentuk list
movie_title = preparation_df['title'].tolist()

# Mengonversi data series genre menjadi dalam bentuk list
movie_genre = preparation_df['genres'].tolist()

print(len(movie_id))
print(len(movie_title))
print(len(movie_genre))

"""Tahap selanjutnya, kita akan membuat dictionary pasangan key-value pada movie_id, movie_name dan movie_genre."""

# Membuat dictionary untuk data 'movie_id', 'movie_title', 'movie_genre'
movie_new = pd.DataFrame({
    'id': movie_id,
    'title': movie_title,
    'genre': movie_genre
})

movie_new

"""# **Model Development dengan Content Based Filtering**

Setelah selesai melakukan tahap preprocessing dan preparation, selanjutnya kita akan melakukan tahap model development. Mari kita mulai dari memindahkan data ke variabel baru.
"""

data = movie_new
data.sample(5)

"""**One-Hot Encoding**

Pada tahap ini, kita akan membangun sistem rekomendasi berdasarkan genre movie. Pada proyek ini kita akan menggunakan teknik One-Hot Encoding terhadap data genre yang dimiliki.
"""

from sklearn.preprocessing import MultiLabelBinarizer

# Mengubah kolom genre dari string menjadi list
data['genres_list'] = data['genre'].apply(lambda x: x.split('|'))

# Inisialisasi dan lakukan one-hot encoding pada genre
mlb = MultiLabelBinarizer()
genre_onehot = mlb.fit_transform(data['genres_list'])

# Buat DataFrame genre dari hasil one-hot encoding
genre_onehot_df = pd.DataFrame(genre_onehot, columns=mlb.classes_, index=data.index)

# Gabungkan dengan data awal
df_final = pd.concat([data[['id', 'title']], genre_onehot_df], axis=1)

df_final.head()

"""**Cosine Similarity**

Setelah mengubah data genre menjadi bentuk One-Hot Encoding, sekarang kita akan menghitung derajat kesamaan antar movie dengan teknik Cosine Similarity.
"""

from sklearn.metrics.pairwise import cosine_similarity

# Menghitung cosine similarity genre pada data movie
cosine_sim = cosine_similarity(genre_onehot)
cosine_sim

"""Selanjutnya, mari kita lihat nilai kesamaan setiap movie dengan menampilkan title movie dalam 5 sampel kolom (axis = 1) dan 10 sampel baris (axis=0). Jalankan kode berikut."""

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa title movie
cosine_sim_df = pd.DataFrame(cosine_sim, index=data['title'], columns=data['title'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap movie
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""Dengan cosine similarity, kita berhasil mengidentifikasi kesamaan antara satu movie dengan movie lainnya.

**Mendapatkan Rekomendasi**

Pada tahap ini kita akan mendapatkan rekomendasi berdasarkan kesamaan yang telah dihitung pada tahap sebelumnya. Kita akan membuat fungsi movie_recommendations dengan beberapa parameter berikut.

- movie_title : Nama movie (index kemiripan dataframe).
- Similarity_data : Dataframe mengenai similarity yang telah kita definisikan sebelumnya.
- Items : Nama dan fitur yang digunakan untuk mendefinisikan kemiripan, dalam hal ini adalah ‘movie_title’ dan ‘genre’.
- k : Banyak rekomendasi yang ingin diberikan.
"""

def movie_recommendations(movie_title, similarity_data=cosine_sim_df, items=data[['title', 'genre']], k=5):
    """
    Rekomendasi Movie berdasarkan kemiripan dataframe

    Parameter:
    ---
    movie_title : tipe data string (str)
                Nama movie (index kemiripan dataframe)
    similarity_data : tipe data pd.DataFrame (object)
                      Kesamaan dataframe, simetrik, dengan movie sebagai
                      indeks dan kolom
    items : tipe data pd.DataFrame (object)
            Mengandung kedua nama dan fitur lainnya yang digunakan untuk mendefinisikan kemiripan
    k : tipe data integer (int)
        Banyaknya jumlah rekomendasi yang diberikan
    ---


    Pada index ini, kita mengambil k dengan nilai similarity terbesar
    pada index matrix yang diberikan (i).
    """


    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,movie_title].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop movie_title agar nama movie yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(movie_title, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

"""Selanjutnya, mari kita terapkan kode di atas untuk menemukan rekomendasi movie yang mirip dengan Lights Out (2016). Terapkan kode berikut:"""

data[data.title.eq('Lights Out (2016)')]

"""Lights Out (2016) masuk dalam genre horror. Tentu kita berharap rekomendasi yang diberikan adalah movie dengan kategori yang mirip. Sekarang, dapatkan rekomendasi movie dengan memanggil fungsi yang telah kita definisikan sebelumnya:"""

movie_recommendations('Lights Out (2016)')

# Fungsi untuk menghasilkan Top-N Recommendation
def movie_recommendations(movie_title, similarity_data=cosine_sim_df, items=data[['title', 'genre']], k=5):
    index = similarity_data.loc[:, movie_title].to_numpy().argpartition(range(-1, -k-1, -1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(movie_title, errors='ignore')
    return pd.DataFrame(closest).merge(items).head(k)

# Contoh Top-5 rekomendasi untuk film 'Lights Out (2016)'
recommendations_cb = movie_recommendations('Lights Out (2016)')
print("Top-5 Rekomendasi untuk 'Lights Out (2016)':")
print(recommendations_cb)

"""# **Model Development Dengan Collaborative Filtering**

Setelah menyelesaikan Model Content Based Filtering, selanjutnya kita akan mengembangkan Model untuk Collaborative Filtering. Berbeda dari teknik sebelumnya yang menggunakan genre, teknik kali ini akan menggunakan rating.

**Data Understanding**

Mari kita import library tambahan yang diperlukan untuk pengembangan ini.
"""

# Import library
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

"""Mari kita pindahkan data dari variabel ratings ke df agar memudahkan proses pengembangan"""

df = ratings
df

"""Dapat dilihat bahwa data yang kita miliki ada sebanyak 25.000.095 data. Seperti yang telah dilakukan pada tahap-tahap sebelumnya, data ini terlalu banyak untuk sebuah sistem rekomendasi sederhana. Maka dari itu mari kita hapus 99,9% data dari seluruh dataset."""

# Menghapus 99,9% baris data secara acak
df = df.drop(df.sample(frac=0.999, random_state=42).index).reset_index(drop=True)

df

"""Dapat dilihat, sekarang kita hanya memiliki 25.000 data yang tersisa.

**Data Preparation**

Selanjutnya pada proses preparation ini, kita akan melakukan encoding pada fitur userId dan movieId menjadi indeks integer.
"""

# Mengubah userId menjadi list tanpa nilai yang sama
user_ids = df['userId'].unique().tolist()
print('list userId: ', user_ids)

# Melakukan encoding userId
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded userId : ', user_to_user_encoded)

# Melakukan proses encoding angka ke ke userId
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke userId: ', user_encoded_to_user)

# Mengubah movieId menjadi list tanpa nilai yang sama
movie_ids = df['movieId'].unique().tolist()

# Melakukan proses encoding movieId
movie_to_movie_encoded = {x: i for i, x in enumerate(movie_ids)}

# Melakukan proses encoding angka ke movieId
movie_encoded_to_movie = {i: x for i, x in enumerate(movie_ids)}

"""Selanjutnya, mapping userId dan movieId tadi ke dalam dataframe."""

# Mapping userId ke dataframe user
df['user'] = df['userId'].map(user_to_user_encoded)

# Mapping movieId ke dataframe resto
df['movie'] = df['movieId'].map(movie_to_movie_encoded)

"""Lakukan pengecekan terhadap jumlah pengguna, movie dan min dan max rating."""

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)

# Mendapatkan jumlah movie
num_movie = len(movie_encoded_to_movie)
print(num_movie)

# Mengubah rating menjadi nilai float
df['rating'] = df['rating'].values.astype(np.float32)

# Nilai minimum rating
min_rating = min(df['rating'])

# Nilai maksimal rating
max_rating = max(df['rating'])

print('Number of User: {}, Number of Resto: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_movie, min_rating, max_rating
))

"""**Membagi Data untuk Training dan Validation**

Sebelum melakukan pembagian dataset, sebaiknya acak data terlebih dahulu agar distribusi pembagian data menjadi random.
"""

# Mengacak dataset
df = df.sample(frac=1, random_state=42)
df

"""Selanjutnya, kita akan membagi data training menjadi 80% dan validation menjadi 20%. Jalankan kode berikut."""

# Membuat variabel x untuk mencocokkan data user dan movie menjadi satu value
x = df[['user', 'movie']].values

# Membuat variabel y untuk membuat rating dari hasil
y = df['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

print(x, y)

"""**Proses Training**

Sebelum memulai proses training, mari definisikan class model yang akan kita gunakan nantinya. Pada proyek ini, kita akan menggunakan RecommenderNet dari Keras Model Class.
"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_movie, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_movie = num_movie
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.movie_embedding = layers.Embedding( # layer embeddings movie
        num_movie,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.movie_bias = layers.Embedding(num_movie, 1) # layer embedding movie bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    movie_vector = self.movie_embedding(inputs[:, 1]) # memanggil layer embedding 3
    movie_bias = self.movie_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)

    x = dot_user_movie + user_bias + movie_bias

    return tf.nn.sigmoid(x) # activation sigmoid

"""Selanjutnya, lakukan compile pada model yang telah didefinisikan."""

model = RecommenderNet(num_users, num_movie, 50) # inisialisasi model

# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""Model ini menggunakan Binary Crossentropy untuk menghitung loss function, Adam (Adaptive Moment Estimation) sebagai optimizer, dan root mean squared error (RMSE) sebagai metrics evaluation.

Langkah berikutnya, mulailah proses training.
"""

# Memulai training

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 32,
    epochs = 20,
    validation_data = (x_val, y_val)
)

"""**Visualisasi Metrik**

Untuk melihat visualisasi proses training, mari kita plot metrik evaluasi dengan matplotlib dengan kode berikut.
"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""Dari proses ini, kita memperoleh nilai error akhir sebesar sekitar 0.17 dan error pada data validasi sebesar 0.25. Nilai tersebut cukup bagus untuk sistem rekomendasi. Mari kita cek, apakah model ini bisa membuat rekomendasi dengan baik."""

# Fungsi untuk menghasilkan Top-N Recommendation berdasarkan user
def top_n_recommendations_collab(user_id, model, df, user_encoded_to_user, movie_encoded_to_movie, k=5):
    user_idx = user_to_user_encoded[user_id]
    movies_watched = df[df['userId'] == user_id]['movieId'].tolist()
    movies_watched_encoded = [movie_to_movie_encoded[m] for m in movies_watched]

    # Semua film yang belum ditonton
    all_movies = np.array(list(set(range(num_movie)) - set(movies_watched_encoded)))
    user_array = np.array([user_idx for _ in range(len(all_movies))])

    # Concatenate user_array and all_movies into a single input array
    input_array = np.stack([user_array, all_movies], axis=1)

    predictions = model.predict(input_array).flatten()

    # Ambil top k
    top_k_indices = predictions.argsort()[-k:][::-1]
    # Get the original movie IDs from the encoded indices
    recommended_movie_ids = [movie_encoded_to_movie[all_movies[i]] for i in top_k_indices]
    recommended_ratings = predictions[top_k_indices]

    return pd.DataFrame({
        'movieId': recommended_movie_ids,
        'predicted_rating': recommended_ratings
    })

# Contoh Top-5 rekomendasi untuk user dengan ID asli 1
recommendations_cf = top_n_recommendations_collab(user_id=1, model=model, df=df,
                                                  user_encoded_to_user=user_encoded_to_user,
                                                  movie_encoded_to_movie=movie_encoded_to_movie, k=5)
print("Top-5 Rekomendasi untuk User 1:")
print(recommendations_cf)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.plot(history.history['root_mean_squared_error'], label='Train RMSE')
plt.plot(history.history['val_root_mean_squared_error'], label='Validation RMSE')
plt.title('Training vs Validation RMSE')
plt.xlabel('Epochs')
plt.ylabel('RMSE')
plt.legend()
plt.show()

"""# **Mendapatkan Rekomendasi Movie**

Untuk mendapatkan rekomendasi movie, pertama kita ambil sampel user secara acak dan definisikan variabel movie_not_watched yang merupakan daftar movie yang belum pernah ditonton oleh pengguna. Sebelumnya, pengguna telah memberi rating pada beberapa movie yang telah mereka tonton. Kita menggunakan rating ini untuk membuat rekomendasi movie yang mungkin cocok untuk pengguna.

Mari kita mulai dengan mengambil sampel pengguna.
"""

movie_df = movie_new

# Mengambil sample user
user_id = df.userId.sample(1).iloc[0]
movie_watched_by_user = df[df.userId == user_id]

# Operator bitwise (~)
movie_not_watched = movie_df[~movie_df['id'].isin(movie_watched_by_user.movieId.values)]['id']
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)

movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]
user_encoder = user_to_user_encoded.get(user_id)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

"""Selanjutnya, gunakan fungsi predict() untuk memperoleh rekomendasi movie."""

ratings = model.predict(user_movie_array).flatten()

top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_to_movie_encoded.get(movie_not_watched[x][0]) for x in top_ratings_indices
]

print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('Movie with high ratings from user')
print('----' * 8)

top_movie_user = (
    movie_watched_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .movieId.values
)

movie_df_rows = movie_df[movie_df['id'].isin(top_movie_user)]
for row in movie_df_rows.itertuples():
    print(row.title, ':', row.genre)

print('----' * 8)
print('Top movies recommendation')
print('----' * 8)

recommended_movie = movie_df[movie_df['id'].isin(recommended_movie_ids)]
for row in recommended_movie.itertuples():
    print(row.title, ':', row.genre)

"""Dari hal yang diperoleh di atas, beberapa rekomendasi movie berupa movie yang bergenre Comedy dan Romance, Drama dan Thriller, Comedy dan Horror, serta hanya Comedy."""

# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
first_movie = watched_movies[0]
first_movie_title = movie_df[movie_df['id'] == first_movie]['title'].values[0]
print(f"\nFilm acuan rekomendasi CBF: {first_movie_title}")

recommendations_cb_user = movie_recommendations(first_movie_title, k=4)
print(f"\nTop-4 Rekomendasi untuk User {user_id}:\n", recommendations_cb_user)

# Tentukan relevansi berdasarkan rating histori user (rating >=4.0 dianggap relevan)
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Hitung Precision@4
# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
first_movie = watched_movies[0]
first_movie_title = movie_df[movie_df['id'] == first_movie]['title'].values[0]
print(f"\nFilm acuan rekomendasi CBF: {first_movie_title}")

recommendations_cb_user = movie_recommendations(first_movie_title, k=4)
print(f"\nTop-4 Rekomendasi untuk User {user_id}:\n", recommendations_cb_user)

# Tentukan relevansi berdasarkan rating histori user (rating >=4.0 dianggap relevan)
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Hitung Precision@4
precision_at_4 = relevan_count / 4
print(f"\nPrecision@4 untuk User {user_id}: {precision_at_4}")
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
first_movie = watched_movies[0]
first_movie_title = movie_df[movie_df['id'] == first_movie]['title'].values[0]
print(f"\nFilm acuan rekomendasi CBF: {first_movie_title}")

recommendations_cb_user = movie_recommendations(first_movie_title, k=4)
print(f"\nTop-4 Rekomendasi untuk User {user_id}:\n", recommendations_cb_user)

# Tentukan relevansi berdasarkan rating histori user (rating >=4.0 dianggap relevan)
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Hitung Precision@4
# Histori rating user 7002
user_id = 7002
histori_user = df[df['userId'] == user_id][['movieId', 'rating']]
print(f'Histori rating user {user_id}:')
print(histori_user.head())

# Ambil semua film yang ditonton user 7002
watched_movies = histori_user['movieId'].tolist()

# Rekomendasi Content-Based Filtering untuk film yang sudah ditonton user 7002 (contoh: film pertama)
first_movie = watched_movies[0]
first_movie_title = movie_df[movie_df['id'] == first_movie]['title'].values[0]
print(f"\nFilm acuan rekomendasi CBF: {first_movie_title}")

recommendations_cb_user = movie_recommendations(first_movie_title, k=4)
print(f"\nTop-4 Rekomendasi untuk User {user_id}:\n", recommendations_cb_user)

# Tentukan relevansi berdasarkan rating histori user (rating >=4.0 dianggap relevan)
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Hitung Precision@4
precision_at_4 = relevan_count / 4
print(f"\nPrecision@4 untuk User {user_id}: {precision_at_4}")
rekomendasi_ids = [movie_df[movie_df['title'] == title]['id'].values[0] for title in recommendations_cb_user['title']]
relevan_count = histori_user[histori_user['movieId'].isin(rekomendasi_ids) & (histori_user['rating'] >= 4.0)].shape[0]

# Hitung Precision@4
precision_at_4 = relevan_count / 4
print(f"\nPrecision@4 untuk User {user_id}: {precision_at_4}")