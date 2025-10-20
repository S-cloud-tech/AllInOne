from .models import GeneralInfo

def site_info(request):
    return {
        "general_info": GeneralInfo.objects.first(),
    }