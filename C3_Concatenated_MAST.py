import subprocess
import os

# Función para leer los IDs de especies desde un archivo
def read_species_ids(file_path):
    """
    Lee los IDs de especies desde un archivo de texto.

    Args:
        file_path (str): Ruta del archivo con los IDs de las especies, cada uno en una línea.

    Returns:
        list: Lista de IDs de especies.
    """
    with open(file_path, 'r') as f:
        species_ids = [line.strip() for line in f]
    return species_ids

# Función para ejecutar MAST en cada especie con su propio directorio de salida
def run_mast_for_species(meme_file, species_ids, species_folder, output_base_folder):
    """
    Ejecuta MAST para cada especie, utilizando archivos específicos y generando resultados en directorios separados.

    Args:
        meme_file (str): Ruta del archivo de motivos en formato MEME.
        species_ids (list): Lista de IDs de especies.
        species_folder (str): Carpeta que contiene los archivos .ur de cada especie.
        output_base_folder (str): Carpeta base donde se crearán subcarpetas con los resultados de MAST.
    """
    for species_id in species_ids:
        species_ur_file = os.path.join(species_folder, f'{species_id}.ur')
        output_species_folder = os.path.join(output_base_folder, f'{species_id}_mast_out')

        if os.path.exists(species_ur_file):
            print(f"Ejecutando MAST para {species_id}...")

            # Crear el directorio de salida para la especie si no existe
            os.makedirs(output_species_folder, exist_ok=True)

            # Ejecutar el comando MAST con el archivo meme.txt y el archivo .ur de la especie
            subprocess.run(
                ['mast', meme_file, species_ur_file, '-oc', output_species_folder],
                stdout=subprocess.PIPE,  # Captura la salida estándar
                stderr=subprocess.PIPE  # Captura los errores
            )
        else:
            print(f"Advertencia: El archivo {species_ur_file} no existe. Saltando...")

# Solicitar parámetros de entrada al usuario
meme_file = input("Ingrese la ruta del archivo de motivos en formato MEME: ")
species_file = input("Ingrese la ruta del archivo con los IDs de las especies: ")
species_folder = input("Ingrese la carpeta donde se encuentran los archivos .ur de las especies: ")
output_base_folder = input("Ingrese la carpeta base para los resultados de MAST: ")

# Leer los IDs de especies
species_ids = read_species_ids(species_file)

# Ejecutar MAST para cada especie y guardar los resultados en directorios separados
run_mast_for_species(meme_file, species_ids, species_folder, output_base_folder)

print("Ejecución de MAST completada. Los resultados se han guardado en directorios separados.")
