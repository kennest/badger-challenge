from urllib.request import Request

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView

from .forms import Model3DForm
from .models import User, Badge, UserBadge, Model3d


@receiver(post_save, sender=Model3d)
def award_badges(sender, instance, created, **kwargs):
    user = instance.user
    if created:
        # Award Collector badge if user has uploaded more than 5 models
        if user.models.count() > 5:
            collector_badge = Badge.objects.filter(name='Collector').first()
            UserBadge.objects.get_or_create(user=user, badge=collector_badge)
    else:
        # Award Star badge if model has more than 1k views
        if instance.views > 1000:
            star_badge = Badge.objects.filter(name='Star').first()
            UserBadge.objects.get_or_create(user=user, badge=star_badge)


def home(request):
    badges = Badge.objects.all()
    models = Model3d.objects.all()
    return render(request, 'home.html', {'badges': badges, 'models': models})


@method_decorator(login_required, name='dispatch')
class Model3DCreateView(CreateView):
    """
      Vue de création d'un pays
    """
    model = Model3d
    form_class = Model3DForm
    template_name = "create_model3D.html"
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        # Look up the author we're interested in.
        # Actually record interest somehow here!
        form = Model3DForm(request.POST,request.FILES, instance=None)
        print(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.save()
            return HttpResponseRedirect(reverse('home'), {"form": form})
        else:
            print(form.errors)
            print(form.non_field_errors())
            return HttpResponseRedirect(reverse('create'), {"form": form})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['form'] = Model3DForm
        return context


@method_decorator(login_required, name='dispatch')
class ModelDetailView(DetailView):
    """
        Vue d'affichage d'une paroisse
    """
    model = Model3d
    template_name = "model_detail.html"

    def get_context_data(self, **kwargs):
        """
            Surchage l'objet context
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        obj = self.get_object()
        obj.views += 1
        obj.save()
        context['object'] = obj
        return context
