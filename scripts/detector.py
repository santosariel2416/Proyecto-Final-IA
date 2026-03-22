# Nombre: Jesus Ariel Santos
# Matricula: 24-EISN-2-034

from ultralytics import YOLO #Aquí importo el modelo YOLOv8 que se encarga de detectar personas en las imágenes o video.
import cv2 # Uso OpenCV para capturar video en tiempo real y dibujar las detecciones.
import os # La importé para manejar rutas de archivos

 
model = YOLO("yolov8n.pt") # Cargo el modelo YOLOv8 preentrenado para detectar objetos en tiempo real.

# Aquí inicializo la cámara para capturar video en tiempo real.
cap = cv2.VideoCapture(0) 

# Verificar si la cámara abrió correctamente 
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara") #Valido que la cámara esté funcionando antes de continuar.
    exit()

while True: #Uso un bucle infinito para procesar continuamente los frames del video.
    ret, frame = cap.read()

    if not ret:
        print("Error al capturar el frame") #Muestra error y detiene el programa
        break

    # Ejecutar detección
    resultados = model(frame)  

    # Procesar resultados
    for r in resultados:
        for box in r.boxes:
            clase = int(box.cls[0])

            # Clase 0 = persona
            if clase == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Dibujar rectángulo
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Mostrar resultado
    cv2.imshow("Deteccion de Personas", frame)

    # Presiona ESC para salir
    if cv2.waitKey(1) == 27:
        break

cap.release() # Esto apaga la camara 
cv2.destroyAllWindows() #esto cierra la ventana 