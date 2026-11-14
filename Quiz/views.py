import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question, Option, Participant, Result
from .forms import ParticipantForm

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = None
        if username_or_email and password:
            user_obj = User.objects.filter(username=username_or_email).first()
            if not user_obj:
                user_obj = User.objects.filter(email=username_or_email).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    quizzes = Quiz.objects.all()
    participant = Participant.objects.filter(user=request.user).first()
    my_results = Result.objects.filter(user=request.user)

    for res in my_results:
        all_res = Result.objects.filter(quiz=res.quiz).order_by('-score', 'submitted_at')
        pos = 1
        for item in all_res:
            if item.user == request.user:
                break
            pos += 1
        res.position = pos

    context = {
        'quizzes': quizzes,
        'participant': participant,
        'my_results': my_results,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    participant = Participant.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Participant information updated.')
            return redirect('dashboard')
    else:
        form = ParticipantForm(instance=participant)

    return render(request, 'profile.html', {'form': form})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        questions = Question.objects.filter(quiz=quiz)
        score = 0
        total = questions.count()

        for q in questions:
            selected_id = request.POST.get(f'question_{q.id}')
            if selected_id:
                selected_option = Option.objects.filter(id=selected_id, question=q).first()
                if selected_option and selected_option.is_correct:
                    score += 1

        result = Result.objects.filter(user=request.user, quiz=quiz).first()
        if result:
            result.score = score
            result.total = total
            result.save()
        else:
            Result.objects.create(user=request.user, quiz=quiz, score=score, total=total)

        return redirect('quiz_result', quiz_id=quiz.id)

    questions = list(Question.objects.filter(quiz=quiz))
    random.shuffle(questions)

    for q in questions:
        options = list(Option.objects.filter(question=q))
        random.shuffle(options)
        q.random_options = options

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    my_result = Result.objects.filter(user=request.user, quiz=quiz).first()
    all_results = Result.objects.filter(quiz=quiz).order_by('-score', 'submitted_at')

    position = None
    if my_result:
        pos = 1
        for item in all_results:
            if item.user == request.user:
                position = pos
                break
            pos += 1

    context = {
        'quiz': quiz,
        'my_result': my_result,
        'all_results': all_results,
        'position': position,
    }
    return render(request, 'quiz_result.html', context)
