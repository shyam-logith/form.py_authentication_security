from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'name',
            'age',
            'email',
            'course',
            'phone',
            'address'
        ]

    def clean_age(self):

        age = self.cleaned_data['age']

        if age < 18:
            raise forms.ValidationError(
                "Student must be at least 18 years old."
            )

        return age

    def clean_email(self):

        email = self.cleaned_data['email']

        if not email.endswith('@gmail.com'):
            raise forms.ValidationError(
            "Please enter a Gmail address."
        )

        return email