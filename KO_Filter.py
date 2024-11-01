# Leer y procesar el archivo de texto con especies y KOs asociados
def find_species_with_min_kos_and_fixed_ko(file_name, kos_list, min_kos=3, fixed_ko=None):
    """
    Encuentra especies que contienen un número mínimo de KOs de una lista especificada y un KO fijo opcional.

    Args:
        file_name (str): Nombre del archivo de entrada que contiene datos de especies y KOs.
        kos_list (set): Conjunto de identificadores de KOs de interés.
        min_kos (int): Número mínimo de KOs que una especie debe tener de la lista especificada (default: 3).
        fixed_ko (str): KO fijo que cada especie debe tener para ser incluida en los resultados.

    Returns:
        list: Especies que cumplen con los criterios de selección.
    """
    matching_species = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Dividir la línea en palabras, siendo las primeras KOs y la última el nombre de la especie
            parts = line.split()
            ko_set = set(parts[:-1])  # Todos los KOs de la línea (excluyendo el último elemento, que es la especie)
            species = parts[-1]  # El último elemento es el nombre de la especie

            # Verificar si el KO fijo está presente
            if fixed_ko and fixed_ko not in ko_set:
                continue  # Si no tiene el KO fijo, pasar a la siguiente especie

            # Encuentra los KOs coincidentes con la lista de KOs
            matching_kos = ko_set.intersection(kos_list)
            
            # Verificar si tiene al menos 'min_kos' KOs coincidentes
            if len(matching_kos) >= min_kos:
                matching_species.append(line.strip())  # Guardar la línea completa si cumple con los criterios

    return matching_species

# Leer la lista de KOs de interés desde un archivo de texto
def load_kos_from_file(file_path):
    """
    Carga una lista de KOs desde un archivo de texto.

    Args:
        file_path (str): Ruta del archivo de texto con un KO por línea.

    Returns:
        set: Conjunto de KOs leídos del archivo.
    """
    kos_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            kos_set.add(line.strip())  # Agregar cada KO, eliminando espacios en blanco
    return kos_set

# Cargar la lista de KOs desde un archivo de texto proporcionado por el usuario
kos_file = input("Ingrese el nombre del archivo que contiene la lista de KOs (un KO por línea): ")
kos_list = load_kos_from_file(kos_file)

# Definir el KO fijo que todas las especies deben tener
fixed_ko = input("Ingrese el KO fijo requerido (o presione Enter para omitir): ").strip() or None

# Solicitar archivo de entrada y número mínimo de KOs, y ejecutar la búsqueda
file_name = input("Ingrese el nombre del archivo de entrada con los datos de especies y KOs: ")
min_kos = int(input("Ingrese el número mínimo de KOs que una especie debe tener de la lista: "))
matching_species = find_species_with_min_kos_and_fixed_ko(file_name, kos_list, min_kos, fixed_ko)

# Imprimir o guardar las especies coincidentes junto con el contador
species_count = len(matching_species)  # Contar cuántas especies coinciden con los criterios

# Imprimir el resultado en consola
if species_count > 0:
    print(f"Número de coincidencias con al menos {min_kos} KOs de los especificados y el KO fijo '{fixed_ko}': {species_count}")
    print("Lista de coincidencias:")
    for line in matching_species:
        print(line)  # Imprime la línea completa original
else:
    print(f"No se encontraron especies con al menos {min_kos} KOs de los especificados y el KO fijo '{fixed_ko}'.")

# Guardar el resultado en un archivo .txt con las líneas originales
output_file = input("Ingrese el nombre del archivo de salida para guardar los resultados: ")
with open(output_file, 'w') as output:
    output.write(f"Número de especies con al menos {min_kos} KOs de los especificados y el KO fijo '{fixed_ko}': {species_count}\n")
    if species_count > 0:
        output.write("Lista de especies:\n")
        for line in matching_species:
            output.write(line + '\n')  # Guardar la línea completa tal cual estaba
    else:
        output.write(f"No se encontraron especies con al menos {min_kos} KOs de los especificados y el KO fijo '{fixed_ko}'.\n")

print(f"Los resultados se guardaron en '{output_file}'")
