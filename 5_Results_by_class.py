import csv
from collections import defaultdict

# Función para leer el archivo combinado de KOs y motivos
def read_combined_file(filename):
    """
    Lee un archivo combinado de datos de conservación de KOs y motivos.

    Parámetros:
        filename (str): Nombre del archivo de entrada que contiene los datos en formato tabular.

    Retorna:
        list: Lista de diccionarios donde cada diccionario representa una fila de datos,
              conteniendo la clase taxonómica, datos de KOs y motivos.
    """
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            taxonomic_class = row['KEGG Class']  # Clase taxonómica
            ko_data = {
                'SigE_KO': int(row['SigE_KO']),  # Conservación de KOs
                'SpoIIIAA_KO': int(row['SpoIIIAA_KO']),
                'SpoIIID_KO': int(row['SpoIIID_KO'])
            }
            motif_data = {
                'SigE_motivo': int(row['SigE_motivo']),  # Conservación de motivos
                'SpoIIID_motivo': int(row['SpoIIID_motivo'])
            }
            data.append({
                'taxonomic_class': taxonomic_class,
                'ko_data': ko_data,
                'motif_data': motif_data
            })
    return data

# Función para contar la conservación por cada clase, combinando KOs y motivos
def count_conservation_by_class(data):
    """
    Cuenta la conservación de KOs y motivos agrupados por clase taxonómica.

    Parámetros:
        data (list): Lista de diccionarios con los datos leídos del archivo.

    Retorna:
        dict: Diccionario que contiene la conservación total de KOs y motivos por cada clase taxonómica,
              junto con el conteo de especies.
    """
    conservation_by_class = defaultdict(lambda: {
        'SigE_KO': 0, 'SpoIIIAA_KO': 0, 'SpoIIID_KO': 0,
        'SigE_motivo': 0, 'SpoIIID_motivo': 0, 'species_count': 0
    })
    
    for entry in data:
        tax_class = entry['taxonomic_class']  # Clase taxonómica actual
        # Sumar la conservación de KOs y motivos
        conservation_by_class[tax_class]['SigE_KO'] += entry['ko_data']['SigE_KO']
        conservation_by_class[tax_class]['SpoIIIAA_KO'] += entry['ko_data']['SpoIIIAA_KO']
        conservation_by_class[tax_class]['SpoIIID_KO'] += entry['ko_data']['SpoIIID_KO']
        conservation_by_class[tax_class]['SigE_motivo'] += entry['motif_data']['SigE_motivo']
        conservation_by_class[tax_class]['SpoIIID_motivo'] += entry['motif_data']['SpoIIID_motivo']
        
        conservation_by_class[tax_class]['species_count'] += 1  # Incrementar el conteo de especies

    return conservation_by_class

# Función para escribir los resultados combinados en un solo archivo de salida con porcentajes de conservación
def write_conservation_output(conservation_by_class, output_filename):
    """
    Escribe los resultados de conservación en un archivo de salida, incluyendo porcentajes de conservación.

    Parámetros:
        conservation_by_class (dict): Diccionario con los datos de conservación por clase.
        output_filename (str): Nombre del archivo donde se guardarán los resultados.
    """
    with open(output_filename, 'w') as f_out:
        f_out.write('Class\tSigE KO Conserved\tSpoIIIAA KO Conserved\tSpoIIID KO Conserved\tSigE Motif Conserved\tSpoIIID Motif Conserved\tSpecies Count\tSigE KO % by Class\tSpoIIIAA KO % by Class\tSpoIIID KO % by Class\tSigE Motif % by Class\tSpoIIID Motif % by Class\tSigE KO % Total\tSpoIIIAA KO % Total\tSpoIIID KO % Total\tSigE Motif % Total\tSpoIIID Motif % Total\n')
        total_species = sum(data['species_count'] for data in conservation_by_class.values())

        for tax_class, data in conservation_by_class.items():
            species_count = data['species_count']
            
            # Porcentajes de conservación por clase
            sigE_ko_pct_class = (data['SigE_KO'] / species_count * 100) if species_count else 0
            spoIIIAA_ko_pct_class = (data['SpoIIIAA_KO'] / species_count * 100) if species_count else 0
            spoIIID_ko_pct_class = (data['SpoIIID_KO'] / species_count * 100) if species_count else 0
            sigE_motif_pct_class = (data['SigE_motivo'] / species_count * 100) if species_count else 0
            spoIIID_motif_pct_class = (data['SpoIIID_motivo'] / species_count * 100) if species_count else 0

            # Porcentajes de conservación respecto al total de especies
            sigE_ko_pct_total = (data['SigE_KO'] / total_species * 100) if total_species else 0
            spoIIIAA_ko_pct_total = (data['SpoIIIAA_KO'] / total_species * 100) if total_species else 0
            spoIIID_ko_pct_total = (data['SpoIIID_KO'] / total_species * 100) if total_species else 0
            sigE_motif_pct_total = (data['SigE_motivo'] / total_species * 100) if total_species else 0
            spoIIID_motif_pct_total = (data['SpoIIID_motivo'] / total_species * 100) if total_species else 0

            # Escribir datos de conservación por clase en el archivo
            f_out.write(f"{tax_class}\t{data['SigE_KO']}\t{data['SpoIIIAA_KO']}\t{data['SpoIIID_KO']}\t{data['SigE_motivo']}\t{data['SpoIIID_motivo']}\t{species_count}\t{sigE_ko_pct_class:.2f}\t{spoIIIAA_ko_pct_class:.2f}\t{spoIIID_ko_pct_class:.2f}\t{sigE_motif_pct_class:.2f}\t{spoIIID_motif_pct_class:.2f}\t{sigE_ko_pct_total:.2f}\t{spoIIIAA_ko_pct_total:.2f}\t{spoIIID_ko_pct_total:.2f}\t{sigE_motif_pct_total:.2f}\t{spoIIID_motif_pct_total:.2f}\n")
        
        # Calcular y escribir los totales
        total_sigE_KO = sum(data['SigE_KO'] for data in conservation_by_class.values())
        total_spoIIIAA_KO = sum(data['SpoIIIAA_KO'] for data in conservation_by_class.values())
        total_spoIIID_KO = sum(data['SpoIIID_KO'] for data in conservation_by_class.values())
        total_sigE_motivo = sum(data['SigE_motivo'] for data in conservation_by_class.values())
        total_spoIIID_motivo = sum(data['SpoIIID_motivo'] for data in conservation_by_class.values())
        
        # Escribir totales al final del archivo
        f_out.write(f'\nTotal\t{total_sigE_KO}\t{total_spoIIIAA_KO}\t{total_spoIIID_KO}\t{total_sigE_motivo}\t{total_spoIIID_motivo}\n')

# Solicitar archivos de entrada y salida al usuario
input_combined_file = input("Ingrese el nombre del archivo combinado de KOs y motivos (ejemplo: 'Dataframe.txt'): ")  # Archivo de entrada
output_combined_file = input("Ingrese el nombre del archivo de salida para los resultados combinados (ejemplo: 'conservation_combined.txt'): ")  # Archivo de salida

# Leer los datos combinados del archivo
combined_data = read_combined_file(input_combined_file)

# Contar la conservación por clase, combinando KOs y motivos
conservation_by_class_combined = count_conservation_by_class(combined_data)

# Escribir los resultados en un archivo de salida único con porcentajes
write_conservation_output(conservation_by_class_combined, output_combined_file)

print("Conservación de KOs y motivos por clase completada. Los resultados se han guardado en el archivo de salida combinado.")
