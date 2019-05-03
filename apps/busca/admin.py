from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import Sequencia, Planta
from forms import SequenciaForm, PlantaForm

class SequenciaAdmin(ModelAdmin):
    list_display = ['titulo', 'data']
    list_filter = ('data', 'tipo')
    form = SequenciaForm

    def queryset(self, request):
        if request.user.is_superuser:
            return Sequencia.objects.all()
        return Sequencia.objects.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()
        

class PlantaAdmin(ModelAdmin):
    list_display = ['nome_cientifico', 'nome_popular']
    form = PlantaForm

    def queryset(self, request):
        if request.user.is_superuser:
            return Planta.objects.all()
        return Planta.objects.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()

admin.site.register(Sequencia, SequenciaAdmin)
admin.site.register(Planta, PlantaAdmin)
