import uuid

from django.db import models

from entity.models import Entity, EntityType

from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



# Create your models here.

class Person(models.Model):
   
    #entity = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True, related_name='person_detail')
    firstname = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    nicknames = models.CharField(max_length=1024, blank=True, null=True)
    # entity_id = uuid.uuid4()
    gender = models.CharField(choices=[('male','Male'),('female','Female')], max_length=6, blank=True, null=True)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE, null=True, blank=True)
    
    # bio
    dob = models.DateField(blank=True, null=True)


    entities = GenericRelation(
        'entity.Entity',
        content_type_field = 'content_type',
        object_id_field = 'object_id',
        related_query_name = 'person'
    )


    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"
    
    def save(self, *args, **kwargs):
        #if not self.entity_id:
        #    self.entity_id = uuid.uuid4()
        
        # create an entity entry for person
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            
            self.entities.create(
                entity_type=self.entity_type
            )
           
    def __str__(self):
        return f"{self.firstname} {self.lastname}".title() 


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
