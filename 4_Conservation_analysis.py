# Importar módulo necesario para manejo de archivos
import os

# Función para leer especies desde un archivo
def read_species(filename):
    """
    Lee una lista de especies desde un archivo de texto y devuelve un conjunto con los nombres de especies.

    Args:
        filename (str): Ruta del archivo que contiene una lista de nombres de especies, cada uno en una línea.

    Returns:
        set: Conjunto de nombres de especies leídos del archivo.
    """
    with open(filename, 'r') as f:
        return set(line.strip() for line in f)

# Leer el archivo principal con la lista completa de especies
main_species_file = input("Ingrese la ruta del archivo de la lista principal de especies: ")
main_species = sorted(read_species(main_species_file))  # Ordenar alfabéticamente para salida ordenada

# Solicitar al usuario las rutas de archivo para cada grupo de especies
species_files = {
    'SigE_KO': input("Ingrese la ruta del archivo para 'SigE_KO': "),
    'SigE_motivo': input("Ingrese la ruta del archivo para 'SigE_motivo': "),
    'SpoIIIAA': input("Ingrese la ruta del archivo para 'SpoIIIAA': "),
    'SpoIIID_KO': input("Ingrese la ruta del archivo para 'SpoIIID_KO': "),
    'SpoIIID_motivo': input("Ingrese la ruta del archivo para 'SpoIIID_motivo': ")
}

# Leer los archivos de cada grupo y almacenar las especies presentes en cada archivo
species_dict = {key: read_species(file) for key, file in species_files.items()}

# Inicializar contadores para cada grupo para llevar registro de las especies conservadas
conservacion = {key: 0 for key in species_files.keys()}

# Nombre del archivo de salida donde se guardará el resultado
output_file = input("Ingrese el nombre del archivo de salida para guardar los resultados: ")

# Escribir el encabezado y los datos de conservación en el archivo de salida
with open(output_file, 'w') as f:
    # Escribir el encabezado con los nombres de cada grupo
    f.write('ID\tSigE_KO\tSigE_motivo\tSpoIIIAA\tSpoIIID_KO\tSpoIIID_motivo\n')
    
    # Para cada especie en la lista principal, verificar su presencia en cada grupo y registrar el resultado
    for species in main_species:
        row = [species]
        for key in species_dict.keys():
            # Comprobar si la especie está en el grupo actual
            if species in species_dict[key]:
                row.append('1')  # Agregar '1' si la especie está presente
                conservacion[key] += 1  # Aumentar el contador para el grupo correspondiente
            else:
                row.append('0')  # Agregar '0' si la especie no está presente
        f.write('\t'.join(row) + '\n')  # Escribir la línea de datos en el archivo

# Mostrar los resultados de conservación en la consola
print("Conservación por cada grupo:")
for group, count in conservacion.items():
    print(f"{group}: {count} especies conservadas")
