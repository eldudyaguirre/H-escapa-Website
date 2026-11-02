# Google Meet en H-Escapa

## Arquitectura

H-Escapa crea una reunión única de Google Meet por cada cita virtual mediante Google Calendar API. La cuenta de Google autorizada es la organizadora de los eventos; el paciente y el profesional reciben las invitaciones de Calendar y el paciente recibe además un correo de acceso privado de H-Escapa.

El enlace de Meet se guarda en la cita junto con el identificador del evento de Google Calendar. Si se vuelve a enviar la invitación, H-Escapa actualiza el evento existente y conserva la misma reunión. Si se reprograma la cita, también se actualiza el evento. Si se cancela la cita o se cambia de virtual a presencial, H-Escapa intenta cancelar el evento de Google Calendar y notifica a los invitados.

El enlace privado del paciente contiene un token aleatorio; en la base de datos se guarda únicamente su hash. Al reenviar la invitación se invalida el enlace privado anterior. El paciente puede acceder sin tener una cuenta de usuario en H-Escapa. Google Meet puede solicitar que el organizador admita a invitados externos según la configuración de la cuenta.

## Requisitos en Google Cloud

1. Utiliza un proyecto de Google Cloud para H-Escapa.
2. En **APIs y servicios → Biblioteca**, habilita **Google Calendar API**.
3. Configura la pantalla de consentimiento OAuth. Agrega como usuario de prueba la cuenta de Google que organizará las reuniones si la aplicación permanece en modo de pruebas.
4. En **Credenciales**, crea un **ID de cliente OAuth 2.0** de tipo **Aplicación web**.
5. Agrega esta URI autorizada de redireccionamiento, exactamente como está escrita:

   `https://h-escapa.com/google-calendar/oauth/callback/`

   Si el dominio canónico de la instalación cambia, actualiza tanto esta URI en Google Cloud como `GOOGLE_CALENDAR_REDIRECT_URI` en el servidor.

La cuenta de Google que autorice H-Escapa será la propietaria de los eventos que se creen en su calendario principal. Conviene usar una cuenta institucional dedicada a las citas, no una cuenta personal de un profesional.

## Variables del servidor

En el archivo `.env` de la instalación de H-Escapa, configura:

```dotenv
GOOGLE_CALENDAR_CLIENT_ID=tu-cliente-oauth.apps.googleusercontent.com
GOOGLE_CALENDAR_CLIENT_SECRET=tu-secreto-oauth
GOOGLE_CALENDAR_REDIRECT_URI=https://h-escapa.com/google-calendar/oauth/callback/
```

No agregues manualmente `GOOGLE_CALENDAR_REFRESH_TOKEN`: H-Escapa lo guardará en el archivo `.env` después de que el administrador complete el consentimiento de Google. El archivo `.env` no debe subirse a GitHub ni compartirse.

El usuario de Windows que ejecuta el servicio Django debe tener permiso de escritura en el archivo `.env` para que la autorización pueda persistirse. Reinicia el servicio si agregas o cambias las credenciales del cliente OAuth.

## Conectar la cuenta desde H-Escapa

1. Ejecuta las migraciones: `python manage.py migrate`.
2. Inicia sesión en H-Escapa con el usuario administrador.
3. Abre **Citas → Consultas virtuales**.
4. Pulsa **Conectar Google**.
5. Selecciona la cuenta institucional de Google y acepta el permiso para administrar eventos del calendario.
6. Al regresar a H-Escapa, el módulo mostrará **Google Calendar conectado**.

La autorización solicita el alcance `https://www.googleapis.com/auth/calendar.events`, utilizado para crear, actualizar y cancelar los eventos de las consultas.

## Flujo de uso

1. Registra una cita y selecciona modalidad **Virtual**.
2. Abre el detalle de la cita y pulsa **Crear Meet y enviar invitación**.
3. H-Escapa crea el evento privado y solicita a Google una conferencia Meet única.
4. Cuando Google confirma que el enlace está listo, se invita al paciente y al profesional desde Google Calendar. También se envía al paciente un correo de H-Escapa con su enlace privado de acceso.
5. El profesional entra desde **Ingresar a Google Meet** en el detalle de la cita. El paciente abre el enlace privado recibido por correo.
6. El acceso desde H-Escapa se habilita desde 30 minutos antes de la cita y hasta 30 minutos después de la hora prevista de finalización.

La generación de la conferencia puede tardar unos segundos. Mientras Google la procesa, H-Escapa conserva el identificador del evento y permite volver a comprobarlo sin crear otra reunión. Las invitaciones de Calendar se envían después de que exista el enlace Meet.

## Seguridad y privacidad

- El evento usa un título genérico: **Consulta virtual H-Escapa**. No se agregan motivos de consulta ni datos clínicos a la descripción del calendario.
- El evento se crea con visibilidad privada y sin permitir que los invitados modifiquen o reenvíen la invitación a otras personas.
- Cada cita tiene un identificador y una conferencia Meet propios. No se reutiliza el enlace de otra cita.
- El profesional solo puede abrir la consulta si es el profesional asignado o un superusuario.
- El paciente solo puede abrir la página de acceso con el token privado que recibió por correo.
- El token no se guarda en texto claro en la base de datos.
- H-Escapa no graba ni almacena audio o video. La llamada ocurre en Google Meet.
- Los enlaces se abren en una pestaña nueva de Google Meet; no se incrustan dentro de H-Escapa.

## Nota sobre el estado de publicación OAuth

Si la pantalla de consentimiento es de tipo externo y la aplicación permanece en estado **Testing**, Google limita la duración de los refresh tokens para estos permisos y puede requerir volver a autorizar la cuenta cada siete días. Para operación continua, revisa el estado de publicación y los requisitos de verificación de OAuth de Google. Si la organización utiliza Google Workspace, el administrador puede evaluar configurar la aplicación como interna, según sus políticas.

Antes de atender pacientes reales, realiza una prueba con una cita virtual, dos direcciones de correo y dos dispositivos. Comprueba la invitación de Calendar, el correo privado, el acceso desde el teléfono y la cancelación/reprogramación de la cita.
