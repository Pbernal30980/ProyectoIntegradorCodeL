from ultralytics import YOLO

model_yolo = YOLO("yolov8n.pt")
results = model_yolo("imgr.jpg")

# Ultralytics may return a list of Results. Ensure we call show/plot on each item.
if isinstance(results, list):
    for r in results:
        # Newer ultralytics Results have a `show()` or `plot()` method.
        if hasattr(r, "show"):
            r.show()
        elif hasattr(r, "plot"):
            img = r.plot()
            # If plot() returns an image array, display via OpenCV (optional) or save.
            try:
                import cv2
                cv2.imshow('result', img[:, :, ::-1])
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception:
                # If cv2 is not available or running headless, try saving
                try:
                    from pathlib import Path
                    out = Path('result.jpg')
                    cv2.imwrite(str(out), img[:, :, ::-1])
                    print(f"Saved plotted result to {out}")
                except Exception:
                    pass
else:
    # Single Results object
    if hasattr(results, "show"):
        results.show()
    elif hasattr(results, "plot"):
        try:
            img = results.plot()
            import cv2
            cv2.imshow('result', img[:, :, ::-1])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception:
            # fallback: save using results.save() if available
            if hasattr(results, "save"):
                results.save()

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB-xA) * max(0, yB-yA)
    boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

    return interArea / float(boxAArea + boxBArea - interArea)
