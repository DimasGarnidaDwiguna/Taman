# 🌳 TAMAN KOTA — Simulasi 3D OpenGL (Python)

Versi modular dari simulasi taman kota 3D berbasis **PyOpenGL + Pygame**.  
Setiap bagian taman dipisah menjadi modul tersendiri agar mudah dikembangkan.

---

## 📁 Struktur Proyek

```
taman_kota/
│
├── main.py                  ← Titik masuk program (jalankan ini)
├── requirements.txt
│
├── core/                    ← Sistem inti
│   ├── camera.py            ← Kamera FPS (gerak + rotasi)
│   ├── lighting.py          ← Setup cahaya OpenGL
│   ├── primitives.py        ← Bentuk dasar (box, cylinder, sphere, dll)
│   ├── renderer.py          ← Perakitan seluruh scene
│   └── state.py             ← State animasi global (waktu, sudut)
│
├── environment/             ← Lingkungan & infrastruktur
│   ├── ground.py            ← Rumput, jalan, trotoar, jogging track
│   ├── fence.py             ← Pagar besi taman
│   ├── gate.py              ← Gerbang masuk
│   └── sky.py               ← Langit berwarna gradient
│
└── objects/                 ← Objek / furnitur taman
    ├── tree.py              ← Pohon pinus, bulat, palem
    ├── flower.py            ← Bedeng bunga & semak
    ├── fountain.py          ← Air mancur animasi
    ├── pond.py              ← Kolam ikan, angsa, jembatan kayu
    ├── gazebo.py            ← Gazebo oktagonal
    ├── pergola.py           ← Pergola kayu berranaman
    ├── playground.py        ← Area bermain (perosotan, ayunan, dll)
    ├── toilet.py            ← Toilet umum + panel surya
    ├── bench.py             ← Bangku taman
    ├── lamp.py              ← Lampu taman
    ├── trash_bin.py         ← Tempat sampah 3 warna
    ├── rock.py              ← Batu alam dekoratif
    ├── bike_rack.py         ← Rak + sepeda terparkir
    ├── parking.py           ← Parkir mobil + garis + palang
    └── person.py            ← Manusia berjalan (animasi)
```

---

## 🚀 Cara Menjalankan

### Langkah 1 — Pastikan Python 3.8+

```bash
python --version
```

### Langkah 2 — Install dependensi

```bash
pip install -r requirements.txt
```

> **Windows:** Jika `PyOpenGL_accelerate` gagal, cukup:
> ```bash
> pip install pygame PyOpenGL
> ```

### Langkah 3 — Jalankan dari dalam folder `taman_kota/`

```bash
python main.py
```

Atau dari direktori induk:

```bash
python taman_kota/main.py
```

> **VS Code:** Buka file `main.py`, tekan **F5**.

---

## 🎮 Kontrol Navigasi

| Tombol | Aksi |
|--------|------|
| `W` | Maju |
| `S` | Mundur |
| `A` | Geser kiri |
| `D` | Geser kanan |
| `Q` | Naik |
| `E` | Turun |
| `← →` (Panah) | Putar kamera horizontal |
| `↑ ↓` (Panah) | Tengok atas/bawah |
| Klik kiri + geser mouse | Rotasi kamera |
| `ESC` | Keluar |

---

## 🏛️ Isi Taman

| Objek | Keterangan |
|-------|------------|
| 🌲 Pohon pinus, bulat, palem | Skala & posisi bervariasi |
| ⛲ Air mancur | Semburan parabola animasi |
| 🦢 Kolam ikan + angsa | Angsa berenang melingkar |
| 🌉 Jembatan kayu | Di ujung kolam |
| 🏠 Gazebo oktagonal | Atap dua tingkat + bangku dalam |
| 🌿 Pergola | Sulur & bunga merambat |
| 🛝 Area bermain | Perosotan, ayunan, jungkat-jungkit, palang panjat |
| 🚽 Toilet umum | Panel surya, rambu difabel, wastafel luar |
| 🪑 Bangku taman | 15 bangku tersebar |
| 💡 Lampu taman | 20 tiang lampu |
| 🗑️ Tempat sampah | 3 warna (organik/anorganik/B3) di tiap klaster |
| 🪨 Batu alam | 16 batu dekoratif |
| 🚲 Rak sepeda | 5 sepeda terparkir |
| 🚗 Area parkir | 9 mobil + garis + palang otomatis |
| 🧍 Pengunjung | 25+ karakter animasi berjalan/berlari |
| 🌸 Bedeng bunga | 15 bedeng warna-warni |
| 🏃 Jogging track | 3 pelari animasi |
| 🌅 Langit | Gradient biru horizon ke atas |

---

## 🔧 Troubleshooting

**`No module named 'pygame'`**
```bash
pip install pygame
```

**`No module named 'OpenGL'`**
```bash
pip install PyOpenGL
```

**Layar hitam / blank**
- Update driver GPU
- Coba jalankan lewat Command Prompt (bukan terminal VS Code)

**Windows: Error DLL OpenGL**
```bash
pip uninstall PyOpenGL PyOpenGL_accelerate
pip install PyOpenGL PyOpenGL_accelerate
```

**FPS lambat**
- Target 60 FPS; normal jika turun saat banyak objek
- Tutup aplikasi berat lainnya
#
