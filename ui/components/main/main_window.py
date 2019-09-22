import pickle

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog

from nn.data import ImageDataset, Sample, ImageDataGenerator
from nn.perceptron import Perceptron
from ui.components.dialog.class_dialog import ClassDialog
from ui.components.main import main_form
from ui.constants import PEN_TYPES, PEN_COLORS, WHITE_COLOR, DIALOG_SIGNAL_CLASS_0, \
    DIALOG_SIGNAL_CLASS_1, MAXPOOL_SIZE


class MainWindow(QtWidgets.QMainWindow, main_form.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._initDrawerSettings()
        self.load_image_button.clicked.connect(self._openImageFile)

        self._dataset = ImageDataset()
        self._selectedPreviewIdx = None
        self.nn = Perceptron(MAXPOOL_SIZE ** 2)

        self.dialog = ClassDialog(self._dataset.get_classes())
        self._initModelTab()
        self._initDatasetTab()
        self._initOther()

    def _initDrawerSettings(self):
        for name in PEN_TYPES:
            self.penTypeBox.addItem(name, PEN_TYPES[name])
        self.penTypeBox.currentIndexChanged.connect(
            lambda idx: self.painter.changePenType(self.penTypeBox.currentData()))

        for name in PEN_COLORS:
            self.penColorBox.addItem(name, PEN_COLORS[name])
        self.penColorBox.currentIndexChanged.connect(
            lambda idx: self.painter.changePenColor(self.penColorBox.currentData()))

        self.spinSizeBox.valueChanged.connect(
            lambda idx: self.painter.changePenSize(self.spinSizeBox.value())
        )

        self.clearCanvasButton.clicked.connect(
            lambda: self.painter.clearCanvas()
        )

    def _initDatasetTab(self):
        self.saveDatasetButton.setEnabled(False)  # TODO: self._saveDataset
        self.loadDatasetButton.setEnabled(False)  # TODO: self._loadDataset

        self.nextImageButton.clicked.connect(self._showNextImage)
        self.previousImageButton.clicked.connect(self._showPreviousImage)
        self.editButton.clicked.connect(self._setPreviewImageOnPainter)
        self.removeImageButton.clicked.connect(self._removeImage)
        self.clearDatasetButton.clicked.connect(self._clearDataset)
        self.loadDatasetButton.clicked.connect(self._loadDataset)
        self.saveDatasetButton.clicked.connect(self._saveDataset)

    def _initModelTab(self):
        self.dropWeightsButton.clicked.connect(lambda: self.nn.set_random_weights())
        self.loadModelButton.clicked.connect(self._loadModel)
        self.saveModelButton.clicked.connect(self._saveModel)
        self.trainModelButton.clicked.connect(self._trainModel)
        self._updateModelLabels()

    def _initOther(self):
        self.addImageButton.clicked.connect(self._addToDataset)
        self.trainButton.clicked.connect(self._trainOnImage)
        self.checkImageButton.clicked.connect(self._predict)
        # edit = QLineEdit()
        # self.class0ValueLabel.setBuddy(edit)

    def _openImageFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                  QDir.currentPath())
        if fileName:
            self.painter.openImage(fileName)

    def _loadDataset(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                  QDir.currentPath())
        if fileName:
            with open(fileName, 'rb') as dataset:
                self._dataset: ImageDataset = pickle.load(dataset)
                self._setPreviewImage(self._dataset.samples[0])

    def _saveDataset(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File",
                                                  QDir.currentPath())
        with open(fileName, 'wb') as f:
            pickle.dump(self._dataset, f)

    def _loadModel(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Загрузить модель",
                                                  QDir.currentPath())
        if fileName:
            with open(fileName, 'rb') as model:
                self.nn: Perceptron = pickle.load(model)
            self._updateModelLabels()

    def _saveModel(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить модель",
                                                  QDir.currentPath())
        with open(fileName, 'wb') as f:
            try:
                pickle.dump(self.nn, f)
            except FileNotFoundError:
                pass

    def _predict(self):
        arr = ImageDataGenerator.prepareImage(self.painter.image)
        print(self.nn.predict(arr))

    def _trainOnImage(self):
        cls = self._selectClass()
        if cls is None:
            return

        arr = ImageDataGenerator.prepareImage(self.painter.image)
        self.nn.train_on_sample(arr, cls)

    def _addToDataset(self):
        cls = self._selectClass()
        if cls is None:
            return

        copy = self.painter.image.copy()
        self._dataset.samples.append(Sample(copy, cls))
        if self._selectedPreviewIdx is None:
            self._selectedPreviewIdx = 0
            self._setPreviewImage(self._dataset.samples[0])
        self._updatePreviewLabel()

    def _clearDataset(self):
        self._dataset.samples.clear()
        self._selectedPreviewIdx = None
        self.previewBox.image.fill(WHITE_COLOR)
        self.previewBox.update()
        self._updatePreviewLabel()

    def _setPreviewImage(self, sample: Sample):
        self.previewBox.setImage(sample.image)
        self.previewClassLabel.setText(self._dataset.classes[sample.cls])

    def _showNextImage(self):
        if self._selectedPreviewIdx is not None \
                and self._selectedPreviewIdx != len(self._dataset.samples) - 1:
            self._selectedPreviewIdx += 1
            self._setPreviewImage(self._dataset.samples[self._selectedPreviewIdx])
            self._updatePreviewLabel()

    def _showPreviousImage(self):
        if self._selectedPreviewIdx is not None and self._selectedPreviewIdx != 0:
            self._selectedPreviewIdx -= 1
            self._setPreviewImage(self._dataset.samples[self._selectedPreviewIdx])
            self._updatePreviewLabel()

    def _updatePreviewLabel(self):
        idx = self._selectedPreviewIdx
        text = '{0}/{1}'.format((
            idx + 1 if idx is not None else '-'),
            len(self._dataset.samples))
        self.imageNumberValueLabel.setText(text)
        self.previewClassLabel.setText(
            self._dataset.classes[self._dataset.samples[idx].cls] if idx is not None else ' ')

    def _setPreviewImageOnPainter(self):
        if self._selectedPreviewIdx is not None:
            self.painter.image = self._dataset.samples[self._selectedPreviewIdx].image.copy()
            self.painter.update()

    def _removeImage(self):
        idx = self._selectedPreviewIdx
        if idx is None:
            return
        del self._dataset.samples[idx]

        if len(self._dataset.samples) == 0:
            self._selectedPreviewIdx = None
            self.previewBox.image.fill(WHITE_COLOR)
            self.previewBox.update()
        elif idx == len(self._dataset.samples):
            self._setPreviewImage(self._dataset.samples[idx - 1])
            self._selectedPreviewIdx -= 1
        else:
            self._setPreviewImage(self._dataset.samples[idx])

        self._updatePreviewLabel()

    def _selectClass(self):
        returnCode = self.dialog.exec_()
        if returnCode == 0:
            return None
        if returnCode == DIALOG_SIGNAL_CLASS_0:
            return 0
        if returnCode == DIALOG_SIGNAL_CLASS_1:
            return 1

    def _updateModelLabels(self):
        self.inputValueLabel.setText(str(self.nn.size()))

    def _trainModel(self):
        X, y = ImageDataGenerator.PrepareDataset(self._dataset.samples)
        self.nn.train(X, y)
        print("trained")
