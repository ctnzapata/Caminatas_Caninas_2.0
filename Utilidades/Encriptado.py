# En Utilidades/Encriptado.py

import os
import base64
from Crypto.Cipher import AES

class EncriptarAES:
    def __init__(self):
        self.secretKey = os.environ.get("AES_SECRET_KEY")
        if not self.secretKey:
            raise ValueError("No se encontró la clave secreta en el entorno (AES_SECRET_KEY).")
        self.secretKey = self.secretKey.encode('utf-8')
        if len(self.secretKey) not in [16, 24, 32]:
            raise ValueError("La clave debe tener 16, 24 o 32 bytes para AES.")

    def cifrar(self, texto: str) -> str:
        cipher = AES.new(self.secretKey, AES.MODE_GCM)
        ciphertext, authTag = cipher.encrypt_and_digest(texto.encode('utf-8'))
        datos = {
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "nonce": base64.b64encode(cipher.nonce).decode('utf-8'),
            "tag": base64.b64encode(authTag).decode('utf-8')
        }
        return f"{datos['ciphertext']}::{datos['nonce']}::{datos['tag']}"

    def decifrar(self, cifrado: str) -> str:
        ciphertext_b64, nonce_b64, tag_b64 = cifrado.split("::")
        ciphertext = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)

        cipher = AES.new(self.secretKey, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')
