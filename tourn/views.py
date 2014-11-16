import json

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Team,
    Tournament,
    TeamEntry,
    PlayerRandomTeamEntry,
    Match,
)


class MessagePage(generic.TemplateView):
    template_name = 'tourn/message.html'

    def get_context_data(self, message=None, **kwargs):
        context = super(MessagePage, self).get_context_data(**kwargs)
        context['message'] = message
        return context


class TournamentDetail(generic.View):
    template_name = 'tourn/tournament_detail.html'

    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        entries = TeamEntry.objects.filter(tournament=tournament)

        teams_list = [
            {
                'name': entry.team.name,
                'id': entry.team.id,
                'members': list(entry.players.values('username', 'id')),
            }
            for entry in entries
        ]

        matches = Match.objects.filter(tournament=tournament)
        matches_list = [
            {
                'name': match.name,
                'teams': [team.name for team in match.teams.all()],
                'winner': match.winner.name if match.winner else None,
            }
            for match in matches
        ]

        tournament_data = json.dumps({
            'matches': matches_list,
            'teams': teams_list,
        })

        return render(request, self.template_name, {
            'tournament_data': tournament_data,
        })


class TournamentList(generic.ListView):
    model = Tournament
    template_name = 'tourn/tournament_list.html'
    context_object_name = 'tournament_list'


class TeamDetail(generic.DetailView):
    model = Team
    template_name = 'tourn/team_detail.html'
    context_object_name = 'team'


class TeamList(generic.ListView):
    model = Team
    template_name = 'tourn/team_list.html'
    context_object_name = 'team_list'
