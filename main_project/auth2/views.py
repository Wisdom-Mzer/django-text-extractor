from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import pytesseract
from django.http import JsonResponse
from PIL import Image
import subprocess
from django.http import HttpResponse

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def index(request):
    return render(request, 'image_to_text/index.html')

def extract_text(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        img = Image.open(image)

        #extracted_text = pytesseract.pytesseract.run_tesseract(img, output_type=pytesseract.Output.BYTES)
        #result = subprocess.run(['tesseract', 'stdin', 'stdout'], input=img.tobytes(), capture_output=True, text=True)
        #extracted_text = result.stdout
        extracted_text = pytesseract.image_to_string(img)

        f = open('imagex.docx',"w+")
        f.write(extracted_text)
        f.close()


        return JsonResponse({'extracted_text': extracted_text})
    return JsonResponse({'error': 'Invalid request'})


def download_text(request):
    if 'extracted_text' in request.session:
        extracted_text = request.session['extracted_text']
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="extracted_text.txt"'
        response.write(extracted_text)
        return response
    return HttpResponse("No extracted text to download.")

def extract_text(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        img = Image.open(image)

        extracted_text = pytesseract.image_to_string(img)
        request.session['extracted_text'] = extracted_text

        return render(request, 'image_to_text/index.html', {'extracted_text': extracted_text})

    return JsonResponse({'error': 'Invalid request'})
