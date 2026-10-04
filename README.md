# Food Recognition & Nutrition Information

## 📌 Deskripsi

**Food Recognition & Nutrition Information** adalah sistem pengenalan dan klasifikasi citra makanan berbasis **Deep Learning**. Sistem ini digunakan untuk mengenali jenis makanan berdasarkan gambar yang diunggah oleh pengguna, kemudian menampilkan informasi gizi dari makanan yang berhasil dikenali.

Sistem dapat mengenali **51 kelas makanan**. Pengguna cukup mengunggah gambar makanan, kemudian gambar akan diproses dan diklasifikasikan oleh model untuk mendapatkan jenis makanan dengan tingkat keyakinan (*confidence score*) tertentu.

## 🧠 Teknologi

Sistem ini menggunakan:

* **Python** sebagai bahasa pemrograman
* **TensorFlow/Keras** untuk pengembangan dan pelatihan model
* **MobileNetV2** dengan pendekatan *Transfer Learning* sebagai model klasifikasi
* **OpenCV** untuk pengolahan citra
* **Pillow** untuk membaca dan memproses gambar
* **Streamlit** untuk membangun antarmuka aplikasi

Model menggunakan ukuran input gambar **224 × 224 piksel** dan menghasilkan prediksi dari **51 kelas makanan**.

## ⚙️ Cara Kerja Sistem

Secara sederhana, alur sistem adalah:

**Upload gambar → Preprocessing → Klasifikasi menggunakan MobileNetV2 → Hasil prediksi → Informasi gizi**

Gambar makanan yang diunggah akan diproses terlebih dahulu, kemudian diberikan kepada model MobileNetV2 untuk menentukan kelas makanan yang paling sesuai.

## 🎯 Output

Output yang dihasilkan berupa:

* **Nama makanan** yang terdeteksi
* **Confidence score** dari hasil prediksi
* **Informasi gizi** berdasarkan makanan yang terdeteksi, seperti:

  * Kalori
  * Protein
  * Lemak
  * Karbohidrat

Contoh hasil:

```text
Prediksi Makanan : Rendang
Confidence       : 95%

Informasi Gizi
Kalori            : xxx kcal
Protein           : xx g
Lemak             : xx g
Karbohidrat       : xx g
```

Dengan demikian, sistem tidak hanya melakukan **klasifikasi gambar makanan**, tetapi juga memberikan informasi gizi berdasarkan hasil klasifikasi tersebut.

## 📊 Model

Model yang digunakan adalah **MobileNetV2** dengan *Transfer Learning* menggunakan bobot **ImageNet**. Pendekatan ini dipilih karena MobileNetV2 memiliki arsitektur yang relatif ringan sehingga sesuai untuk kebutuhan klasifikasi citra dengan proses yang lebih efisien.

## 💡 Tujuan

Project ini bertujuan untuk menerapkan **Computer Vision dan Deep Learning** dalam mengenali makanan dari citra digital serta memberikan informasi gizi secara otomatis berdasarkan hasil prediksi model.


## ⚠️ Disclaimer

Project ini dibuat **untuk keperluan pembelajaran**, bukan untuk penggunaan profesional atau komersial.

informasi gizi yang digunakan dalam project ini diperoleh/dibantu dengan **AI (Artificial Intelligence)** dan digunakan sebagai bahan pembelajaran. Hasil klasifikasi dan informasi gizi yang ditampilkan oleh sistem **tidak menjamin 100% akurat** dan tidak dapat dijadikan sebagai acuan medis, kesehatan, atau konsultasi gizi.



