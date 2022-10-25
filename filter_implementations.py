import filter
import cv2

class Brightness(filter.Filter):
    def __init__(self) -> None:
        super().__init__()

    def process(self, params, image):
        print("brightness")
        return image #super().process(params, image)

    def getUiMetadata(self):
        return super().getUiMetadata()

class Hue(filter.Filter):
    def __init__(self) -> None:
        super().__init__()

    def process(self, params, image):
        print("hue")
        return image # super().process(params, image)

    def getUiMetadata(self):
        return super().getUiMetadata()