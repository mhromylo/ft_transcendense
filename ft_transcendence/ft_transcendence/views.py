from django.contrib.auth.decorators import login_required
from game.models import Player
from django.shortcuts import render, redirect
from game.forms import PlayerProfileForm
from django.http import JsonResponse
from game.models import Game
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



def dashboard(request):
    game = Game.objects.first()  # Example: Get the first game
    game_data = {
        'id': game.id,
        'scores': game.scores,
    }
    return render(request, 'dashboard.html',{game_data: game_data})

def profile(request):
    user = request.user
    if request.method == 'POST':
        user.display_name = request.POST.get('display_name')
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('profile')
    return render(request, 'profile.html', {'user': user})


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

def match_history(request):
    games = Game.objects.all().values('id', 'start_time', 'players__display_name')
    data = [
        {
            'id': game['id'],
            'date': game['start_time'].strftime('%Y-%m-%d %H:%M'),
            'players': [player['display_name'] for player in game['players']]
        }
        for game in games
    ]
    return JsonResponse(data, safe=False)

class RegisterView(View):
    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
        return JsonResponse({'success': True}, status=201)


class LoginView(View):
    def post(self, request, *args, **kwargs):
        # Add your login logic here
        return JsonResponse({"message": "Login successful"})