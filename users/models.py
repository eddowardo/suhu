from django.db import models
from django.contrib.auth.models import User

# Tidak perlu custom model dulu, kecuali kamu mau tambah field lain.
# Contoh tambahan profil pengguna:
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
