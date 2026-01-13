from django.contrib import admin
from .models import Blogmodel, Projectmodel, Gallerymodel, ContactForm, LikeTableBlog, LikeTableProjects


admin.site.register(Blogmodel)
admin.site.register(Projectmodel)
admin.site.register(Gallerymodel)
admin.site.register(ContactForm)
admin.site.register(LikeTableBlog)
admin.site.register(LikeTableProjects)
