from django import forms
from .models import OrderComment, UserProfile, Order
from django.contrib.auth.models import User




class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['comment', ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture', ]



class MyDateTimeInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['model', 'due_back', 'status', ]
        list_editable = ['model']
        widgets = {'due_back': MyDateTimeInput}


class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['model']