from django.contrib import admin
from .models import Species, Plant

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_per_page = 20
    ordering = ('id',)
    fieldsets = (
        (None, {
            'fields': ('name', 'is_active')
        }),
    )

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'species', 'height', 'health_condition', 'water_access', 'registration_date')
    list_filter = ('species', 'health_condition', 'water_access')
    search_fields = ('user__username', 'species__name', 'health_condition')
    list_per_page = 20
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': ('user', 'species')
        }),
        ('Характеристики', {
            'fields': ('height', 'health_condition', 'crown_length', 'water_access')
        }),
        ('Местоположение', {
            'fields': ('location_latitude', 'location_longitude')
        }),
        ('Даты', {
            'fields': ('planting_date', )
        }),
        ('Фотографии', {
            'fields': ('full_growth_photo', 'fetal_photo', 'reference_point_photo')
        }),
    )

    exclude = ('registration_date',)
