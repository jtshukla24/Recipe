from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login')
def recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get('recipe_image')
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        messages.success(request, 'Recipe created successfully!')
        return redirect("/recipe/")
        # return redirect("/")
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, "recipe.html", context)


@login_required(login_url='/login')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    messages.success(request, 'Recipe deleted successfully!')
    return redirect('/recipe/')

@login_required(login_url='/login')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get("recipe_image")

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if queryset.recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()
        messages.success(request, 'Recipe updated successfully!')
        return redirect('/recipe/')

    context = {'recipes': queryset}
    return render(request, "update_recipe.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'The username you entered does not exist.'
                                    ' Please try again or register for a new account.')
            return redirect('/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('/')

        else:
            login(request, user)
            return redirect("/recipe/")

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'The username is already taken. Please choose a different username.')
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'account created successfully')

        return redirect('/')
    return render(request, "register.html")


def logout_page(request):
    logout(request)
    return redirect('/')
