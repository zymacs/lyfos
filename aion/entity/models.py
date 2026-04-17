from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

# class Entity(models.Model):
#     """Abstract base - no table"""
#     name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name

#     class Meta:
#         abstract = True


# filter content types
# filter their content ids
# use that for choice

class EntityType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Entity(models.Model):
    entity_type = models.ForeignKey(EntityType,on_delete=models.CASCADE, null=True, blank=True)
    
    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        return f"{self.entity_type} -> {self.entity}"

    class Meta:
        verbose_name_plural = 'entities'

    
    def get_full_name(self):
        return self.entity.full_name

