from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class FAQ(models.Model):
    """
    A FAQ model for frequently asked questions to be shown on the FAQ page
    """
    question = models.CharField(max_length=100)
    answer = models.TextField()


class CustomerTestimonial(models.Model):
    """
    A model for users to leave testimonials/feedback about their experience
    with the shop/website
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Testimonial {self.body} from (self.author)"
