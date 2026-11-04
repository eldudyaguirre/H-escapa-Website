import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings


def _fernet():
    # SECRET_KEY debe permanecer estable y protegida para poder descifrar los datos.
    material = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(material))


def cifrar_dato(valor: bytes) -> bytes:
    return _fernet().encrypt(valor)


def descifrar_dato(valor: bytes) -> bytes:
    return _fernet().decrypt(valor)
