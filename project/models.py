from django.db import models


class Project(models.Model):
    title = models.CharField("Название проекта", max_length=200)
    address = models.CharField("Адрес", max_length=255)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='projects/')
    is_flipped = models.BooleanField("Перевёрнут", default=False)

    def __str__(self):
        return self.title


class ProjectDetail(models.Model):
    project = models.ForeignKey(Project, related_name='details', on_delete=models.CASCADE)
    text = models.CharField("Деталь", max_length=255)

    def __str__(self):
        return f"{self.project.title} - {self.text}"


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectCategoryImages(models.Model):
    image = models.ImageField("Category image", upload_to='projects/')
    category = models.ForeignKey(ProjectCategory, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name
