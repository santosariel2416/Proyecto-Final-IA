# Nombre: Jesus Ariel Santos
# Matricula: 24-EISN-2-034

from ultralytics import YOLO #Aquí importo el modelo YOLOv8 que se encarga de detectar personas en las imágenes o video.
import cv2 # Uso OpenCV para capturar video en tiempo real y dibujar las detecciones.
import os # La importé para manejar rutas de archivos
from telegram_bot import enviar_alerta # Importo la función para enviar alertas por Telegram
import time # Uso time para controlar el envío de alertas

 
model = YOLO("yolov8n.pt") # Cargo el modelo YOLOv8 preentrenado para detectar objetos en tiempo real.

# Aquí inicializo la cámara para capturar video en tiempo real.
cap = cv2.VideoCapture(0) 

# Defino una zona restringida (x1, y1, x2, y2)
zona = (100, 100, 400, 400)

# Variable para controlar el tiempo entre alertas
ultimo_envio = 0

contador_frames = 0 # Variable para reducir el procesamiento de frames
COOLDOWN = 60 # Tiempo de espera entre alertas

# Verificar si la cámara abrió correctamente 
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara") #Valido que la cámara esté funcionando antes de continuar.
    exit()

while True: #Uso un bucle infinito para procesar continuamente los frames del video.
    ret, frame = cap.read()

    if not ret:
        print("Error al capturar el frame") #Muestra error y detiene el programa
        break

    contador_frames += 1

    if contador_frames % 3 != 0:
        continue

    # Ejecutar detección
    resultados = model(frame, imgsz=640, conf=0.5)  

    # Dibujar la zona restringida
    cv2.rectangle(frame, (zona[0], zona[1]), (zona[2], zona[3]), (255, 0, 0), 2)

    # Procesar resultados
    for r in resultados:
        for box in r.boxes:
            clase = int(box.cls[0])

            # Clase 0 = persona
            if clase == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                ancho = x2 - x1
                alto = y2 - y1

                if ancho < 50 or alto < 50:
                    continue

                # Calculo el centro de la persona
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Verifico si la persona está dentro de la zona restringida
                if zona[0] < cx < zona[2] and zona[1] < cy < zona[3]:
                    color = (0, 0, 255) # rojo si es intruso

                    tiempo_actual = time.time()

                    # Evito enviar muchas alertas seguidas
                    if tiempo_actual - ultimo_envio > COOLDOWN:
                        enviar_alerta()
                        ultimo_envio = tiempo_actual

                else:
                    color = (0, 255, 0) # verde si está fuera de la zona

                # Dibujar rectángulo
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Dibujar el centro de la persona
                cv2.circle(frame, (cx, cy), 5, color, -1)

    # Mostrar resultado
    cv2.imshow("Deteccion de Personas", frame)

    # Presiona ESC para salir
    if cv2.waitKey(1) == 27:
        break

cap.release() # Esto apaga la camara 
cv2.destroyAllWindows() #esto cierra la ventana