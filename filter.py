from abc import ABC, abstractmethod

class Param():
    def __init__(self) -> None:
        pass

class Params():
    def __init__(self) -> None:
        pass

class Filter(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, params, image):
        pass

    @abstractmethod
    def getUiMetadata(self):
        pass


class VideoFilter():
    def __init__(self) -> None:
        pass

    def selectVideo(self):
        pass

    def addFilter(self):
        pass

    def getFilters(self):
        pass

    def exportVideo(self):
        pass

    def previewVideo(self):
        pass