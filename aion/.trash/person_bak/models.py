from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Person(models.Model):
    """
    Names : (fname, lname, nicknames*) basic requirement
    Bio data (DOB, Place of birth, Nationality, Born where,)
    Education data
    Work data
    Pets
    Interests
    """
    #entity = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True, related_name='person_detail')
    firstname = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    nicknames = models.CharField(max_length=1024, blank=True, null=True)
    
    gender = models.CharField(choices=[('male','Male'),('female','Female')], max_length=6, blank=True, null=True)

    # bio
    dob = models.DateField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.firstname} {self.lastname}".title() 


   
class Cat(models.Model):
    name = models.CharField(max_length=100)
    # Cat-specific fields
    
class Institution(models.Model):
    name = models.CharField(max_length=100)
    # Institution-specific fields

class Entity(models.Model):
    name = models.CharField(max_length=100)
    
    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        return f"{self.name} -> {self.entity}"

    class Meta:
        verbose_name_plural = 'entities'




class RelationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    reverse_name = models.CharField(max_length=100, blank=True, null=True, help_text="One-way relation if empty.")
    biological =  models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name

class Relation(models.Model):

    from_entity = models.ForeignKey(Entity, related_name="outgoing", on_delete=models.CASCADE)
    to_entity = models.ForeignKey(Entity, related_name="incoming", on_delete=models.CASCADE)
    relation_type = models.ForeignKey(RelationType, on_delete=models.CASCADE)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    is_bidirectional = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['from_entity', 'to_entity', 'relation_type']
        indexes = [
            models.Index(fields=['from_entity']),
            models.Index(fields=['to_entity']),
            ]
        
    @classmethod
    def get_bidirectional(cls, entity_1, entity_2, relation_type):
        """Get relation regardless of direction for symmetric types"""
        if not relation_type.is_bidirectional:
            return cls.objects.filter(
                from_entity=entity_1,
                to_entity=entity_2,
                relation_type=relation_type
            ).first()
        
        # For bidirectional, check both directions
        return cls.objects.filter(
            models.Q(from_entity=entity_1, to_entity=entity_2) |
            models.Q(from_entity=entity_2, to_entity=entity_1),
            relation_type=relation_type
        ).first()    


    

    def __str__(self):
        return f"{self.from_entity} → {self.relation_type} → {self.to_entity}"
