import sqlite3

# Configuración de la base de datos
DATABASE = "libro_recetas.db"

def inicializar_db():
    """Crea la base de datos y la tabla si no existe."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            ingredientes TEXT NOT NULL,
            pasos TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def agregar_receta():
    """Agregar una nueva receta a la base de datos."""
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO recetas (nombre, ingredientes, pasos)
            VALUES (?, ?, ?)
        """, (nombre, ingredientes, pasos))
        conn.commit()
        print("✅ Receta agregada exitosamente.")
    except sqlite3.IntegrityError:
        print("❌ Ya existe una receta con ese nombre.")
    finally:
        conn.close()

def actualizar_receta():
    """Actualizar una receta existente."""
    nombre = input("Nombre de la receta a actualizar: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,))
    receta = cursor.fetchone()

    if receta:
        print("Receta encontrada:")
        print(f"Ingredientes: {receta[2]}")
        print(f"Pasos: {receta[3]}")

        nuevo_ingredientes = input("Nuevos ingredientes (dejar en blanco para no cambiar): ")
        nuevo_pasos = input("Nuevos pasos (dejar en blanco para no cambiar): ")

        nuevo_ingredientes = nuevo_ingredientes if nuevo_ingredientes else receta[2]
        nuevo_pasos = nuevo_pasos if nuevo_pasos else receta[3]

        cursor.execute("""
            UPDATE recetas
            SET ingredientes = ?, pasos = ?
            WHERE nombre = ?
        """, (nuevo_ingredientes, nuevo_pasos, nombre))
        conn.commit()
        print("✅ Receta actualizada exitosamente.")
    else:
        print("❌ No se encontró la receta especificada.")
    conn.close()

def eliminar_receta():
    """Eliminar una receta existente."""
    nombre = input("Nombre de la receta a eliminar: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,))
    receta = cursor.fetchone()

    if receta:
        cursor.execute("DELETE FROM recetas WHERE nombre = ?", (nombre,))
        conn.commit()
        print("✅ Receta eliminada exitosamente.")
    else:
        print("❌ No se encontró la receta especificada.")
    conn.close()

def ver_listado_recetas():
    """Mostrar el listado de todas las recetas."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM recetas")
    recetas = cursor.fetchall()
    conn.close()

    if recetas:
        print("📜 Listado de recetas:")
        for i, (nombre,) in enumerate(recetas, start=1):
            print(f"{i}. {nombre}")
    else:
        print("❌ No hay recetas disponibles.")

def buscar_receta():
    """Buscar los detalles de una receta específica."""
    nombre = input("Nombre de la receta a buscar: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,))
    receta = cursor.fetchone()
    conn.close()

    if receta:
        print(f"📖 Receta: {receta[1]}")
        print(f"Ingredientes: {receta[2]}")
        print(f"Pasos: {receta[3]}")
    else:
        print("❌ No se encontró la receta especificada.")

def menu():
    """Mostrar el menú principal y gestionar las opciones del usuario."""
    while True:
        print("\n=== Libro de Recetas ===")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_receta()
        elif opcion == "2":
            actualizar_receta()
        elif opcion == "3":
            eliminar_receta()
        elif opcion == "4":
            ver_listado_recetas()
        elif opcion == "5":
            buscar_receta()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    inicializar_db()
    menu()