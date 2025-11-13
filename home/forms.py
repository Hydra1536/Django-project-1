from django import forms
from home.models import Contact
from home.models import Order

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your comments'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 11:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone
    def clean_comments(self):
        comments = self.cleaned_data.get('comments', '').strip()
        if len(comments) < 10:
            raise forms.ValidationError("Comments must be at least 10 characters long.")
        return comments
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Delivery Address'}),
        }

    def clean_customer_phone(self):
        phone = self.cleaned_data['customer_phone']
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number")
        return phone

    def clean_customer_address(self):
        address = self.cleaned_data['customer_address']
        if len(address) < 10:
            raise forms.ValidationError("Address is too short")
        return address
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery Address'}),
        }

    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if len(address) < 10:
            raise forms.ValidationError("Please provide a more detailed delivery address.")
        return address