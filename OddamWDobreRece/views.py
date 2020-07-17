from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import CreateView, FormView

from OddamWDobreRece.forms import RegisterForm
from OddamWDobreRece.models import Donation, Institution, Category


class LandingPage(View):

    def get(self, request):
        no_of_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        no_of_institutions = Institution.no_of_helped(request)
        foundations = Institution.objects.filter(type=1)
        non_gov = Institution.objects.filter(type=2)
        local_col = Institution.objects.filter(type=3)
        return render(request, 'index.html',
                      {'bags': no_of_bags, 'institutions': no_of_institutions, 'foundations': foundations,
                       'non_gov': non_gov, 'local_col': local_col})


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', context)


class Login(LoginView):

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('registration'))
    #django messages


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy("login")
