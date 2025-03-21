# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Empleado

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingresa una dirección de correo válida.')
    
    class Meta:
        model = Empleado
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Opcional. 150 caracteres o menos. Letras, dígitos y @/./+/-/_.'
        self.fields['password1'].help_text = 'La contraseña debe tener al menos 8 caracteres.'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'
        
        # Añadir clases para estilos CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir clases para estilos CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})