from django.shortcuts import render
import random
from .models import Player

# Create your views here.

def play_game(request):
    choices = ['rock', 'paper', 'scissors']
    result = None
    user_choice = None
    computer_choice = None

    # Initialize session variables for name and score
    if 'player_score' not in request.session:
        request.session['player_score'] = 0
    if 'computer_score' not in request.session:
        request.session['computer_score'] = 0
    if 'player_name' not in request.session:
        request.session['player_name'] = ''

    # Handle player name input
    if request.method == 'POST' and 'set_player_name' in request.POST:
        request.session['player_name'] = request.POST.get('player_name', '').strip()

    player_name = request.session.get('player_name', '')

    if request.method == 'POST' and 'choice' in request.POST:
        user_choice = request.POST.get('choice')
        computer_choice = random.choice(choices)
        if user_choice == computer_choice:
            result = 'Draw!'
        elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'paper' and computer_choice == 'rock') or
            (user_choice == 'scissors' and computer_choice == 'paper')
        ):
            result = 'You win!'
            request.session['player_score'] += 1
        else:
            result = 'You lose!'
            request.session['computer_score'] += 1

        # Update player statistics
        if player_name and player_name.strip():
            player, created = Player.objects.get_or_create(name=player_name.strip())
            if result == 'You win!':
                player.wins += 1
            elif result == 'You lose!':
                player.losses += 1
            else:  # Draw
                player.draws += 1
            player.save()

    # Handle score reset
    if request.method == 'POST' and 'reset_score' in request.POST:
        request.session['player_score'] = 0
        request.session['computer_score'] = 0

    # Handle leaderboard reset
    if request.method == 'POST' and 'reset_leaderboard' in request.POST:
        Player.objects.all().delete()

    # Get leaderboard data - order by win percentage (descending), then total games, then name
    all_players = list(Player.objects.all())
    leaderboard = sorted(all_players, key=lambda p: (p.win_percentage, p.total_games(), p.name), reverse=True)

    return render(request, 'game/play_game.html', {
        'choices': choices,
        'result': result,
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'player_name': player_name,
        'player_score': request.session.get('player_score', 0),
        'computer_score': request.session.get('computer_score', 0),
        'leaderboard': leaderboard,
    })
