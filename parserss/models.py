from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=1000)
    price = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=1000)
    full_title = models.TextField()
    size = models.CharField(max_length=200, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=50, null=True, blank=True)  # Изменение типа поля
    image_urls = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True, null=True, max_length=500)

    def __str__(self):
        return self.title