from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from .models import User, Badge, UserBadge, Model3d


@receiver(post_save, sender=Model3d)
def award_badges(sender, instance, created, **kwargs):
    user = instance.user
    if created:
        # Award Collector badge if user has uploaded more than 5 models
        if user.models.count() > 5:
            collector_badge = Badge.objects.get(name='Collector')
            UserBadge.objects.get_or_create(user=user, badge=collector_badge)
    else:
        # Award Star badge if model has more than 1k views
        if instance.views > 1000:
            star_badge = Badge.objects.get(name='Star')
            UserBadge.objects.get_or_create(user=user, badge=star_badge)


def home(request):
    badges = Badge.objects.all()
    models = Model3d.objects.all()
    return render(request, 'home.html', {'badges': badges, 'models': models})


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
