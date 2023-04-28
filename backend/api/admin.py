from django.contrib import admin
from api.models import *

# Register your models here.


admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PeekabooUser)