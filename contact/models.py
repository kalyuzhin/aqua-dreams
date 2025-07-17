from django.db import models

class Contact(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    phone_number = models.CharField("Номер телефона", max_length=20)
    pool_slug = models.SlugField("Слаг бассейна", max_length=100, blank=True, null=True)
    pool_name = models.CharField("Название бассейна", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.full_name} - {self.phone_number}"