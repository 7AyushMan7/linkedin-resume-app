import PyPDF2
from django.shortcuts import render
from django.http import HttpResponse
import openai

def upload_resume(request):
    if request.method == 'POST':
        # Get the uploaded PDF file
        pdf_file = request.FILES['pdf_file']
        api_key = request.POST.get('api_key')
        
        if not api_key:
            return HttpResponse("API key is required.", status=400)

        openai.api_key = api_key

        # Read PDF file
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            return HttpResponse(f"Error reading PDF file: {str(e)}", status=400)
        
        # Use OpenAI API to generate HTML resume
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Generate an HTML resume from the following text:\n\n{text}"}
                ]
            )
            html_resume = response.choices[0].message['content'].strip()
        except Exception as e:
            return HttpResponse(f"Error generating resume: {str(e)}", status=400)

        # Return HTML resume as response
        return HttpResponse(html_resume, content_type="text/html")

    return render(request, 'upload_resume.html')
