from django import forms

from .models import Cita, Especialidad, Paciente, Profesional, Post, CategoriaBlog, EtiquetaBlog

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
            "recibir_recordatorios_citas", "recibir_notificaciones_resultados",
            "recibir_notificaciones_recetas", "recibir_boletin_novedades",
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
            "profesional", "observaciones",
        ]
        widgets = {
            "cedula": forms.TextInput(attrs={"maxlength": "10", "inputmode": "numeric", "autocomplete": "off", "placeholder": "Ingrese la cédula"}),
            "fecha_nacimiento": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
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
        self.fields["fecha_nacimiento"].input_formats = ["%Y-%m-%d"]
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


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ["nombre", "activa"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ej.: Psicología Infantil",
                "maxlength": "100",
            }),
        }


class ProfesionalForm(forms.Form):
    foto = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"accept":"image/jpeg,image/png,image/webp"}))
    cedula = forms.CharField(label="Cédula", max_length=10, required=False, widget=forms.TextInput(attrs={"maxlength":"10","inputmode":"numeric","placeholder":"10 dígitos"}))
    nombre = forms.CharField(label="Nombres", max_length=100, widget=forms.TextInput(attrs={"placeholder":"Ingrese los nombres"}))
    apellido = forms.CharField(label="Apellidos", max_length=100, widget=forms.TextInput(attrs={"placeholder":"Ingrese los apellidos"}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={"type":"date"}))
    genero = forms.ChoiceField(label="Género", required=False, choices=[("", "Seleccione género")] + Profesional.GENEROS)
    telefono = forms.CharField(label="Teléfono", max_length=30, required=False, widget=forms.TextInput(attrs={"placeholder":"Ej.: 099 999 9999"}))
    email = forms.EmailField(label="Correo electrónico", required=True, widget=forms.EmailInput(attrs={"placeholder":"profesional@correo.com"}))
    direccion = forms.CharField(label="Dirección", max_length=250, required=False, widget=forms.TextInput(attrs={"autocomplete":"street-address"}))
    ciudad = forms.CharField(label="Ciudad", max_length=100, required=False, widget=forms.TextInput(attrs={"autocomplete":"address-level2"}))
    provincia = forms.CharField(label="Provincia", max_length=100, required=False, widget=forms.TextInput(attrs={"autocomplete":"off"}))
    codigo_postal = forms.CharField(label="Código postal", max_length=20, required=False, widget=forms.TextInput(attrs={"inputmode":"numeric", "autocomplete":"postal-code"}))
    pais = forms.CharField(label="País", max_length=100, required=False, initial="Ecuador", widget=forms.TextInput(attrs={"autocomplete":"country-name"}))
    contacto_emergencia_nombre = forms.CharField(label="Contacto de emergencia", max_length=150, required=False)
    contacto_emergencia_telefono = forms.CharField(label="Teléfono de emergencia", max_length=30, required=False)
    contacto_emergencia_relacion = forms.CharField(label="Relación", max_length=80, required=False)
    profesion = forms.CharField(label="Profesión", max_length=150, required=False, widget=forms.TextInput(attrs={"placeholder":"Ej.: Psicólogo"}))
    especialidad = forms.ModelChoiceField(label="Especialidad", queryset=Especialidad.objects.none(), empty_label="Seleccione una especialidad")
    especializacion = forms.CharField(label="Especialización", max_length=150, required=False)
    titulo = forms.CharField(label="Título / certificación", max_length=150, required=False)
    institucion_titulo = forms.CharField(label="Institución", max_length=200, required=False)
    anio_titulo = forms.IntegerField(label="Año de titulación", required=False, min_value=1900, max_value=2100)
    tipo_licencia = forms.CharField(label="Tipo de licencia", max_length=150, required=False)
    numero_licencia = forms.CharField(label="Número de licencia", max_length=100, required=False)
    fecha_emision_licencia = forms.DateField(label="Fecha de emisión", required=False, widget=forms.DateInput(attrs={"type":"date"}))
    fecha_vencimiento_licencia = forms.DateField(label="Fecha de vencimiento", required=False, widget=forms.DateInput(attrs={"type":"date"}))
    biografia = forms.CharField(label="Biografía / descripción", required=False, widget=forms.Textarea(attrs={"rows":4}))
    codigo_empleado = forms.CharField(label="Código de empleado", max_length=50, required=False)
    tipo_contrato = forms.ChoiceField(label="Tipo de contrato", required=False, choices=[("", "Seleccione tipo")] + Profesional.TIPOS_CONTRATO)
    fecha_ingreso = forms.DateField(label="Fecha de ingreso", required=False, widget=forms.DateInput(attrs={"type":"date"}))
    username = forms.CharField(label="Usuario de acceso", max_length=150, widget=forms.TextInput(attrs={"placeholder":"Ej.: jgarcia"}))
    password1 = forms.CharField(label="Contraseña", min_length=8, widget=forms.PasswordInput(attrs={"placeholder":"Mínimo 8 caracteres"}))
    password2 = forms.CharField(label="Confirmar contraseña", min_length=8, widget=forms.PasswordInput(attrs={"placeholder":"Repita la contraseña"}))
    activo = forms.BooleanField(label="Profesional activo", required=False, initial=True)
    forzar_cambio_clave = forms.BooleanField(label="Forzar cambio de contraseña", required=False, initial=True)
    dos_factores = forms.BooleanField(label="Autenticación de dos factores", required=False, initial=False)
    rol_sistema = forms.ChoiceField(
        label="Rol del sistema",
        choices=[
            ("ADMINISTRADOR", "Administrador"),
            ("GESTOR", "Gestor"),
            ("PROFESIONAL", "Profesional"),
            ("RECEPCION", "Recepción"),
            ("PERSONAL", "Personal"),
        ],
        initial="PROFESIONAL",
        widget=forms.RadioSelect,
    )
    permisos = forms.MultipleChoiceField(
        label="Permisos de módulos",
        required=False,
        choices=[
            ("pacientes_view", "Pacientes · Ver"),
            ("pacientes_add", "Pacientes · Agregar"),
            ("pacientes_change", "Pacientes · Editar"),
            ("pacientes_delete", "Pacientes · Eliminar"),
            ("citas_view", "Citas · Ver"),
            ("citas_add", "Citas · Agregar"),
            ("citas_change", "Citas · Editar"),
            ("citas_delete", "Citas · Eliminar"),
            ("profesionales_view", "Profesionales · Ver"),
            ("profesionales_add", "Profesionales · Agregar"),
            ("profesionales_change", "Profesionales · Editar"),
            ("profesionales_delete", "Profesionales · Eliminar"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["especialidad"].queryset = Especialidad.objects.filter(activa=True).order_by("nombre")

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula", "").strip()
        if cedula and (not cedula.isdigit() or len(cedula) != 10):
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
        return cedula

    def clean_username(self):
        from django.contrib.auth import get_user_model
        username = self.cleaned_data["username"].strip()
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ese usuario ya existe.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") and cleaned_data.get("password2") and cleaned_data["password1"] != cleaned_data["password2"]:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data


class ContactoForm(forms.Form):
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    mensaje = forms.CharField(max_length=5000, required=True, widget=forms.Textarea)


class AgendamientoForm(forms.Form):
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=30, required=True)
    servicio = forms.CharField(max_length=100, required=True)
    fecha = forms.DateField(required=True)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "titulo", "resumen", "contenido", "imagen_destacada",
            "categoria", "etiquetas", "estado",
            "meta_titulo", "meta_descripcion",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "blog-input",
                "placeholder": "Ej.: Cómo manejar la ansiedad en el día a día",
                "maxlength": "200",
            }),
            "resumen": forms.Textarea(attrs={
                "class": "blog-input",
                "rows": 3,
                "placeholder": "Un resumen breve que aparecerá en la portada del blog.",
            }),
            "contenido": forms.Textarea(attrs={
                "class": "blog-input blog-content-editor",
                "rows": 18,
                "placeholder": "Escribe aquí el contenido del artículo...",
            }),
            "imagen_destacada": forms.ClearableFileInput(attrs={
                "class": "blog-input",
                "accept": "image/jpeg,image/png,image/webp",
            }),
            "categoria": forms.Select(attrs={"class": "blog-input"}),
            "etiquetas": forms.SelectMultiple(attrs={
                "class": "blog-input",
                "size": "5",
            }),
            "estado": forms.Select(attrs={"class": "blog-input"}),
            "meta_titulo": forms.TextInput(attrs={
                "class": "blog-input",
                "placeholder": "Título para buscadores (opcional)",
                "maxlength": "200",
            }),
            "meta_descripcion": forms.Textarea(attrs={
                "class": "blog-input",
                "rows": 2,
                "placeholder": "Descripción para buscadores (opcional)",
                "maxlength": "300",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = CategoriaBlog.objects.filter(activa=True).order_by("nombre")
        self.fields["categoria"].required = False
        self.fields["etiquetas"].queryset = EtiquetaBlog.objects.all().order_by("nombre")
        self.fields["etiquetas"].required = False
