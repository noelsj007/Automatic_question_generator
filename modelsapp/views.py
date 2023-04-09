from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserAdminCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
from django.shortcuts import render
from modelsfile.aqgFunction import AutomaticQuestionGenerator

@login_required

def generate_questions(request):
    user = request.user
    today = datetime.datetime.now().date()
    if request.method == 'POST':
        # Get the user's input text from the form
        input_text = request.POST.get('input_text', '')
        # Create a new question set
        question_set = GeneratedQuestionSet.objects.create(
            name='Generated questions for %s' % today,
            user=user
        )
        # Create an AQG object
        aqg = AutomaticQuestionGenerator()
        # Generate questions from the input text
        question_list = aqg.aqgParse(input_text)
        # Save the questions to the database
        for question in question_list:
            GeneratedQuestion.objects.create(
                question_text=question,
                question_set=question_set
            )
        # Pass the questions to the template
        return render(request, 'questions.html', {'question_list': question_list})
    else:
        # Render the input form for the user to enter text
        return render(request, 'input.html')


def loginPage(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('generate_questions')
        
        else:
            messages.info(request, 'Password Or Username is incorrect')
            

    return render(request, 'login.html')


def registerPage(request):

    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('first_name')

            messages.success(request, 'Account Created for ' + str(user) + ' Please login')
            return redirect('login')
    return render(request, 'register.html', {'form': form}) 


def homePage(request):
    return render(request, 'index.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

# def savedQuestionsPage(request):
#     user = request.user
#     saved_questions = SavedQuestions.objects.filter(user=user).all()
#     print(saved_questions)
#     for i in saved_questions:
#         print(saved_questions.savedquestions)
#     return render(request, 'savedquestions.html', {saved_questions: 'saved_questions'})

# def view_questions(request):
#     generated_questions = GeneratedQuestions.objects.all()
#     return render(request, 'generated_questions.html', {'generated_questions': generated_questions})


def savedQuestionsPage(request):
    user = request.user
    generated_question_sets = GeneratedQuestionSet.objects.filter(user=user)
    return render(request, 'savedquestions.html', {'generated_question_sets': generated_question_sets})