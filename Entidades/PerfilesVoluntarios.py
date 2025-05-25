class PerfilesVoluntarios:
    def __init__(self):
        self.id: int = 0
        self.usuario: int = 0
        self.experiencia: str = None
        self.disponibilidad: str = None
        self.telefono: str = None
        self.direccion: str = None

    def GetId(self):
        return self.id

    def SetId(self, id):
        self.id = id

    def GetUsuario(self):
        return self.usuario

    def SetUsuario(self, usuario):
        self.usuario = usuario

    def GetExperiencia(self):
        return self.experiencia

    def SetExperiencia(self, experiencia):
        self.experiencia = experiencia

    def GetDisponibilidad(self):
        return self.disponibilidad

    def SetDisponibilidad(self, disponibilidad):
        self.disponibilidad = disponibilidad

    def GetTelefono(self):
        return self.telefono

    def SetTelefono(self, telefono):
        self.telefono = telefono

    def GetDireccion(self):
        return self.direccion

    def SetDireccion(self, direccion):
        self.direccion = direccion
