from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label="Usuario:", min_length=6, max_length=12, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: peluche'}))
    nombre = forms.CharField(label="Nombre:", max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Manuel'}))
    apellido = forms.CharField(label="Apellido:", max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Velez'}))
    email = forms.CharField(label="Email:", max_length=75, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ej.: manuelvelez@hotmail.com'}))
    password1 = forms.CharField(label="Contraseña:", min_length=8, max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Ej.: de*738Hoewiux!$'}))
    password2 = forms.CharField(label="Repita la contraseña:", min_length=8, max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Ej.: de*738Hoewiux!$'}))
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombres", "apellidos", "fecha_nacimiento", "genero", "correo",
            "telefono", "direccion", "tipo_sangre", "contacto_emergencia",
            "telefono_emergencia", "profesional", "estado", "observaciones",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profesional"].queryset = Profesional.objects.filter(
            activo=True
        ).order_by("apellido", "nombre")


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            "paciente", "profesional", "fecha_hora", "duracion_minutos",
            "modalidad", "motivo", "notas",
        ]
        widgets = {
            "fecha_hora": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "duracion_minutos": forms.NumberInput(attrs={"min": 15, "step": 15}),
            "notas": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["paciente"].queryset = Paciente.objects.filter(
            estado="ACTIVO"
        ).order_by("apellidos", "nombres")
        self.fields["profesional"].queryset = Profesional.objects.filter(
            activo=True
        ).order_by("apellido", "nombre")
        self.fields["fecha_hora"].input_formats = ["%Y-%m-%dT%H:%M"]
