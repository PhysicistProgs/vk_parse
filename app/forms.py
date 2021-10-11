from django import forms


class MainForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    user_list = forms.FileField()
