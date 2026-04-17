from django.contrib import admin

# Register your models here.

from .models import Relation, RelationType, Person

admin.site.register(Relation)
admin.site.register(Person)
admin.site.register(RelationType)

