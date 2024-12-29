from django.shortcuts import render

# Create your views here.

class IndexView(generic.ListView):
    template_name = "battles/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Battle.objects.order_by("id")

def battle_turn_view(request, battle_id, turn):
    battle_turn_view = get_object_or_404(Battle, pk=battle_id)
    template_name = "polls/detail.html"

