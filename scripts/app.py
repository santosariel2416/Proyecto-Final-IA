# Nombre: Jesus Ariel Santos
# Matricula: 24-EISN-2-034

import gradio as gr # Uso Gradio para crear una interfaz gráfica interactiva
import cv2 # Uso OpenCV para manejar la cámara
from ultralytics import YOLO # Modelo de detección de objetos
from telegram_bot import enviar_alerta # Importo la función de alertas
import time # Control de tiempo para evitar spam

model = YOLO("yolov8n.pt") # Cargo el modelo 

zona = (100, 100, 400, 400) # Zona restringida

ultimo_envio = 0 # Control de alertas
ejecutando = False # Controla si el video está activo

def iniciar_video():
    global ejecutando, ultimo_envio # Permite modificar estas variables globales dentro de la función
    ejecutando = True # Indica que el sistema está activo 

    cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Abre la cámara de la laptop (índice 0) 
    cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW) # Abre la cámara del celular (índice 1)

    while ejecutando: # Mientras el sistema esté activo, sigue ejecutándose
        ret1, frame1 = cap1.read() # Captura un frame (imagen) de la cámara 1
        ret2, frame2 = cap2.read() # Captura un frame de la cámara 2

        if not ret1 or not ret2: # Si alguna cámara falla
            continue # Se salta este ciclo y vuelve a intentar
        

        #  CAMARA 1 
        resultados1 = model(frame1) # La IA analiza la imagen de la cámara 1

        cv2.rectangle(frame1, (zona[0], zona[1]), (zona[2], zona[3]), (0, 0, 255), 2) # Dibuja la zona restringida en color rojo

        for r in resultados1: # Recorre los resultados detectados
            for box in r.boxes: # Recorre cada objeto detectado
                clase = int(box.cls[0]) # Obtiene el tipo de objeto detectado

                if clase == 0: # Solo nos interesa cuando es una persona (clase 0)
                    x1, y1, x2, y2 = map(int, box.xyxy[0]) # Coordenadas del rectángulo de la persona

                    cx = (x1 + x2) // 2 # Calcula el centro en X de la persona
                    cy = (y1 + y2) // 2 # Calcula el centro en Y de la persona

                    if zona[0] < cx < zona[2] and zona[1] < cy < zona[3]:  # Verifica si la persona está dentro de la zona restringida
                        color = (255, 0, 0) # Rojo = intruso


                        tiempo_actual = time.time() # Obtiene el tiempo actual


                        if tiempo_actual - ultimo_envio > 5: # Verifica si han pasado más de 5 segundos desde la última alerta
                            enviar_alerta() # Envía mensaje a Telegram
                            ultimo_envio = tiempo_actual # Actualiza el tiempo del último envío
                    else:
                        color = (0, 255, 0)  # Verde = persona fuera de la zona 

                    cv2.rectangle(frame1, (x1, y1), (x2, y2), color, 2) # Dibuja el rectángulo de la persona
                    cv2.circle(frame1, (cx, cy), 5, color, -1) # Dibuja un punto en el centro de la persona

        #  CAMARA 2 
        resultados2 = model(frame2) # La IA analiza la imagen de la cámara 2

        cv2.rectangle(frame2, (zona[0], zona[1]), (zona[2], zona[3]), (0, 0, 255), 2) # Dibuja la zona restringida en la segunda cámara

        for r in resultados2:
            for box in r.boxes:
                clase = int(box.cls[0])

                if clase == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if zona[0] < cx < zona[2] and zona[1] < cy < zona[3]:
                        color = (255, 0, 0)

                        tiempo_actual = time.time()

                        if tiempo_actual - ultimo_envio > 5:
                            enviar_alerta()
                            ultimo_envio = tiempo_actual
                    else:
                        color = (0, 255, 0)

                    cv2.rectangle(frame2, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame2, (cx, cy), 5, color, -1)

        # Ajuste tamaño para evitar errores
        frame1 = cv2.resize(frame1, (400, 300)) # Reduce tamaño de la cámara 1
        frame2 = cv2.resize(frame2, (400, 300)) # Reduce tamaño de la cámara 2

        combinado = cv2.hconcat([frame1, frame2]) # Une las dos cámaras lado a lado


        frame = cv2.cvtColor(combinado, cv2.COLOR_BGR2RGB) # Convierte colores para que Gradio lo muestre correctamente

        yield frame # Envía el frame a la interfaz en tiempo real

    cap1.release()  # Libera la cámara 1
    cap2.release()  # Libera la cámara 2

def detener_video():
    global ejecutando
    ejecutando = False # Apaga el sistema
    return None

with gr.Blocks(
    theme=gr.themes.Base(), # Tema visual de la app
    css="""
    body { background-color: #0f172a; color: white; }
    h1, h2 { text-align: center; }
    """
) as interfaz:

    gr.Markdown("# 🛡️ SISTEMA DE SEGURIDAD PARA EL HOGAR") # Título principal
    gr.Markdown("## 🔍 DETECCIÓN DE INTRUSOS EN TIEMPO REAL") # Subtítulo

    with gr.Row():
        imagen = gr.Image(label="📷 Monitoreo en Vivo", height=400)

    with gr.Row():
        btn_iniciar = gr.Button("▶️ Iniciar Sistema", scale=1) # Botón para iniciar
        btn_detener = gr.Button("⏹️ Detener Sistema", scale=1) # Botón para detener

    btn_iniciar.click(fn=iniciar_video, outputs=imagen) # un clic para iniciar 
    btn_detener.click(fn=detener_video, outputs=imagen) # un clic para detener 

interfaz.launch() # Ejecuta la aplicacion 