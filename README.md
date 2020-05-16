This is the RankChecker Project.

RankChecker is a GUI App running on Mac OS X.

RankChecker is the simple tool to check Google search engine rankings.

This app was made by Tkinter which is the Python GUI Framework.

Please install following package by conda or pip.

### Setup

pillow is Image Processing Library.
This package enable to show image on the App.

`conda install pillow`

To handle DataFrame, please install pandas.

`conda install pandas`

"google" is a Python bindings to the Google search engine.

`conda install google`

### Running Python File

To run this app, you just run main.py.

`python main.py` 

### Building to app on Mac OS X(option)
py2app is the very useful package.
If you want to make App from .py files, Please install this.

`conda install py2app`

then, you can make .app by typing this command.

`python setup.py py2app -A`

.app will exist in the dist directory.
