from django import forms

from .models import Cita, Paciente, Profesional

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
            "cedula", "nombres", "apellidos", "fecha_nacimiento", "genero",
            "estado_civil", "direccion", "ciudad", "provincia", "codigo_postal",
            "correo", "telefono", "telefono_alternativo", "contacto_preferido",
            "contacto_emergencia", "relacion_emergencia", "telefono_emergencia",
            "correo_emergencia", "tipo_sangre", "altura_cm", "peso_kg",
            "alergias", "medicamentos_actuales", "condiciones_cronicas",
            "cirugias_previas", "hospitalizaciones", "antecedentes_familiares",
            "tabaquismo", "consumo_alcohol", "frecuencia_ejercicio",
            "habitos_dieteticos", "seguro_proveedor", "seguro_poliza",
            "seguro_grupo", "seguro_titular", "seguro_relacion",
            "seguro_telefono", "seguro_secundario", "seguro_secundario_proveedor",
            "seguro_secundario_poliza", "metodo_facturacion", "pago_online",
            "profesional", "estado", "observaciones",
        ]
        widgets = {
            "cedula": forms.TextInput(attrs={"maxlength": "10", "inputmode": "numeric", "autocomplete": "off", "placeholder": "Ingrese la cédula"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "direccion": forms.Textarea(attrs={"rows": 3}),
            "alergias": forms.Textarea(attrs={"rows": 3}),
            "medicamentos_actuales": forms.Textarea(attrs={"rows": 3}),
            "condiciones_cronicas": forms.Textarea(attrs={"rows": 3}),
            "cirugias_previas": forms.Textarea(attrs={"rows": 3}),
            "hospitalizaciones": forms.Textarea(attrs={"rows": 3}),
            "antecedentes_familiares": forms.Textarea(attrs={"rows": 3}),
            "habitos_dieteticos": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 4}),
            "altura_cm": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "peso_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"].strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
        return cedula

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["cedula"].disabled = True
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
