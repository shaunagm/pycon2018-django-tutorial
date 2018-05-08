from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class UsersView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'polls/users.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["staff"] = [user for user in User.objects.all() if
                                user.is_staff]
            context["non_staff"] = [user for user in User.objects.all() if
                                not user.is_staff]
            return context


class CreateCommentView(generic.edit.CreateView):
    template_name = 'polls/add_comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('polls:detail', kwargs={'pk': self.object.question.id})

    def get_form_kwargs(self):
        kwargs = super(CreateCommentView, self).get_form_kwargs()
        kwargs['question_pk'] = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            kwargs['author'] = self.request.user.username
        return kwargs