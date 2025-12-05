import torch
import cv2
from ultralytics import YOLO
import ultralytics.nn.tasks as tasks

# Registrar safe globals solo si la función existe (compatibilidad con distintas versiones de torch)
import torch.nn.modules.container as container

if hasattr(torch, "serialization") and hasattr(torch.serialization, "add_safe_globals"):
    try:
        torch.serialization.add_safe_globals([
            tasks.DetectionModel,
            container.Sequential,
        ])
    except Exception:
        # No interrumpir la ejecución si la API cambia
        pass


if __name__ == "__main__":
    # Cargar el modelo nano (rápido y liviano)
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated = results[0].plot()  # dibuja las detecciones

        cv2.imshow("Detección YOLOv8", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()