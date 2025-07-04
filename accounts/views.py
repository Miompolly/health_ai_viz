from cProfile import Profile
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Account
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(request, f'Account created for {user.email}!')
            return redirect('login') 
        else:
            messages.error(request, 'Form is invalid. Please check the data and try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)

            if not user.is_active:
                messages.error(request, 'Your account is not active. Please contact support.')
                return render(request, 'accounts/login.html')

            if user.check_password(password):
                auth_login(request, user)

                if user.role == "admin":
                    return redirect('admin_dashboard')
                elif user.role == "doctor":
                    return redirect('dashboard')
                else:
                    return redirect('nurse_dashboard')
            else:
                messages.error(request, 'Invalid password')

        except get_user_model().DoesNotExist:
            messages.error(request, 'Invalid email address')

        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'pages/profile.html', {'user': request.user})



def add_profile_view(request):
    return render(request, 'pages/add_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user

    # ✅ Safely get or create the profile
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')

        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.birth_date = request.POST.get('birth_date')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')  # Update this to your actual profile view name

    # Send both user and profile to the template
    return render(request, 'pages/edit_profile.html', {'user': user, 'profile': profile})
