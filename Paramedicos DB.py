from pymongo import MongoClient
import hashlib

# Configuración de conexión a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017')  # Cambia esto según tu configuración
db = mongo_client["hospitales_db"]  # Base de datos
collection = db["ids_hospitales"]  # Colección


def verificardata(hospital_id, nombre_completo, nombre_hospital):
    """
    Verifica si los datos ya tienen un ID asociado en MongoDB.
    """
    query = {
        "hospital_id": hospital_id,
        "nombre_completo": nombre_completo,
        "nombre_hospital": nombre_hospital
    }
    result = collection.find_one(query)  # Busca un documento que coincida con los datos
    return result["_id"] if result else None


def genuid(hospital_id, nombre_completo, nombre_hospital):
    """
    Genera un ID único corto de 6 caracteres basado en un hash.
    Si los datos ya tienen un ID asociado, lanza un error.
    """
    # Verificar si los datos ya tienen un ID
    id_existente = verificardata(hospital_id, nombre_completo, nombre_hospital)
    if id_existente:
        raise ValueError(f"Error: Los datos ya tienen un ID asociado")

    # Concatenar los datos
    base_string = f"{hospital_id}{nombre_completo}{nombre_hospital}"

    # Crear un hash MD5 y truncar los primeros 6 caracteres
    hash_id = hashlib.md5(base_string.encode()).hexdigest()[:6]

    # Comprobar si el ID ya existe en MongoDB
    while collection.find_one({"_id": hash_id}):  # Consulta por _id en MongoDB
        # Si el ID ya existe, genera un nuevo hash añadiendo un contador
        base_string += "1"
        hash_id = hashlib.md5(base_string.encode()).hexdigest()[:6]

    # Guardar los datos asociados en MongoDB
    datos = {
        "_id": hash_id,  # MongoDB usa "_id" como clave primaria
        "hospital_id": hospital_id,
        "nombre_completo": nombre_completo,
        "nombre_hospital": nombre_hospital
    }
    collection.insert_one(datos)  # Inserta el documento en la colección

    return hash_id


def obteneruid(hash_id):
    """
    Recupera los datos asociados a un ID único desde MongoDB.
    """
    result = collection.find_one({"_id": hash_id})  # Busca por _id
    if result:
        del result["_id"]  # Opcional: eliminar el _id del resultado si no se necesita
    return result


# Ejemplo de uso
if __name__ == "__main__":
    hospital_id = "H123"
    nombre_completo = "Wentur"
    nombre_hospital = "Hospital Central"

    try:
        # Generar ID único corto y almacenar datos
        short_id = genuid(hospital_id, nombre_completo, nombre_hospital)
        print(f"ID generado: {short_id}")
    except ValueError as e:
        print(e)

    # Recuperar datos por ID (opcional)
    datos = obteneruid(short_id) if 'short_id' in locals() else None
    if datos:
        print(f"Datos asociados: {datos}")

