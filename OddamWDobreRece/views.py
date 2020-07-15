from django.shortcuts import render

from django.views import View
from django.views.generic import CreateView

from OddamWDobreRece.forms import RegisterForm
from OddamWDobreRece.models import Donation, Institution


class LandingPage(View):

    def get(self, request):
        no_of_bags = Donation.no_of_bags(request)
        no_of_institutions = Institution.no_of_helped(request)
        foundations = Institution.objects.filter(type=1)
        non_gov = Institution.objects.filter(type=2)
        local_col = Institution.objects.filter(type=3)
        return render(request, 'index.html',
                      {'bags': no_of_bags, 'institutions': no_of_institutions, 'foundations': foundations,
                       'non_gov': non_gov, 'local_col': local_col})


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'


