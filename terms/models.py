from django.db import models
from django.utils.text import slugify

class TermsPool(models.Model):
    name = models.CharField(max_length=200)
    description_short = models.TextField(
        verbose_name="Краткое описание",
        blank=True,
        help_text="Короткое описание (до 300 символов)"
    )
    main_image = models.ImageField(upload_to='terms_pools/main/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class TermsPoolImage(models.Model):
    pool = models.ForeignKey(TermsPool, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='terms_pools/gallery/')

    def __str__(self):
        return f"Изображение для {self.pool.name}"


class TermsPoolDescription(models.Model):
    pool = models.OneToOneField(
        TermsPool,
        related_name='description_obj',
        on_delete=models.CASCADE,
        primary_key=True
    )
    description = models.TextField(verbose_name="Полное описание")

    def __str__(self):
        return f"Описание для {self.pool.name}"
