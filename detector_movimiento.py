import cv2
import numpy as np
import serial
import time

# Inicializar la cámara (índice 0, puede variar según la PC)
cap = cv2.VideoCapture(0)

# Conectarse al Arduino en el puerto COM4 (verifica el puerto correcto en tu PC)
arduino = serial.Serial('COM4', 9600)  # Cambia 'COM4' al puerto correcto
time.sleep(2)  # Esperar 2 segundos para que el Arduino se inicie

# Configuración inicial para la detección de movimiento
ret, frame1 = cap.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

def detector_movimiento():
    while True:
        ret, frame2 = cap.read()
        if not ret:
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Calcular la diferencia entre los frames
        diff = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Encontrar contornos de áreas con movimiento
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Ajustar sensibilidad
                motion_detected = True
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Mostrar el resultado en pantalla
        cv2.imshow("Detección de Movimiento - Scorpion Security", frame2)

        # Enviar señal al Arduino
        if motion_detected:
            arduino.write(b'M')  # Envía 'M' para activar el buzzer
        else:
            arduino.write(b'N')  # Envía 'N' para desactivar

        # Actualizar el frame de referencia
        gray1 = gray2

        # Salir con la tecla 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    detector_movimiento()
