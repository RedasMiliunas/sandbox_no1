from django import forms
from .models import OrderComment

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['comment', ]