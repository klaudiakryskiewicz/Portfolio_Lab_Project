from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import CreateView, FormView

from OddamWDobreRece.forms import RegisterForm
from OddamWDobreRece.models import Donation, Institution, Category


class LandingPage(View):

    def get(self, request):
        no_of_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        no_of_institutions = Institution.no_of_helped(request)
        foundation_list = Institution.objects.filter(type=1)
        paginator_foundations = Paginator(foundation_list, 5)
        page = request.GET.get('page')
        foundations = paginator_foundations.get_page(page)
        non_gov_list = Institution.objects.filter(type=2)
        paginator_non_gov = Paginator(non_gov_list, 5)
        page = request.GET.get('page')
        non_gov = paginator_non_gov.get_page(page)
        local_col_list = Institution.objects.filter(type=3)
        paginator_local_col = Paginator(local_col_list, 5)
        page = request.GET.get('page')
        local_col = paginator_local_col.get_page(page)

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
    # django messages


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy("login")


class Profile(View):

    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        context = {'donations': donations}
        return render(request, 'profile.html', context)


class Archive(View):

    def post(self, request):
        donation_id = request.POST.get("donation_id")
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('profile'))


class Settings(PasswordChangeView):
    pass
