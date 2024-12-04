import redis
import hashlib

# Configuración de conexión a KeyDB
keydb = redis.StrictRedis(
    host='localhost',  # Cambia a la IP o hostname de tu servidor KeyDB
    port=6379,  # Puerto de KeyDB
    db=1,
    decode_responses=True  # Para manejar strings en lugar de bytes
)


def verificardata(hospital_id, nombre_completo, nombre_hospital):
    """
    Verifica si los datos ya tienen un ID asociado en KeyDB.
    """
    for key in keydb.scan_iter():  # Escanea todas las claves en KeyDB
        # Verificar que la clave es del tipo 'hash'
        if keydb.type(key) != "hash":
            continue  # Si no es un hash, saltar a la siguiente clave

        datos = keydb.hgetall(key)  # Obtener los datos del hash
        if (datos.get("hospital_id") == hospital_id and
            datos.get("nombre_completo") == nombre_completo and
            datos.get("nombre_hospital") == nombre_hospital):
            return key  # Retorna el ID existente si encuentra una coincidencia
    return None


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

    # Comprobar si el ID ya existe en KeyDB
    while keydb.exists(hash_id):
        # Si el ID ya existe, genera un nuevo hash añadiendo un contador
        base_string += "1"
        hash_id = hashlib.md5(base_string.encode()).hexdigest()[:6]

    # Guardar los datos asociados en KeyDB
    datos = {
        "hospital_id": hospital_id,
        "nombre_completo": nombre_completo,
        "nombre_hospital": nombre_hospital
    }
    keydb.hset(hash_id, mapping=datos)  # Uso de hset en lugar de hmset

    return hash_id


def obteneruid(hash_id):
    """
    Recupera los datos asociados a un ID único desde KeyDB.
    """
    return keydb.hgetall(hash_id)


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
