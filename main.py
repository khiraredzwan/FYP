from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import *
import sys,os, cv2, glob,warnings
from sklearn import svm
from sklearn.externals import joblib
import skimage.color, skimage.io
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import exposure, feature, img_as_ubyte 
from skimage.filters.rank import entropy
from skimage.morphology import disk
from matplotlib import pyplot as plt
import numpy as np
from scipy.ndimage.filters import median_filter
from numpy import array
import matplotlib.image as mpimg
from skimage.feature import greycomatrix,greycoprops
from skimage.filters import threshold_otsu
import pandas as pd
from skimage.feature import local_binary_pattern
from scipy import misc

class App(QWidget):

	def __init__(self):

		# top level qt's window
		self.root = QApplication(sys.argv)
		QWidget.__init__(self)
		self.setWindowTitle("Ident-Knot")

		self.root.setStyle(QStyleFactory.create('GTK+'))

		# load SVM trained model 
		self.lin_svc_acacia = joblib.load('modelAcacia-0.76-linear.pkl')
		self.lin_svc_rubber = joblib.load('modelGetah-0.79-linear.pkl') 

		self.init_ui()
		self.load_widgets()
		
		self.button_upload.clicked.connect(self.push_button_action)
		self.button_process.clicked.connect(self.do_processing)
		self.radioButton_Acacia.clicked.connect(self.radio_acacia_clicked)
		self.radioButton_rubber.clicked.connect(self.radio_rubber_clicked)

		# show the QDialog
		self.show()

		# enter application event loop
		self.root.exec_()
		
		
	def do_processing(self):
		
		# 1) pre-processing
		data = self.image_processing(self.fileName)
		data = np.reshape(data, (1, -1))
		
		# 2) use trained SVM model for data prediction
		predicted_output = self.predict_with_svm(data)[0]
		
		output_str = "Sound" if predicted_output == 0 else "Unsound"
		
		# 3) show it to the user
		self.label_output.setText("Predicted Class : " + output_str)

	def radio_acacia_clicked(self):
		self.button_process.setEnabled(True)

	def radio_rubber_clicked(self):
		self.button_process.setEnabled(True)
		
	def predict_with_svm(self, X):
		if self.radioButton_Acacia.isChecked():
			return self.lin_svc_acacia.predict(X)
		else:
			return self.lin_svc_rubber.predict(X)

	def image_processing(self,fileName):
		#change to gray
		im = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)

		#contrast
		icon = exposure.rescale_intensity(im, in_range=(np.percentile(im,5), np.percentile(im,20)))
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			dt = img_as_ubyte(icon)

		# make image blur
		imed = cv2.medianBlur(icon.astype(np.uint8), 3)

		#LBP
		radius = 3
		n_points = 8 * radius
		lbp = local_binary_pattern(imed, n_points, radius, 'ror')

		return lbp.flatten().tolist()
		
	def push_button_action(self):
		self.fileName = self.openFileNameDialog()
		pixmap = QPixmap(self.fileName)
		self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))
		self.groupBox_radio.setEnabled(True)

	def openFileNameDialog(self):
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
		return fileName

	def init_ui(self):
	
		''' baca ui yg hg design kt qt creator '''

		ui_file_path = os.path.join(os.path.realpath(
								os.path.dirname(__file__)),
								'mainwindow.ui')
		self.main_gui = self.load_ui(ui_file_path)

		# Add a vertical layout with all our widgets
		layout = QVBoxLayout()
		layout.addWidget(self.main_gui)
		self.setLayout(layout)

		# show the QDialog
		self.show()

	def load_widgets(self):
	
		''' load suma elements yg hg tarik masuk dlm windows '''

		self.button_upload = self.findChild(QPushButton, "pushButton_upload")
		self.label = self.findChild(QLabel, "label")
		self.button_process = self.findChild(QPushButton,"pushButton_process" )
		self.label_output = self.findChild(QLabel, 'label_output')

		# load radio buttons
		self.groupBox_radio = self.findChild(QGroupBox, 'groupBox_radio')
		self.radioButton_Acacia = self.findChild(QRadioButton, 'radioButton_Acacia')
		self.radioButton_rubber = self.findChild(QRadioButton, 'radioButton_rubber')

	def load_ui(self, filename):

		# open up .ui file
		file = QFile(filename)
		file.open(QIODevice.ReadOnly)

		# file = QFile object to file name
		# None = parent widget
		loader = QUiLoader()
		ui = loader.load(file, None)

		# clear up resource`
		file.close()

		# return `ui` widget object to caller
		return ui



if __name__ == '__main__':

	try:
		sys.exit(App())

	except Exception as e:
		msgBox = QMessageBox()
		msgBox.setText(str(e))
		msgBox.exec_()