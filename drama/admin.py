from django.contrib import admin

from drama.models import Genre, Drama


class DramaInline(admin.StackedInline):
    model = Drama
    extra = 2


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = (DramaInline,)
    list_display = ('id', 'name', 'description')


@admin.register(Drama)
class DramaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')

