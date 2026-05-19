# TAMAN KOTA — Simulasi 3D OpenGL (Python)

Simulasi 3D taman kota berbasis **PyOpenGL + Pygame** dengan kamera FPS, animasi
pengunjung, air mancur, lentera kaca, dan banyak aset taman lainnya. Dibangun
modular sehingga setiap kategori objek (vegetasi, struktur, furnitur,
transportasi, dst.) tinggal di file-nya sendiri.

---

## Struktur Proyek

```
Taman/
│
├── main.py                  ← Titik masuk program (jalankan ini)
├── requirements.txt
│
├── core/                    ← Sistem inti
│   ├── camera.py            ← Kamera FPS (gerak + rotasi keyboard/mouse)
│   ├── layout.py            ← Sistem zona untuk hindari tumpang tindih aset
│   ├── lighting.py          ← Setup cahaya & material OpenGL
│   ├── primitives.py        ← Box, cylinder, sphere, cone, disk (display list)
│   ├── renderer.py          ← Perakitan seluruh scene per frame
│   ├── state.py             ← State animasi global (waktu, sudut)
│   └── text3d.py            ← Render teks 3D (papan nama, rambu)
│
├── environment/             ← Lingkungan & infrastruktur
│   ├── ground.py            ← Rumput, jalan ring, trotoar, jalur, parkir
│   ├── fence.py             ← Pagar besi mengelilingi taman
│   ├── gate.py              ← Gerbang utama + papan "TAMAN KOTA" + info
│   └── sky.py               ← Langit gradient cyan
│
└── objects/                 ← Objek / furnitur taman
    ├── tree.py              ← Pinus, pohon mahkota bulat, palem
    ├── flower.py            ← Bedeng bunga, semak, tanaman pagar
    ├── fountain.py          ← Air mancur animasi (semburan parabola)
    ├── pond.py              ← Kolam, ikan, angsa berenang, jembatan kayu
    ├── gazebo.py            ← Gazebo oktagonal atap dua tingkat
    ├── pergola.py           ← Pergola kayu dengan sulur merambat
    ├── playground.py        ← Perosotan, ayunan, jungkat-jungkit, palang panjat
    ├── toilet.py            ← Toilet umum + panel surya + signage
    ├── bench.py             ← Bangku taman kayu kaki besi
    ├── lamp.py              ← Lampu taman klasik (sangkar kaca + bohlam)
    ├── trash_bin.py         ← Tong sampah 3 warna (organik/anorganik/B3)
    ├── rock.py              ← Batu alam dekoratif
    ├── bike_rack.py         ← Rak parkir + 5 sepeda warna-warni
    ├── parking.py           ← Mobil parkir, lampu jalan, palang, rambu "P"
    └── person.py            ← Manusia low-poly dengan animasi berjalan/berlari
```

---

## Cara Menjalankan

### 1. Pastikan Python 3.8+

```bash
python --version
```

### 2. Install dependensi

```bash
pip install -r requirements.txt
```

> Jika `PyOpenGL_accelerate` gagal di-build di Windows, cukup install yang dasar:
> ```bash
> pip install pygame PyOpenGL
> ```

### 3. Jalankan

Dari folder proyek (`Taman/`):

```bash
python main.py
```

> **VS Code:** buka `main.py`, tekan **F5**.

Program berjalan pada resolusi 1280×720, target frame rate 144 FPS, dan VSync
aktif untuk frame pacing yang halus.

---

## Kontrol Navigasi

| Tombol                  | Aksi                          |
| ----------------------- | ----------------------------- |
| `W` / `S`               | Maju / mundur                 |
| `A` / `D`               | Geser kiri / kanan            |
| `Q` / `E`               | Naik / turun                  |
| `←` / `→`               | Putar kamera (yaw)            |
| `↑` / `↓`               | Tengok atas / bawah (pitch)   |
| Klik kiri + geser mouse | Rotasi kamera bebas           |
| `ESC`                   | Keluar                        |

Pitch dibatasi ±89° agar kamera tidak terbalik. Saat jendela di-resize,
proyeksi otomatis menyesuaikan rasio aspek baru.

---

## Isi Taman

| Objek                          | Keterangan                                                        |
| ------------------------------ | ----------------------------------------------------------------- |
| 🌲 Pohon pinus, bulat, palem   | Skala & posisi bervariasi, tersebar di perimeter dan area dalam   |
| 🌸 Bedeng bunga                | 4 bedeng mengelilingi air mancur + bedeng tersebar warna-warni    |
| 🌿 Semak hijau                 | Cluster bola hijau di sudut-sudut & sepanjang pagar depan         |
| ⛲ Air mancur                   | Tiga tingkat dengan semburan parabola animasi                     |
| 🦢 Kolam ikan + angsa          | Angsa berenang melingkar, ikan-ikan kecil di permukaan            |
| 🌉 Jembatan kayu               | Menyeberangi ujung kolam                                          |
| 🏠 Gazebo oktagonal            | Atap merah dua tingkat, bangku internal                           |
| 🌿 Pergola                     | Rangka kayu dengan sulur & bunga merambat                         |
| 🛝 Area bermain                | Perosotan, ayunan, jungkat-jungkit, palang panjat di area pasir   |
| 🚽 Toilet umum                 | Atap pelana, panel surya, signage gender, wastafel luar           |
| 🪑 Bangku taman                | Tersebar mengelilingi air mancur dan jalur                        |
| 💡 Lampu taman klasik          | Tiang tinggi, sangkar logam, kaca transparan, bohlam kuning hangat |
| 🗑️ Tong sampah 3 warna         | Organik (hijau), anorganik (kuning), B3 (merah) — 10 klaster      |
| 🪨 Batu alam                   | 16 batu dekoratif di pinggir taman                                |
| 🚲 Rak sepeda                  | 5 sepeda warna-warni + papan "PARKIR SEPEDA"                      |
| 🚗 Area parkir                 | 9 mobil low-poly, garis slot putih, palang otomatis, rambu "P"    |
| 🧍 Pengunjung                  | Karakter berjalan / berlari dengan ayunan kaki & lengan           |
| � Langit                      | Gradient cyan ke biru muda + fog horizon                          |

Penempatan aset dijaga oleh `core/layout.py`: tiap struktur besar mendaftarkan
zona terlarangnya, dan aset kecil seperti pohon, bunga, lampu, atau orang akan
otomatis di-skip kalau posisinya bertabrakan.

---

## Catatan Teknis

- **Display lists** dipakai di `core/primitives.py` untuk shape unit
  (cube, cylinder, cone, sphere, disk). Tiap kombinasi `(slices, stacks)`
  dikompilasi sekali, lalu setiap pemanggilan tinggal `glScalef` + `glCallList`.
  Ini memangkas overhead Python→GL drastis dibanding membuat-hapus quadric per
  panggilan.
- **Depth buffer 24-bit** diminta eksplisit (`GL_DEPTH_SIZE = 24`) agar tidak
  ada z-fighting antara rumput dan jalur yang ketinggiannya berdekatan.
- **Polygon offset** dipakai saat menggambar jalur paver di atas rumput.
- **Fog linear** menyatukan objek jauh ke warna horizon untuk kesan kedalaman.
- **Animasi** dijalankan dari satu `AnimationState.time` global, jadi semua
  pengunjung, ikan, angsa, dan semburan air sinkron tanpa perlu mempunyai
  jam masing-masing.

---

## Troubleshooting

**`No module named 'pygame'`**
```bash
pip install pygame
```

**`No module named 'OpenGL'`**
```bash
pip install PyOpenGL
```

**Layar hitam / blank**
- Update driver GPU.
- Coba jalankan lewat Command Prompt biasa, bukan terminal bawaan IDE.

**Windows: error DLL OpenGL**
```bash
pip uninstall PyOpenGL PyOpenGL_accelerate
pip install PyOpenGL PyOpenGL_accelerate
```

**FPS terasa lambat / stutter**
- Target 144 FPS dengan VSync aktif. Bila monitor 60 Hz, frame akan dikunci 60.
- Tutup aplikasi berat yang merebut GPU.
- Jika perangkat lemah, turunkan `TARGET_FPS` di `main.py` atau matikan
  `GL_SWAP_CONTROL` agar tidak terkunci VSync.
