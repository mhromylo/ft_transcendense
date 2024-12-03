from django.contrib.auth.decorators import login_required
from .models import Player
from django.shortcuts import render, redirect
from .forms import PlayerProfileForm

@login_required
def user_profile(request):
    player = request.user  # Assuming the user is logged in and is a Player
    return render(request, 'user_profile.html', {'player': player})




@login_required
def update_profile(request):
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = PlayerProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def add_friend(request, player_id):
    player_to_add = Player.objects.get(id=player_id)
    request.user.friends.add(player_to_add)
    return redirect('user_profile')

@login_required
def remove_friend(request, player_id):
    player_to_remove = Player.objects.get(id=player_id)
    request.user.friends.remove(player_to_remove)
    return redirect('user_profile')

