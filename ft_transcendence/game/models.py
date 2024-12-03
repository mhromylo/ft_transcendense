from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

class Player(AbstractUser):
    display_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)
    groups = models.ManyToManyField(Group, related_name="player_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="player_permissions", blank=True)

    def __str__(self):
        return self.display_name

    def update_ranking(self):
        self.ranking = (self.ranking * 100) / (self.wins + self.losses)

class Game(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for players'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    players = models.ManyToManyField('Player', related_name='games')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    scores = models.JSONField(default=dict)  # A dictionary to store player scores
    winner = models.ForeignKey('Player', related_name='won_games', null=True, blank=True, on_delete=models.SET_NULL)

    def start_game(self):
        """Start the game and initialize scores."""
        if self.players.count() != 4:
            raise ValueError("A game requires exactly 4 players.")
        self.start_time = timezone.now()
        self.status = 'in_progress'
        self.scores = {str(player.id): 0 for player in self.players.all()}
        self.save()

    def update_score(self, player, points):
        """Update the score of a specific player."""
        if str(player.id) not in self.scores:
            raise ValueError("Player is not part of this game.")
        self.scores[str(player.id)] += points
        self.save()

    def end_game(self):
        """End the game and determine the winner."""
        self.end_time = timezone.now()
        self.status = 'finished'
        if self.scores:
            max_score = max(self.scores.values())
            winners = [player_id for player_id, score in self.scores.items() if score == max_score]
            self.winner = Player.objects.get(id=winners[0]) if len(winners) == 1 else None
        self.save()

    def __str__(self):
        return f"Game #{self.id} - {self.get_status_display()}"

