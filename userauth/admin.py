from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from membership.models import Membership, UserMembership, Subscription

class UserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='User name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'age','sexType','city')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Creating a new UserMembership
            user_membership = UserMembership.objects.create(user=user, membership=self.free_membership)
            user_membership.save()
            # Creating a new UserSubscription
            user_subscription = Subscription()
            user_subscription.user_membership = user_membership
            user_subscription.save()
        return user


class UserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'age','sexType','city', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['id','email','username','first_name','last_name']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','age','sexType','city')}),
    )
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('age','sexType','city')}),
    )

# Re-register UserAdmin
admin.site.register(CustomUser, UserAdmin)