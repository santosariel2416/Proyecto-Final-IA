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
    global ejecutando, ultimo_envio
    ejecutando = True

    cap = cv2.VideoCapture(0)

    while ejecutando:
        ret, frame = cap.read()

        if not ret:
            break

        resultados = model(frame)

        cv2.rectangle(frame, (zona[0], zona[1]), (zona[2], zona[3]), (0, 0, 255), 2)

        for r in resultados:
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

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame, (cx, cy), 5, color, -1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        yield frame

    cap.release()

def detener_video():
    global ejecutando
    ejecutando = False
    return None

with gr.Blocks(
    theme=gr.themes.Base(), # Tema compatible con tu versión
    css="""
    body { background-color: #0f172a; color: white; }
    h1, h2 { text-align: center; }
    """
) as interfaz:

    gr.Markdown("# 🛡️ SISTEMA DE SEGURIDAD PARA EL HOGAR")
    gr.Markdown("## 🔍 DETECCIÓN DE INTRUSOS EN TIEMPO REAL")

    with gr.Row():
        imagen = gr.Image(label="📷 Monitoreo en Vivo", height=400)

    with gr.Row():
        btn_iniciar = gr.Button("▶️ Iniciar Sistema", scale=1)
        btn_detener = gr.Button("⏹️ Detener Sistema", scale=1)

    btn_iniciar.click(fn=iniciar_video, outputs=imagen)
    btn_detener.click(fn=detener_video, outputs=imagen)

interfaz.launch()