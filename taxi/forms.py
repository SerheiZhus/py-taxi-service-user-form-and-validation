from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car
from django import forms


class DriverLicenseUpdateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "license_number",

        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) is not 8:
            raise forms.ValidationError("License number must be 8 characters long.")
        elif not license_number[: 3].isupper():
            raise forms.ValidationError("First 3 characters are uppercase letters.")
        elif not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters are digits.")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
