# 🚀 Deploy WAI Real Asian v5.0 (Pony SDXL) ke Replicate via GitHub Actions

Repositori ini berisi konfigurasi **Cog** untuk mengemas checkpoint model **WAI Real Asian v5.0 (waiREALCN_v50)** dari Hugging Face ke dalam container GPU Replicate secara otomatis menggunakan **GitHub Actions**.

---

## 📋 Langkah-Langkah Deploy (Cukup 1 Kali Setup)

### Langkah 1: Buat Model di Replicate
1. Buka [https://replicate.com/create](https://replicate.com/create) di browser.
2. Isi formulir:
   - **Model name:** `wai-real-cn`
   - **Owner:** `xirecentxz` (atau username Replicate Anda)
   - **Visibility:** Pilih **Private** 🔒 *(hanya Anda dan STB Anda yang bisa akses)*
   - **Hardware:** Pilih **Nvidia A40 (Large)** atau **Nvidia L40S**
3. Klik tombol **Create model**.

---

### Langkah 2: Buat Repositori Baru di GitHub & Unggah Folder Ini
1. Buka [https://github.com/new](https://github.com/new).
2. Beri nama repositori, misalnya: `replicate-wai-real-cn` (bisa Public atau Private).
3. Di PC / Laptop Anda, masuk ke folder ini lalu jalankan:
   ```bash
   git init
   git add .
   git commit -m "feat: initial cog deployment for wai-real-cn"
   git branch -M main
   git remote add origin https://github.com/xirecentxz/replicate-wai-real-cn.git
   git push -u origin main
   ```

---

### Langkah 3: Tambahkan Token Replicate ke GitHub Secrets
1. Di halaman repositori GitHub Anda, klik tab **Settings** (di menu atas).
2. Di sidebar kiri, klik **Secrets and variables** -> **Actions**.
3. Klik tombol hijau **New repository secret**.
4. Isi data:
   - **Name:** `REPLICATE_API_TOKEN`
   - **Secret:** *(Tempelkan API token Replicate Anda yang berawalan `r8_...`)*
5. Klik **Add secret**.

---

### Langkah 4: Jalankan Build Otomatis di GitHub Actions ⚡
1. Klik tab **Actions** di repositori GitHub Anda.
2. Di sebelah kiri, klik workflow **Build and Push to Replicate**.
3. Di sebelah kanan, klik menu dropdown **Run workflow** lalu tekan tombol hijau **Run workflow**.
4. **Selesai!** GitHub Cloud akan:
   - Mengunduh file `waiREALCN_v50.safetensors` (6.6 GB) langsung dari Hugging Face via koneksi 10 Gbps cloud (~20 detik).
   - Mengemas container Docker GPU menggunakan `cog`.
   - Mengunggah container langsung ke `r8.im/xirecentxz/wai-real-cn`.
5. Anda bisa melihat prosesnya berjalan secara live. Setelah selesai (berwarna hijau centang), model Anda sudah aktif 100% di Replicate!

---

### Langkah 5: Hubungkan ke Portal STB Anda
Setelah proses di GitHub Actions selesai, beri tahu AI di chat ini, dan AI akan langsung mendaftarkan model `xirecentxz/wai-real-cn` ke dropdown menu di portal STB Anda ([https://portal.xirecentxz.my.id/image](https://portal.xirecentxz.my.id/image)).
