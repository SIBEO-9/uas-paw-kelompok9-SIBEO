# SIBEO - Sistem Belajar Online

Platform e-learning modern untuk mahasiswa dan instruktur dengan tampilan profesional menggunakan warna hitam, putih, dan ungu.

## Fitur Utama

- **Autentikasi**: Login dan registrasi untuk mahasiswa dan instruktur dengan verifikasi OTP
- **Mode Gelap/Terang**: Toggle dark/light mode untuk kenyamanan pengguna
- **Manajemen Kursus**: CRUD lengkap untuk kursus (instruktur)
- **Modul dengan Markdown**: Instruktur membuat modul dengan Markdown editor dan preview
- **Enrollment**: Mahasiswa bisa mendaftar dan keluar dari kursus
- **Dashboard Interaktif**: Dashboard berbeda untuk mahasiswa dan instruktur dengan data real-time
- **Progress Tracking**: Monitor perkembangan belajar mahasiswa
- **Responsive Design**: Tampilan optimal di semua perangkat

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **State Management**: React Context API
- **Markdown**: react-markdown untuk render konten modul
- **Language**: JavaScript (JSX)

## Instalasi dan Setup

### 1. Download Project

Download ZIP dari Vercel atau clone dari GitHub

### 2. Extract dan Buka di VS Code

```bash
# Extract ZIP file
# Buka folder di VS Code
code sibeo-frontend
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Setup Environment Variables

Buat file `.env.local` di root project:

```env
# Backend API URL - Ganti dengan URL backend di Niagahoster
NEXT_PUBLIC_API_URL=http://localhost:6543/api

# Untuk production, ganti dengan URL backend yang sudah di-deploy
# NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
```

### 5. Jalankan Development Server

```bash
npm run dev
```

Buka browser di `http://localhost:3000`

## Struktur Project

```
sibeo-frontend/
├── app/
│   ├── layout.jsx              # Root layout dengan ThemeProvider
│   ├── page.jsx                # Homepage
│   ├── login/page.jsx          # Halaman login
│   ├── register/page.jsx       # Halaman register dengan OTP
│   ├── courses/
│   │   ├── page.jsx            # Daftar kursus dengan filter
│   │   └── [id]/page.jsx       # Detail kursus dan enrollment
│   ├── dashboard/page.jsx      # Dashboard mahasiswa/instruktur
│   └── instructor/
│       └── courses/
│           ├── create/page.jsx              # Buat kursus baru
│           └── [id]/
│               ├── page.jsx                 # Detail kursus instruktur
│               ├── edit/page.jsx            # Edit kursus
│               └── modules/
│                   ├── create/page.jsx      # Buat modul dengan Markdown
│                   └── [id]/edit/page.jsx   # Edit modul
├── components/
│   ├── navbar.jsx              # Navigation bar dengan dark mode toggle
│   ├── footer.jsx              # Footer dengan GitHub links
│   └── ui/                     # shadcn/ui components
├── lib/
│   ├── auth-context.jsx        # Authentication context
│   ├── theme-provider.jsx      # Dark/Light mode provider
│   └── api.js                  # API service layer
└── public/
    └── logo.png                # Logo SIBEO
```

## Fitur Khusus

### 1. Dashboard Interaktif
- Instruktur: Lihat statistik kursus, total mahasiswa, modul, dan kursus aktif
- Mahasiswa: Lihat kursus yang diikuti, progress, dan modul selesai
- CRUD kursus langsung dari dashboard (instruktur)
- Navigasi cepat ke detail kursus dan edit

### 2. CRUD Kursus (Instruktur)
- **Create**: Buat kursus baru dengan judul, deskripsi, kategori, level
- **Read**: Lihat detail kursus, daftar modul, dan mahasiswa terdaftar
- **Update**: Edit informasi kursus
- **Delete**: Hapus kursus dengan konfirmasi

### 3. Modul dengan Markdown Editor
- Editor markdown dengan tab Edit dan Preview
- Preview real-time menggunakan react-markdown
- Support untuk:
  - Bold, italic, heading
  - Link dan gambar
  - Code block dengan syntax highlighting
  - Blockquote
  - List (ordered dan unordered)
- Mahasiswa hanya melihat preview yang sudah dirender (tanpa kode markdown)
- Video URL opsional untuk setiap modul

### 4. Enrollment Flow
- Mahasiswa bisa mendaftar ke kursus dengan 1 klik
- Check otomatis apakah sudah terdaftar
- Tombol "Keluar dari Kursus" untuk unenroll
- Tracking enrollment di dashboard mahasiswa

### 5. Verifikasi Instruktur (Registrasi)
- Kode OTP: `292929`
- Tombol "Hubungi Admin" ke WhatsApp: 085216069919
- Validasi OTP di frontend sebelum submit

## Integrasi dengan Backend

### Environment Variable

```env
NEXT_PUBLIC_API_URL=http://localhost:6543/api
```

Ganti dengan URL backend production saat deploy.

### API Endpoints yang Digunakan

**Authentication:**
- `POST /api/register` - Registrasi user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user

**Courses:**
- `GET /api/courses` - Get semua kursus
- `GET /api/courses/:id` - Get detail kursus
- `POST /api/courses` - Create kursus (instruktur)
- `PUT /api/courses/:id` - Update kursus (instruktur)
- `DELETE /api/courses/:id` - Delete kursus (instruktur)

**Enrollments:**
- `POST /api/enrollments` - Enroll ke kursus
- `GET /api/enrollments/me` - Get kursus yang diikuti
- `DELETE /api/enrollments/:id` - Unenroll dari kursus

**Modules:**
- `GET /api/courses/:id/modules` - Get modul dari kursus
- `POST /api/courses/:id/modules` - Create modul
- `PUT /api/modules/:id` - Update modul
- `DELETE /api/modules/:id` - Delete modul

**Dashboard:**
- `GET /api/instructor/dashboard` - Data dashboard instruktur
- `GET /api/courses/:id/students` - Daftar mahasiswa di kursus
- `GET /api/student/progress` - Progress mahasiswa

Lihat detail lengkap API di `BACKEND_README.md`

## Deploy ke Vercel

### 1. Push ke GitHub

```bash
git init
git add .
git commit -m "Initial commit SIBEO frontend"
git remote add origin https://github.com/dvnkrtk/uas-paw-kelompok9-SIBEO.git
git push -u origin main
```

### 2. Deploy via Vercel

1. Login ke [vercel.com](https://vercel.com)
2. Klik "Add New Project"
3. Import repository dari GitHub
4. Tambahkan environment variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: URL backend di Niagahoster (misal: `https://api.yoursite.com/api`)
5. Klik "Deploy"

### 3. Custom Domain (Opsional)

Di Vercel dashboard:
1. Pilih project
2. Settings → Domains
3. Tambahkan custom domain

## Development Tips

### Test dengan Backend Lokal

```env
NEXT_PUBLIC_API_URL=http://localhost:6543/api
```

### Test dengan Backend Production

```env
NEXT_PUBLIC_API_URL=https://api.yoursite.com/api
```

### Debugging

Buka browser console untuk melihat error API calls. Look for logs with `[v0]` prefix.

## Catatan Penting

1. **CORS**: Pastikan backend mengizinkan origin dari Vercel (misal: `https://sibeo.vercel.app`)
2. **Environment Variables**: `NEXT_PUBLIC_API_URL` harus diset di Vercel
3. **SSL**: Gunakan HTTPS untuk backend API di Niagahoster
4. **Authentication**: Token JWT disimpan di localStorage
5. **Markdown**: Mahasiswa hanya melihat preview, instruktur bisa edit raw markdown
6. **OTP**: Kode hardcoded `292929` untuk demo, ganti dengan sistem backend di production

## Tim Pengembang

Kelompok 9 - UAS PAW:

1. [Tengku Hafid Diraputra](https://github.com/ThDptr)
2. [Devina Kartika](https://github.com/dvnkrtk)
3. [Riyan Sandi Prayoga](https://github.com/404S4ND1)
4. [Jonathan Nicholaus Damero Sinaga](https://github.com/SinagaPande)
5. Muhammad Fadhil AB

Repository: [https://github.com/dvnkrtk/uas-paw-kelompok9-SIBEO](https://github.com/dvnkrtk/uas-paw-kelompok9-SIBEO)

## Support

Untuk pertanyaan lebih lanjut, hubungi tim development SIBEO atau buka issue di GitHub.

---

**SIBEO** - Sistem Belajar Online | Pusat Ilmu Daring
