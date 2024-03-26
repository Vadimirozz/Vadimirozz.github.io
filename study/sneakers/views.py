from django.shortcuts import render
from .models import Sneakers
from django.views.generic import DetailView

def sneakers(request):
	sneakers = Sneakers.objects.all()
	return render(request, 'main/layout.html', {'sneakers': sneakers})

class SneakersDetailView(DetailView):
	model = Sneakers
	template_name = 'main/details_view.html'
	context_object_name = 'sneaker'


