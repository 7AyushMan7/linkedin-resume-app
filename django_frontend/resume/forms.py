from django import forms

class ResumeForm(forms.Form):
    api_key = forms.CharField(label='OpenAI API Key', max_length=100, widget=forms.PasswordInput)
    pdf_file = forms.FileField(label='Upload LinkedIn PDF')
