import requests
from django.shortcuts import render, redirect
from .forms import ResumeForm

# URL for FastAPI backend
FASTAPI_URL = 'http://localhost:8000/upload/'

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            api_key = form.cleaned_data['api_key']
            pdf_file = request.FILES['pdf_file']

            # Send the file and API key to the FastAPI backend
            files = {'pdf_file': pdf_file}
            data = {'api_key': api_key}
            response = requests.post(FASTAPI_URL, files=files, data=data)

            if response.status_code == 200:
                html_resume = response.text
                return render(request, 'display_resume.html', {'html_resume': html_resume})
            else:
                return render(request, 'resume_form.html', {'form': form, 'error': 'Failed to generate HTML'})
    else:
        form = ResumeForm()

    return render(request, 'resume_form.html', {'form': form})
