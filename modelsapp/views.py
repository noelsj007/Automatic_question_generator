from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from modelsfile.aqgFunction import AutomaticQuestionGenerator

def generate_questions(request):
    if request.method == 'POST':
        # Get the user's input text from the form
        input_text = request.POST.get('input_text', '')
        # Create an AQG object
        aqg = AutomaticQuestionGenerator()
        # Generate questions from the input text
        question_list = aqg.aqgParse(input_text)
        # Pass the questions to the template
        return render(request, 'questions.html', {'question_list': question_list})
    else:
        # Render the input form for the user to enter text
        return render(request, 'input.html')