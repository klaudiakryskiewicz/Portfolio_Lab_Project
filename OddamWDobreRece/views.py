import json

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
        foundation_list = Institution.objects.filter(type=1).order_by('id')
        paginator_foundations = Paginator(foundation_list, 5)
        page = request.GET.get('page')
        foundations = paginator_foundations.get_page(page)
        non_gov_list = Institution.objects.filter(type=2).order_by('id')
        paginator_non_gov = Paginator(non_gov_list, 5)
        page = request.GET.get('page')
        non_gov = paginator_non_gov.get_page(page)
        local_col_list = Institution.objects.filter(type=3).order_by('id')
        paginator_local_col = Paginator(local_col_list, 5)
        page = request.GET.get('page')
        local_col = paginator_local_col.get_page(page)

        return render(request, 'index.html',
                      {'bags': no_of_bags, 'institutions': no_of_institutions, 'foundations': foundations,
                       'non_gov': non_gov, 'local_col': local_col})


class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()  # na korelację z kategoriami
        context = {
            'categories': categories,
            'institutions': institutions,
        }  # stworzyć skrypt w htmlu i odebrać w app.js, json, można w ajaxie i zrobić zapytanie do serwera
        return render(request, 'form.html', context)

    def post(self, request):
        new_donation = request.POST  # zmień na nazwy z htmla
        institution = Institution.objects.get(id=new_donation['organization'])
        donation = Donation.objects.create(quantity=new_donation['bags'],
                                           institution=institution,
                                           address=new_donation['address'],
                                           city=new_donation['city'],
                                           zip_code=new_donation['postcode'],
                                           phone_number=new_donation['phone'],
                                           pick_up_date=new_donation['date'],
                                           pick_up_time=new_donation['time'],
                                           pick_up_comment=new_donation['more_info'],
                                           user=request.user)

        for id in new_donation['categories']:
            donation.categories.add(Category.objects.get(id=id))

        donation.save()
        print(donation)
        return redirect(reverse('form-confirmation'))


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
        donations = Donation.objects.filter(user=request.user).filter(is_taken=False)
        past_donations = Donation.objects.filter(user=request.user).filter(is_taken=True)
        context = {'donations': donations, 'past_donations': past_donations}
        return render(request, 'profile.html', context)


class Archive(View):

    def post(self, request):
        donation_id = request.POST.get("donation_id")
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('profile'))


class Settings(PasswordChangeView):
    success_url = reverse_lazy('profile')


class FormConfirmation(View):

    def get(self, request):
        return render(request, 'form-confirmation.html')
