from django import forms
from django.contrib.auth.models import User
from profiles.models import Profile

class userForm(forms.ModelForm):
    # username= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))

    def __init__(self, *args, **kwargs):
        super(userForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        # fields= '__all__' 



class profileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(profileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'capture':'camera','hidden':True})
            }