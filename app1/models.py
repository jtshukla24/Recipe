from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .util import generate_slug

User = get_user_model()


# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe_images")
    recipe_view_count = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.recipe_name)
        super(Recipe, self).save(*args, **kwargs)
