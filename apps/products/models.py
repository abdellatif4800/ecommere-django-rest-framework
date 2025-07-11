from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField()
    descreption = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk and Product.objects.filter(pk=self.pk).exists():
            # Only update when it's not creation
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Image(models.Model):
    name = models.CharField(max_length=255, default="Main Image")
    photo = models.ImageField(upload_to="products/")
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )

    photo_url = models.URLField(blank=True, null=True, editable=False)  # New field

    def save(self, *args, **kwargs):
        # Call save first so `photo.url` is available
        self.photo_url = self.photo.url
        # print(self.photo.name)
        super().save(*args, **kwargs)

        # # Only save again if the photo_url is not yet set or changed
        # if self.photo and self.photo_url != self.photo.url:
        #     self.photo_url = self.photo.url
        #     super().save(update_fields=["photo_url"])
