# SIBEO - Sistem Belajar Online (Frontend)
Repositori ini berisi kode sumber untuk server frontend SIBEO (Sistem Belajar Online).

![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css)
![shadcn/ui](https://img.shields.io/badge/shadcn/ui-Components-black?style=for-the-badge&logo=shadcnui)

## Tech Stack
- **Framework**: [Next.js 15 (App Router)](https://nextjs.org/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **UI Components**: [shadcn/ui](https://ui.shadcn.com/)
- **State Management**: React Context API
- **Content Rendering**: `react-markdown`
- **Language**: JavaScript (JSX)

---

## Memulai (Local Development)
Ikuti langkah-langkah berikut untuk menjalankan project di komputer lokal Anda:

### 1. Persiapan
Pastikan Anda sudah menginstall [Node.js](https://nodejs.org/) (versi 18+) di komputer Anda.

### 2. Clone Repositori
```bash
git clone [https://github.com/SIBEO-9/uas-paw-kelompok9-SIBEO.git](https://github.com/SIBEO-9/uas-paw-kelompok9-SIBEO.git)
cd uas-paw-kelompok9-SIBEO
```

### 3. Install Depedensi
```bash
npm install
```

### 4. Konfigurasi Environment Variables
```bash
NEXT_PUBLIC_API_URL=[https://uas-paw-kelompok9-sibeo.onrender.com/api](https://uas-paw-kelompok9-sibeo.onrender.com/api)
```

### 5. Jalankan Server Development
```bash
npm run dev
```

### 6. Buka di Browser
Buka browser dan kunjungi: **http://localhost:3000**
Aplikasi SIBEO sekarang berjalan di komputer Anda!

## Panduan Testing

### Test Flow Student:
1. **Register** → Pilih "Student" → Isi form → Daftar
2. **Login** → Masukkan email & password
3. **Dashboard** → Lihat statistik dan kursus yang diikuti
4. **Courses** → Browse kursus yang tersedia
5. **Enroll** → Klik detail kursus → "Daftar Kursus"
6. **Belajar** → Lihat modul dan konten kursus

### Test Flow Instructor:
1. **Register** → Pilih "Instructor"
2. **Verifikasi OTP**:
   - Klik "Hubungi Admin" untuk demo
   - Masukkan menggunakan kode OTP
3. **Login** → Masukkan email & password
4. **Dashboard** → Lihat statistik kursus Anda
5. **Buat Kursus** → Klik "Tambah Kursus"
6. **Buat Modul** → Buka detail kursus → "Tambah Modul"
7. **Markdown Editor** → Gunakan tab Edit & Preview
8. **Manage** → Edit atau hapus kursus/modul

---

## Struktur Project

```
sibeo-frontend/
├── app/
│   ├── layout.jsx              # Root layout dengan ThemeProvider
│   ├── page.jsx                # Homepage dengan logo
│   ├── login/page.jsx          # Halaman login dengan error handling
│   ├── register/page.jsx       # Halaman register dengan OTP & validasi
│   ├── courses/
│   │   ├── page.jsx            # Daftar kursus dengan filter & empty state
│   │   └── [id]/page.jsx       # Detail kursus dan enrollment
│   ├── dashboard/page.jsx      # Dashboard students/instructor
│   └── instructor/
│       └── courses/
│           ├── create/page.jsx              # Buat kursus baru
│           └── [id]/
│               ├── page.jsx                 # Detail kursus instructor
│               ├── edit/page.jsx            # Edit kursus
│               └── modules/
│                   ├── create/page.jsx      # Buat modul dengan Markdown
│                   └── [courseId]/modules/[id]/edit/page.jsx
├── components/
│   ├── navbar.jsx              # Navigation dengan logo, dark mode toggle
│   ├── footer.jsx              # Footer dengan GitHub links tim
│   └── ui/                     # shadcn/ui components
├── lib/
│   ├── auth-context.jsx        # Authentication dengan real API
│   ├── theme-provider.jsx      # Dark/Light mode provider
│   └── api.js                  # API service 
├── public/
│   └── logo.png                # Logo SIBEO
├── .env.local                  # Environment variables 
└── package.json                # Dependencies
```

---

## Integrasi dengan Backend

### Backend URL

Backend sudah di-hosting di Render.com:
```
https://uas-paw-kelompok9-sibeo.onrender.com/api
```

### API Endpoints yang Digunakan
**Authentication:**
- `POST /api/register` - Registrasi user
- `POST /api/login` - Login user (returns user_id, email, role)
- `POST /api/logout` - Logout user

**Courses:**
- `GET /api/courses` - Get semua kursus (returns {data: [...], count: n})
- `GET /api/courses/{id}` - Get detail kursus
- `POST /api/courses` - Create kursus (instructor only)
- `PUT /api/courses/{id}` - Update kursus (instructor only)
- `DELETE /api/courses/{id}` - Delete kursus (instructor only)

**Enrollments:**
- `POST /api/enrollments` - Enroll ke kursus (body: {course_id})
- `GET /api/enrollments/me` - Get kursus yang diikuti students
- `DELETE /api/enrollments/{id}` - Unenroll dari kursus

**Modules:**
- `GET /api/courses/{id}/modules` - Get modul dari kursus
- `POST /api/courses/{id}/modules` - Create modul (instructor)
- `PUT /api/modules/{id}` - Update modul (instructor)
- `DELETE /api/modules/{id}` - Delete modul (instructor)

**Dashboard:**
- `GET /api/instructor/dashboard` - Data dashboard instructor
- `GET /api/student/progress` - Progress students

## Tim Pengembang
Kelompok 9 - UAS Pemrograman Aplikasi Web:
1. [Tengku Hafid Diraputra](https://github.com/ThDptr)
2. [Devina Kartika](https://github.com/dvnkrtk)
3. [Riyan Sandi Prayoga](https://github.com/404S4ND1)
4. [Jonathan Nicholaus Damero Sinaga](https://github.com/SinagaPande)

---

**Repository Frontend**: [https://github.com/SIBEO-9/uas-paw-kelompok9-SIBEO.git](https://github.com/SIBEO-9/uas-paw-kelompok9-SIBEO.git)

**Backend API**: https://uas-paw-kelompok9-sibeo.onrender.com/api

© 2025 **SIBEO Team** | UAS Pemrograman Aplikasi Web
