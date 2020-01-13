from django import forms
from accounts.models import users_table


class DocumentForm(forms.ModelForm):
    class Meta:
        model = users_table
        fields = ('Resume',)
