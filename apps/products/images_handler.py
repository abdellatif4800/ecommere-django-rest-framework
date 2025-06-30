from . import models


def saveImages(files, prodid):
    for k in files:
        image = models.Image(
            photo=files.get(k), name=k, product=models.Product.objects.get(id=prodid)
        )
        image.save()
