# TODO: Implementasi Redirect Root ke Halaman Login

## Langkah-langkah:
1. [x] Edit backend/urls.py untuk mengubah root URL agar langsung mengarah ke halaman login
2. [x] Test akses http://127.0.0.1:8000/ untuk memastikan langsung ke halaman login
3. [x] Verifikasi bahwa jika sudah login, redirect ke dashboard
4. [x] Perbaiki logout redirect ke root URL
5. [x] Perbaiki link logout di template agar menggunakan URL absolut

## Detail Perubahan:
- Ubah path('') di backend/urls.py dari include monitor_suhu.urls ke users.views.login_view
- Tambahkan import untuk login_view
- Ubah path dashboard dari '' ke 'dashboard/' di monitor_suhu.urls
- Ubah logout_view redirect dari '/users/login/' ke '/'
- Ubah link logout di base.html dari {% url 'logout' %} ke /users/logout/

## Hasil Test:
- Server berjalan di http://127.0.0.1:8000/
- Akses ke root URL mengembalikan status 200, yang menunjukkan halaman login berhasil dimuat
- Akses ke /dashboard/ tanpa login redirect ke /users/login/?next=/dashboard/ (status 200)
- Tidak ada redirect loop lagi
- Logout sekarang redirect ke root URL (/)

## Masalah yang Ditemukan dan Diperbaiki:
- Redirect loop terjadi karena path('') di backend/urls.py dan monitor_suhu/urls.py sama-sama menangani root URL
- Solusi: Tetap gunakan login_view untuk root URL, dan monitor_suhu.urls untuk path yang berbeda
- Logout redirect ke '/users/login/' yang tidak konsisten dengan root URL baru
- Solusi: Ubah logout redirect ke '/'
- Link logout di template menggunakan {% url 'logout' %} yang mungkin tidak resolve dengan benar
- Solusi: Gunakan URL absolut /users/logout/
