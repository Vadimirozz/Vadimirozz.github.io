from django.db import models

class Sneakers(models.Model):
    image = models.ImageField(upload_to="main/images/sneakers/")
    name = models.CharField('Name', max_length=50)
    price = models.CharField('Price', max_length=15)
    description = models.CharField('Description', max_length=250, default='Description')
    post_description = models.TextField('Post-Description')

    class Meta:
        verbose_name = 'Sneaker'
        verbose_name_plural = 'Sneakers'

    def __str__(self):
        return self.name
