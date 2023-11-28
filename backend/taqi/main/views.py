from django.http import JsonResponse
from django.conf import settings
import logging
# Create your views here.
logger = logging.getLogger(__name__)
logger.info(getattr(settings, "CORS_ALLOW_CREDENTIALS", ()))

def index(request):
    return JsonResponse({'status': getattr(settings, "CORS_ALLOW_CREDENTIALS", ())})