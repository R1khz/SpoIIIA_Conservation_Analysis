library(ggplot2)
library(reshape2)
library(showtext)
library(viridis)

# Configuración de la fuente Times New Roman
font_add(family = "Times New Roman", regular = "C:/Windows/Fonts/times.ttf")
showtext_auto()

# Leer el archivo CSV
# Parámetros:
#   file_path (str): Ruta del archivo CSV que contiene los datos de conservación de KOs y motivos.
#
# Retorna:
#   data.frame: Un marco de datos con las columnas renombradas y sin la fila "Total".
motifs_data <- read.csv("ruta.csv")

# Renombrar las columnas para que coincidan con tu archivo
colnames(motifs_data) <- c("Class", "SigE_KO", "SpoIIIAA_KO", "SpoIIID_KO", "SigE_Motivo", "SpoIIID_Motivo")

# Eliminar la fila "Total"
motifs_data <- motifs_data[motifs_data$Class != "Total", ]

# Crear el DataFrame para el Heatmap
# Este paso reorganiza los datos para su representación gráfica.
heatmap_data <- motifs_data[, c("Class", "SigE_KO", "SigE_Motivo", "SpoIIIAA_KO", "SpoIIID_KO", "SpoIIID_Motivo")]
heatmap_long <- melt(heatmap_data, id.vars = "Class", 
                     variable.name = "Gene", value.name = "Conservación")

# Generar el Heatmap
# Este bloque crea un gráfico de calor que representa la conservación de KOs y motivos.
ggplot(heatmap_long, aes(x = Gene, y = Class, fill = Conservación)) +
  geom_tile(color = "black", size = 0.5) +  
  geom_text(aes(label = Conservación, color = ifelse(Conservación > 150, "white", "black")), size = 4) +
  scale_fill_viridis_c(option = "D", direction = -1) +  
  scale_color_identity() +  
  labs(title = "Heatmap de conservación de KOs y Motivos por clase", 
       x = "KOs y Motivos", 
       y = "Clase", 
       fill = "Conservación\n(Número de especies)") + 
  theme_minimal(base_family = "Times New Roman") +  
  theme(text = element_text(size = 14), 
        plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 45, hjust = 1))

# Exportar como PNG con mayor resolución
# Parámetros de salida:
#   width (int): Ancho de la imagen en píxeles.
#   height (int): Alto de la imagen en píxeles.
#   res (int): Resolución de la imagen en dpi.
png("Conservación.png", width = 3300, height = 2400, res = 300)

# Generar el gráfico
ggplot(heatmap_long, aes(x = Gene, y = Class, fill = Conservación)) +
  geom_tile(color = "black", size = 0.5) +  
  geom_text(aes(label = Conservación, color = ifelse(Conservación > 150, "white", "black")), size = 15) +
  scale_fill_viridis_c(option = "D", direction = -1) +  
  scale_color_identity() +  
  labs(title = "Heatmap de conservación de KOs y Motivos por clase", 
       x = "KOs y Motivos", 
       y = "Clase", 
       fill = "Conservación\n(Número de especies)") + 
  theme_minimal(base_family = "Times New Roman") +
  theme(text = element_text(size = 45), 
        plot.title = element_text(hjust = 4, size = 66),
        axis.text.x = element_text(angle = 70, hjust = 1, size = 45),
        axis.text.y = element_text(size = 45))

# Finalizar la exportación
dev.off()
