# Videollamadas de H-Escapa

## Arquitectura

La aplicación integra Jitsi Meet mediante su IFrame API. Esta implementación está preparada para una **instancia propia de Jitsi Meet con autenticación JWT HS256**. No utiliza una sala pública compartida.

El profesional ingresa desde el detalle de la cita con su usuario del sistema. El paciente recibe por correo un enlace privado que acredita el acceso a esa cita. El backend valida la cita y emite un JWT de corta duración, restringido a una sala concreta.

## Configuración de H-Escapa

Define estas variables en el mismo entorno que utiliza el proceso Django (por ejemplo, el archivo `.env` que carga el servicio):

```dotenv
JITSI_DOMAIN=video.tu-dominio.com
JITSI_APP_ID=hescapa
JITSI_APP_SECRET=CAMBIA_POR_UN_SECRETO_LARGO_Y_ALEATORIO
```

- `JITSI_DOMAIN`: solo el nombre del dominio, sin `https://`, rutas ni barra final.
- `JITSI_APP_ID`: identificador de la aplicación; debe coincidir con `JWT_APP_ID` del servidor Jitsi.
- `JITSI_APP_SECRET`: secreto compartido; debe coincidir exactamente con `JWT_APP_SECRET` del servidor Jitsi.

Genera un secreto aleatorio desde PowerShell con:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

No guardes ese secreto en GitHub ni lo incluyas en capturas o correos.

## Configuración del servidor Jitsi

En el archivo de entorno de la instalación propia de Jitsi (por ejemplo, el `.env` de Docker Compose), configura la autenticación JWT:

```dotenv
ENABLE_AUTH=1
AUTH_TYPE=jwt
JWT_APP_ID=hescapa
JWT_APP_SECRET=EL_MISMO_SECRETO_CONFIGURADO_EN_H_ESCAPA
JWT_ACCEPTED_ISSUERS=hescapa
JWT_ACCEPTED_AUDIENCES=hescapa
JWT_ALLOW_EMPTY=0
JWT_SIGN_TYPE=HS256
ENABLE_GUESTS=0
```

Usa el mismo secreto en Jitsi y en H-Escapa. No habilites acceso anónimo si quieres que todos los participantes deban presentar un JWT. Reinicia o recrea los servicios Jitsi de acuerdo con el método de instalación para aplicar los cambios.

La instancia de Jitsi debe tener HTTPS y conectividad de medios configurada. En una instalación Docker estándar, revisa también el firewall y la publicación de puertos de Jitsi, especialmente UDP 10000. La aplicación carga `external_api.js` desde el dominio configurado.

## Flujo de uso

1. Registra una cita y selecciona modalidad **Virtual**.
2. Abre el detalle de la cita y pulsa **Enviar enlace al paciente**.
3. H-Escapa genera una sala exclusiva y manda el enlace al correo registrado del paciente.
4. El profesional asignado entra desde **Ingresar a la sala** en el detalle de la cita.
5. La sala se habilita desde 30 minutos antes y hasta 30 minutos después de la finalización prevista.

El enlace del paciente es una credencial privada: no debe reenviarse. En la base de datos se guarda su hash, no el token original. Volver a enviar la invitación invalida el enlace anterior. Cambiar fecha, hora o modalidad de la cita elimina la sala y revoca el enlace anterior.

## Requisitos y límites de esta primera versión

- El profesional debe tener una cuenta activa y asociada a la cita.
- El paciente debe tener un correo válido registrado. El enlace funciona sin una cuenta de paciente porque el portal actual no tiene autenticación de pacientes.
- La cámara y el micrófono requieren permisos del navegador y una conexión HTTPS.
- El backend no graba ni almacena audio o video. La configuración de grabación del servidor Jitsi también debe permanecer deshabilitada.
- Esta integración usa JWT HS256 de una instalación propia de Jitsi. No es la configuración JWT de Jitsi as a Service (JaaS); para JaaS se necesita adaptar el emisor JWT al tipo de credencial de ese servicio.
- Antes de usarla con pacientes reales, valida con una cita de prueba, dos dispositivos y cuentas de prueba. Revisa además las obligaciones de privacidad, consentimiento informado y protección de datos aplicables a teleconsulta.
