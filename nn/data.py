from typing import TypeVar, List

import numpy as np
from PyQt5.QtGui import QImage

from ui.constants import MAXPOOL_SIZE


class Sample:
    def __init__(self, image, cls):
        self.image = image
        self.cls = cls


class ImageDataGenerator:
    def __init__(self):
        pass

    @staticmethod
    def imageAsArray(image: QImage):
        image = image.convertToFormat(QImage.Format_RGB32)
        width = image.width()
        height = image.height()

        ptr = image.constBits()
        ptr.setsize(height * width * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))  # GBRff
        arr = np.delete(arr, -1, axis=2)  # GBR
        return np.fliplr(arr)

    @staticmethod
    def _toGrayscale(image: np.ndarray):
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray

    @staticmethod
    def convertImage(image: QImage):
        arr = ImageDataGenerator.imageAsArray(image)
        return ImageDataGenerator._toGrayscale(arr)

    @staticmethod
    def _maxpool(image: np.ndarray, output_size=MAXPOOL_SIZE):
        input_size = image.shape[0]
        bin_size = input_size // output_size
        return image.reshape((1, output_size, bin_size,
                              output_size, bin_size)).max(4).max(2)

    @staticmethod
    def prepareImage(image: QImage):
        arr = ImageDataGenerator.convertImage(image)
        return ImageDataGenerator._maxpool(arr).flatten()

    @staticmethod
    def prepareSample(sample: Sample):
        return ImageDataGenerator.prepareImage(sample.image), sample.cls

    @staticmethod
    def PrepareDataset(samples: List[Sample]) -> tuple:
        X = []
        y = []
        for s in samples:
            xi, yi = ImageDataGenerator.prepareSample(s)
            X.append(xi)
            y.append(yi)

        return np.array(X), np.array(y)


class ImageDatasetDTO:
    def __init__(self, samples, name, classes):
        self.name = name
        self.classes = classes
        self.samples = samples


class ImageDataset:
    IMG = TypeVar('IMG', QImage, np.ndarray)

    def __init__(self, samples=None):
        self.name = 'dataset'
        self.classes = {
            0: 'class_0',
            1: 'class_1'
        }

        if samples is None:
            samples: List[Sample] = list()
        self.samples = samples

    def __len__(self):
        return len(self.samples)

    def get_classes(self) -> tuple:
        return self.classes[0], self.classes[1]

    def toDTO(self) -> ImageDatasetDTO:
        samples = []
        for item in self.samples:
            image = item.image.convertToFormat(QImage.Format_RGB32)
            width = image.width()
            height = image.height()

            ptr = image.constBits()
            ptr.setsize(height * width * 4)
            arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
            samples.append((arr, item.cls))
        return ImageDatasetDTO(samples, self.name, self.classes)

    @staticmethod
    def fromDto(dto: ImageDatasetDTO):
        dataset = ImageDataset()

        dataset.name = dto.name
        dataset.classes = dto.classes
        for item in dto.samples:
            image = QImage(item[0], item[0].shape[1], item[0].shape[1],
                           QImage.Format_RGB32)
            cls = item[1]
            dataset.samples.append(Sample(image, cls))
        return dataset
