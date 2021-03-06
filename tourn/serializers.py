from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from tourn.models import (
    Team,
    Match,
    Tournament,
    TeamEntry,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class UsernameSerializer(serializers.RelatedField):
    """Serializes User instances as their username."""
    read_only = False

    def to_native(self, user):
        return user.username

    def from_native(self, data):
        return get_object_or_404(User, username=data)


class TournamentField(serializers.RelatedField):
    class Meta:
        model = Tournament
        fields = ('name', 'id', 'planned_start')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'id', 'min_team_size', 'max_team_size',
                  'min_teams_per_match', 'max_teams_per_match', 'matches')

    min_team_size = serializers.IntegerField(default=2, min_value=1)
    max_team_size = serializers.IntegerField(default=2, min_value=1)

    min_teams_per_match = serializers.IntegerField(default=2, min_value=1)
    max_teams_per_match = serializers.IntegerField(default=2, min_value=1)


class TeamNameField(serializers.RelatedField):
    """Serializes Team instances as their name."""
    read_only = False

    def to_native(self, team):
        return team.name

    def from_native(self, data):
        return get_object_or_404(Team, name=data)


class TeamEntrySerializer(serializers.ModelSerializer):
    team = TeamNameField()
    players = UsernameSerializer(many=True)

    class Meta:
        model = TeamEntry
        fields = ('id', 'team', 'players', 'tournament')


class MemberField(serializers.RelatedField):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ('id', 'name')


class TeamEntryField(serializers.ModelSerializer):
    read_only = False
    members = MemberField(many=True, source='get_member_names')

    class Meta:
        model = TeamEntry
        fields = ('id', 'members', 'tournament')


class TeamSerializer(serializers.ModelSerializer):
    """Serialize a team, with entries intact."""
    tournament_entries = TeamEntryField(many=True, source='entries',
                                        read_only=True)

    class Meta:
        model = Team
        fields = ('name', 'id', 'creator', 'tournament_entries')


class MatchSerializer(serializers.ModelSerializer):
    teams = TeamNameField(many=True)

    class Meta:
        model = Match
        fields = ('name', 'id', 'teams', 'tournament')
