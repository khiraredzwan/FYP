
+++++++++++++++++++++++
PROJECT PRE-REQUISITES
+++++++++++++++++++++++

1) Anaconda (Python 3++, x86 or x64)
2) Install some additional libraries (see following links for how-to install)
   i)   OpenCV (https://anaconda.org/conda-forge/opencv)
   ii)  Scikit-Image (https://anaconda.org/anaconda/scikit-image)
   iii) PySide (https://anaconda.org/anaconda/pyside)

+++++++
FOLDER
+++++++

Part 1  - Training Dataset (Model Generation)
-------

"Image Dataset" folder - contains cropped knot images for both Acacia & Getah
"Training" folder - contains pre-procesing & SVM training code

Part 2  - Prediction System
-------

Contains a Python system for image knot prediction.
   - Using trained model from Part 1.
   - Using PySide for GUI interface.

main.py - the main processing code. It contains code on what-to-do when GUI elements are clicked.
mainwindow.ui - contains XML code for UI design. This file can be designed using Qt Designer.
modelAcacia-0.76-linear.pkl - pickle file for best SVM trained model of Acacia tree
modelGetah-0.79-linear.pkl - pickle file for best SVM trained model of Getah tree

++++++++++++
EXPLANATION
++++++++++++

1) Run the image pre-processing & SVM training (inside "Part 1" folder)
   i) "Part 1/Training" folder (run for both Acacia & Rubber)

2) Copy the highest model into the "Part 2" folder. (see main.py for model naming)

3) Run the prediction interface (it will take a while to load the model)
   i) Run main.py to run the system