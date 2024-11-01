import re

# Función para cargar secuencias en formato FASTA
def load_fasta(filename):
    """
    Carga secuencias de un archivo en formato FASTA.

    Args:
        filename (str): Nombre del archivo FASTA.

    Returns:
        dict: Diccionario con identificadores de secuencia como claves y secuencias como valores.
    """
    sequences = {}
    with open(filename, 'r') as file:
        current_seq_id = None
        current_seq = []
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_seq_id:
                    sequences[current_seq_id] = ''.join(current_seq)
                current_seq_id = line[1:]  # Guardar el identificador sin el ">"
                current_seq = []
            else:
                current_seq.append(line)
        # Agregar la última secuencia
        if current_seq_id:
            sequences[current_seq_id] = ''.join(current_seq)
    return sequences

# Función para cargar motivos desde un archivo de texto
def load_motifs(filename):
    """
    Carga motivos desde un archivo de texto.

    Args:
        filename (str): Nombre del archivo de motivos.

    Returns:
        list: Lista de motivos leídos del archivo.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Función para buscar motivos en una secuencia y obtener posiciones (inicio y fin)
def find_motif_positions(sequence, motif):
    """
    Encuentra posiciones de un motivo en una secuencia.

    Args:
        sequence (str): Secuencia en la que buscar el motivo.
        motif (str): Motivo que se quiere buscar.

    Returns:
        list: Lista de tuplas con posiciones de inicio y fin del motivo.
    """
    return [(m.start(), m.start() + len(motif)) for m in re.finditer(f'(?={motif})', sequence)]

# Función para verificar si hay superposición entre dos motivos
def check_superposition(pos1, pos2):
    """
    Verifica si hay superposición entre dos posiciones de motivos.

    Args:
        pos1 (tuple): Posición de inicio y fin del primer motivo.
        pos2 (tuple): Posición de inicio y fin del segundo motivo.

    Returns:
        bool: True si hay superposición, False en caso contrario.
    """
    return pos1[0] < pos2[1] and pos1[1] > pos2[0]

# Solicitar los nombres de archivos de entrada al usuario
fasta_file = input("Ingrese el nombre del archivo de secuencias en formato FASTA: ")
motif_file1 = input("Ingrese el nombre del archivo con el primer conjunto de motivos: ")
motif_file2 = input("Ingrese el nombre del archivo con el segundo conjunto de motivos: ")

# Cargar secuencias y motivos desde los archivos
sequences = load_fasta(fasta_file)
motifs1 = load_motifs(motif_file1)
motifs2 = load_motifs(motif_file2)

# Convertir secuencias y motivos a minúsculas para evitar problemas de sensibilidad de mayúsculas/minúsculas
sequences = {seq_id: seq.lower() for seq_id, seq in sequences.items()}
motifs1 = [motif.lower() for motif in motifs1]
motifs2 = [motif.lower() for motif in motifs2]

# Solicitar nombres de archivos de salida al usuario
output_filename_with_superpositions = input("Ingrese el nombre del archivo de salida para secuencias con superposiciones: ")
output_filename_without_superpositions = input("Ingrese el nombre del archivo de salida para secuencias sin superposiciones: ")

# Abrir archivos de salida para guardar los resultados
with open(output_filename_with_superpositions, "w") as output_file_with, open(output_filename_without_superpositions, "w") as output_file_without:
    # Recorrer todas las secuencias
    for seq_id, seq in sequences.items():
        found_overlap = False  # Bandera para verificar si se encontró alguna superposición
        output_file_with.write(f"Secuencia '{seq_id}':\n")
        output_file_without.write(f"Secuencia '{seq_id}':\n")
        
        # Buscar posiciones de motivos del primer archivo en la secuencia actual
        motif_positions1 = {}
        for motif1 in motifs1:
            positions1 = find_motif_positions(seq, motif1)
            if positions1:
                motif_positions1[motif1] = positions1
        
        # Buscar posiciones de motivos del segundo archivo en la secuencia actual
        motif_positions2 = {}
        for motif2 in motifs2:
            positions2 = find_motif_positions(seq, motif2)
            if positions2:
                motif_positions2[motif2] = positions2

        # Verificar superposiciones entre todos los motivos de ambos archivos encontrados
        for motif1, positions1 in motif_positions1.items():
            for motif2, positions2 in motif_positions2.items():
                for pos1 in positions1:
                    for pos2 in positions2:
                        if check_superposition(pos1, pos2):
                            result = (f"  Superposición encontrada:\n"
                                      f"  Motivo 1 '{motif1}' en {pos1} y Motivo 2 '{motif2}' en {pos2}\n"
                                      f"  Secuencia solapada: {seq[min(pos1[0], pos2[0]):max(pos1[1], pos2[1])]}\n")
                            output_file_with.write(result)
                            found_overlap = True
        
        # Escribir en el archivo correspondiente según si hay superposición o no
        if not found_overlap:
            output_file_without.write(f"  No se encontraron superposiciones en la secuencia '{seq_id}'.\n")
        else:
            # Si se encontró alguna superposición, escribir la secuencia también en el archivo correspondiente
            output_file_with.write(f"Secuencia completa: {seq}\n\n")

print(f"Análisis completado. Los resultados se han guardado en '{output_filename_with_superpositions}' y '{output_filename_without_superpositions}'.")
