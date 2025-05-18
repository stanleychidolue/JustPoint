from django.db import models
from django.core.mail import send_mail
import uuid

# Create your models here.


class Advertisement(models.Model):
    advert_title = models.CharField(max_length=100, default="no advert title")
    # advert_text = models.CharField(max_length=250, default="no advert text")
    # advert_location = models.CharField(max_length=150, choices=(
    #     ('Nav_advert', 'Nav_advert'),
    #     ('CAROUSEL', u'CAROUSEL'),
    #     ('sec2_advert', u'sec2_advert'),
    #     ('sec3_advert', u'sec3_advert'),
    #     ('sec4_advert', u'sec4_advert'),
    #     ('whats-hot_advert', 'whats-hot_advert'),))
    advert_img = models.FileField(
        upload_to="images/advert", default="default_carousel.jpg")
    advert_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.advert_title


class UtilityPayment(models.Model):
    utility_name = models.CharField(max_length=100, default="no advert title")
    utility_image = models.FileField(upload_to="images/utility",
                                     default="utility-default.jpg")
    utility_code = models.CharField(max_length=100, default='no code')

    def __str__(self) -> str:
        return self.utility_name


class HomeAppliances(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True)
    name = models.CharField(max_length=150, unique=True)
    product_img = models.FileField(
        upload_to=f"images/appliance", default="default.jpg")
    price = models.CharField(max_length=200)
    old_price = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.name


class NewsLetterSubscribers(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email


class NewsLetters(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='newsletters/')

    def __str__(self):
        # return self.subject + " " + self.created_at.strftime("%B %d, %Y")
        return self.subject

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        # subscribers = NewsLetterSubscribers.objects.filter(confirmed=True)
        subscribers = NewsLetterSubscribers.objects.all()
        for sub in subscribers:
            send_mail(
                subject=self.subject,
                message=None,
                html_message=contents + (
                    '<br><a href="{}?email={}">Unsubscribe</a>.').format(
                    request.build_absolute_uri(
                        '/user/unsubscribe-newsletter/'),
                    sub.email),

                from_email=None,
                recipient_list=[sub.email],
            )
