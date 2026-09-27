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
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "profile-file",
            "accept": "image/jpeg,image/png,image/gif",
        }),
    )

    ESTADOS_CIVILES = [
        ("", "Seleccione estado civil"),
        ("SOLTERO", "Soltero"),
        ("CASADO", "Casado"),
        ("DIVORCIADO", "Divorciado"),
        ("VIUDO", "Viudo"),
        ("SEPARADO", "Separado"),
        ("UNION_LIBRE", "Unión libre"),
    ]

    EJERCICIO_OPCIONES = [
        ("", "Seleccione frecuencia"),
        ("NINGUNO", "Ninguno"),
        ("OCASIONAL", "Ocasional"),
        ("REGULAR", "Regular"),
        ("DIARIO", "Diario"),
    ]

    frecuencia_ejercicio = forms.ChoiceField(
        choices=EJERCICIO_OPCIONES,
        required=False,
        label="Frecuencia de ejercicio",
    )

    CONSUMO_OPCIONES = [
        ("", "Seleccione consumo"),
        ("NINGUNO", "Ninguno"),
        ("OCASIONAL", "Ocasional"),
        ("MODERADO", "Moderado"),
        ("ALTO", "Alto"),
    ]

    consumo_alcohol = forms.ChoiceField(
        choices=CONSUMO_OPCIONES,
        required=False,
        label="Consumo de alcohol",
    )

    consumo_drogas = forms.ChoiceField(
        choices=CONSUMO_OPCIONES,
        required=False,
        label="Consumo de drogas",
    )

    TABAQUISMO_OPCIONES = [
        ("", "Seleccione estado"),
        ("NUNCA", "Nunca fumó"),
        ("EXFUMADOR", "Exfumador"),
        ("ACTUAL", "Fumador actual"),
    ]

    tabaquismo = forms.ChoiceField(
        choices=TABAQUISMO_OPCIONES,
        required=False,
        label="Tabaquismo",
    )

    TIPO_IDENTIFICACION_FACTURACION = [
        ("", "Seleccione identificación"),
        ("CEDULA", "Cédula"),
        ("RUC", "RUC"),
        ("PASAPORTE", "Pasaporte"),
        ("CONSUMIDOR_FINAL", "Consumidor final"),
    ]

    tipo_identificacion_facturacion = forms.ChoiceField(
        choices=TIPO_IDENTIFICACION_FACTURACION,
        required=False,
        label="Tipo de identificación",
    )

    METODO_FACTURACION_OPCIONES = [
        ("", "Seleccione método"),
        ("ELECTRONICA_EMAIL", "Factura electrónica por correo"),
        ("ELECTRONICA_WHATSAPP", "Factura electrónica por WhatsApp"),
        ("IMPRESA", "Factura impresa"),
    ]

    metodo_facturacion = forms.ChoiceField(
        choices=METODO_FACTURACION_OPCIONES,
        required=False,
        label="Preferencia de facturación",
    )

    estado_civil = forms.ChoiceField(
        choices=ESTADOS_CIVILES,
        required=False,
        label="Estado civil",
    )

    family_diabetes = forms.BooleanField(required=False)
    family_hypertension = forms.BooleanField(required=False)
    family_asthma = forms.BooleanField(required=False)
    family_heart_disease = forms.BooleanField(required=False)
    family_cancer = forms.BooleanField(required=False)
    family_mental_health = forms.BooleanField(required=False)

    class Meta:
        model = Paciente
        fields = [
            "cedula", "foto_perfil", "nombres", "apellidos", "fecha_nacimiento", "genero",
            "estado_civil", "direccion", "ciudad", "provincia",
            "correo", "telefono", "telefono_alternativo", "contacto_preferido",
            "contacto_emergencia", "relacion_emergencia", "telefono_emergencia",
            "correo_emergencia", "tipo_sangre", "altura_cm", "peso_kg",
            "alergias", "medicamentos_actuales", "condiciones_cronicas",
            "cirugias_previas", "hospitalizaciones", "antecedentes_familiares",
            "tabaquismo", "consumo_alcohol", "consumo_drogas", "frecuencia_ejercicio",
            "habitos_dieteticos",
            "tipo_identificacion_facturacion", "identificacion_facturacion",
            "nombre_facturacion", "correo_facturacion",
            "metodo_facturacion",
            "pago_efectivo", "pago_tarjeta", "pago_transferencia",
            "pago_deposito", "pago_cheque", "pago_otros", "pago_online",
            "profesional", "estado", "observaciones",
        ]
        widgets = {
            "cedula": forms.TextInput(attrs={"maxlength": "10", "inputmode": "numeric", "autocomplete": "off", "placeholder": "Ingrese la cédula"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "direccion": forms.Textarea(attrs={"rows": 3}),
            "identificacion_facturacion": forms.TextInput(attrs={
                "placeholder": "Ingrese el número de identificación",
                "maxlength": "13",
                "inputmode": "numeric",
            }),
            "nombre_facturacion": forms.TextInput(attrs={
                "placeholder": "Ingrese el nombre o razón social",
            }),
            "correo_facturacion": forms.EmailInput(attrs={
                "placeholder": "Ingrese el correo para recibir la factura",
            }),
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

    def clean_antecedentes_familiares(self):
        notes = (self.cleaned_data.get("antecedentes_familiares") or "").strip()
        history = []
        labels = [
            ("family_diabetes", "Diabetes"),
            ("family_hypertension", "Hipertensión"),
            ("family_asthma", "Asma"),
            ("family_heart_disease", "Enfermedad cardíaca"),
            ("family_cancer", "Cáncer"),
            ("family_mental_health", "Condiciones de salud mental"),
        ]
        for field_name, label in labels:
            if self.cleaned_data.get(field_name):
                history.append(label)

        if history:
            selected = "Antecedentes familiares seleccionados: " + ", ".join(history)
            return f"{selected}\n{notes}".strip()

        return notes

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
