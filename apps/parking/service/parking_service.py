import numpy as np
from ultralytics import YOLO

try:
    from django.conf import settings

    MODEL_PATH = str(settings.MODEL_PATH)
    MODEL_CONFIDENCE = settings.MODEL_CONFIDENCE
    MODEL_IMAGE_SIZE = settings.MODEL_IMAGE_SIZE

except:
    MODEL_PATH = "yolov8m.pt"
    MODEL_CONFIDENCE = 0.25
    MODEL_IMAGE_SIZE = 640


class ParkingService:
    """Service responsible for detecting and counting vehicles in images.
        Attributes:
            path: Path to the YOLO model.
            confidence: Minimum confidence threshold for detections.
            image_size: Image size used by the YOLO model during inference.
    """

    def __init__(self,
                 path = MODEL_PATH,
                 confidence = MODEL_CONFIDENCE,
                 image_size = MODEL_IMAGE_SIZE
    ) -> None:
        """Initialize the parking service.
           Args:
                path: Path to the YOLO model.
                confidence: Minimum confidence threshold for detections.
                image_size: Image size used during model inference.
        """

    def __init__(self, path=MODEL_PATH, confidence=MODEL_CONFIDENCE, image_size=MODEL_IMAGE_SIZE) -> None:
        self.path = path
        self.confidence = confidence
        self.image_size = image_size
        self.model = YOLO(self.path)

    def count_vehicles(self, image: np.ndarray) -> int:
        """Count cars detected in an image.
           Args:
               image: Image represented as a NumPy array.
               Returns: Number of cars detected in the image.
        """

        model = YOLO(self.path)
        results = model(image, conf=self.confidence, imgsz=self.image_size)
        results = self.model(image, conf=self.confidence, imgsz=self.image_size, verbose=False)

        car_count = 0

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]

            if class_name == "car":
                car_count += 1

        return car_count