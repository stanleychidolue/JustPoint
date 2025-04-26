from .forms import NewsLetterForm

CACHE_TIMEOUT = 60*10

form = NewsLetterForm()


def base_request(request):
    context = {"newsletterform": form, }
    return context
