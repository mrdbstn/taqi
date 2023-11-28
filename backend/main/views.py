from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return JsonResponse({'message': 'Hello, World!'})

def process_csv(request):
    if not request.method == 'POST':
        return JsonResponse({'message': 'Invalid request method.'})
    
    if not request.FILES.get('csv'):
        return JsonResponse({'message': 'No CSV file provided.'})
    
    csv_file = request.FILES.get('csv')