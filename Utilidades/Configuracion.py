import pyodbc

class Configuracion:
    strConnection: str = """
		Driver={MySQL ODBC 9.2 Unicode Driver};
		Server=localhost;
		Database=caminatas_comunitarias;
		PORT=3306;
		user=user_ptyhon;
		password=Clas3s1Nt2024_!""";

    @staticmethod
    def obtener_conexion():
        return pyodbc.connect(Configuracion.strConnection)