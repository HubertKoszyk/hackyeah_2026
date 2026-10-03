import numpy as np
import requests
from .image_getter import get_image

class CameraRepository():
    def __init__(self):
        pass

    def get_photo(self, url : str) -> np.ndarray:
<<<<<<< Updated upstream
        return get_image(url)
=======
        get_image(url)

>>>>>>> Stashed changes
