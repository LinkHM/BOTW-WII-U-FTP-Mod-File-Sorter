from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import Sortmodfiles as smf
import os
import configparser

PROGRAM_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_INI_PATH = PROGRAM_DIR + os.sep + "settings.ini"
MENU_UI_PATH = PROGRAM_DIR + os.sep + 'menu.ui'

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(MENU_UI_PATH, self)

        # Get and Connect Required Buttons
        self.browseBaseGameList_Btn = self.findChild(QtWidgets.QPushButton, "browseBaseGameList_Btn")
        self.browseBaseGameList_Btn.clicked.connect(self.openBrowseBaseGameList)
        self.browseUpdateList_Btn = self.findChild(QtWidgets.QPushButton, "browseUpdateList_Btn")
        self.browseUpdateList_Btn.clicked.connect(self.openBrowseUpdateList)
        self.browseDLCList_Btn = self.findChild(QtWidgets.QPushButton, "browseDLCList_Btn")
        self.browseDLCList_Btn.clicked.connect(self.openBrowseDLCList)

        self.browseModFolder_Btn = self.findChild(QtWidgets.QPushButton, "browseModFolder_Btn")
        self.browseModFolder_Btn.clicked.connect(self.openBrowseModFolder)
        self.browseOutputFolder_Btn = self.findChild(QtWidgets.QPushButton, "browseOutputFolder_Btn")
        self.browseOutputFolder_Btn.clicked.connect(self.openBrowseOutputFolder)

        self.startSorting_Btn = self.findChild(QtWidgets.QPushButton, "startSorting_Btn")
        self.startSorting_Btn.setEnabled(False)
        self.startSorting_Btn.clicked.connect(self.startSortingMod)
        self.exitApp_Btn = self.findChild(QtWidgets.QPushButton, "exitApp_Btn")
        self.exitApp_Btn.clicked.connect(self.exitBtnPressed)
        self.savePaths_Btn = self.findChild(QtWidgets.QPushButton, "savePaths_Btn")
        self.savePaths_Btn.clicked.connect(self.saveIniFile)

        # Get and Connect Required LineEdits (Text Inputs)
        self.browseBaseGameList_LineEdit = self.findChild(QtWidgets.QLineEdit, "browseBaseGameList_LineEdit")
        self.browseBaseGameList_LineEdit.textChanged.connect(self.bgl_LineEditChanged)
        self.browseUpdateList_LineEdit = self.findChild(QtWidgets.QLineEdit, "browseUpdateList_LineEdit")
        self.browseUpdateList_LineEdit.textChanged.connect(self.udl_LineEditChanged)
        self.browseDLCList_LineEdit = self.findChild(QtWidgets.QLineEdit, "browseDLCList_LineEdit")
        self.browseDLCList_LineEdit.textChanged.connect(self.dlcl_LineEditChanged)

        self.browseModFolder_LineEdit = self.findChild(QtWidgets.QLineEdit, "browseModFolder_LineEdit")
        self.browseModFolder_LineEdit.textChanged.connect(self.modfolder_LineEditChanged)
        self.browseOutputFolder_LineEdit = self.findChild(QtWidgets.QLineEdit, "browseOutputFolder_LineEdit")
        self.browseOutputFolder_LineEdit.textChanged.connect(self.outputfolder_LineEditChanged)

        #Get Required Status Labels
        self.browseBaseGameList_Label = self.findChild(QtWidgets.QLabel, "browseBaseGameList_Label")
        self.browseUpdateList_Label = self.findChild(QtWidgets.QLabel, "browseUpdateList_Label")
        self.browseDLCList_Label = self.findChild(QtWidgets.QLabel, "browseDLCList_Label")

        self.browseModFolder_Label = self.findChild(QtWidgets.QLabel, "browseModFolder_Label")
        self.browseOutputFolder_Label = self.findChild(QtWidgets.QLabel, "browseOutputFolder_Label")

        self.sortingProgress_Label = self.findChild(QtWidgets.QLabel, "sortingProgress_Label")
        self.sortingProgress_Label.displayState = 0

        # Get Progress Bar
        self.sorting_ProgressBar = self.findChild(QtWidgets.QProgressBar, "sorting_ProgressBar")

        # Get Container for all path settings
        self.pathSettingsContainer = self.findChild(QtWidgets.QWidget, "pathSettingsContainer")
        
        # Setup flags for determining if sorting can begin
        self.browseBaseGameList_Label.statusOK = False
        self.browseUpdateList_Label.statusOK = False
        self.browseDLCList_Label.statusOK = False
        self.browseModFolder_Label.statusOK = False
        self.browseOutputFolder_Label.statusOK = False

        # Set Default Paths for LineEdits
        if os.path.isfile(DEFAULT_INI_PATH):
            self.loadIniFile()
        else:
            self.browseBaseGameList_LineEdit.setText(os.path.abspath(smf.DEFAULT_BASEGAMELIST_PATH))
            self.browseUpdateList_LineEdit.setText(os.path.abspath(smf.DEFAULT_UPDATELIST_PATH))
            self.browseDLCList_LineEdit.setText(os.path.abspath(smf.DEFAULT_DLCFILELIST_PATH))

        # Update Status Labels
        self.updateLabelsStatus()

        # Set the main status label to update every 1 sec
        self.updateSortingProgress_timer = QtCore.QTimer()
        self.updateSortingProgress_timer.timeout.connect(self.updateSortingProgress_Label)
        self.updateSortingProgress_timer.start(1000)


        self.show()

    def exitBtnPressed(self):
        if self.pathSettingsContainer.isEnabled():
            sys.exit()
        else:
            confirmQuit = QtWidgets.QMessageBox.question(self, 'Are you sure you want to exit?',
                  "File sorting is in progress; are you sure you want to exit?",
                  QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes,
                  QtWidgets.QMessageBox.Cancel)
            if confirmQuit == QtWidgets.QMessageBox.Yes:
                sys.exit()

    def bgl_LineEditChanged(self):
        self.updatefileListStatus(self.browseBaseGameList_LineEdit, self.browseBaseGameList_Label)

    def udl_LineEditChanged(self):
        self.updatefileListStatus(self.browseUpdateList_LineEdit, self.browseUpdateList_Label)

    def dlcl_LineEditChanged(self):
        self.updatefileListStatus(self.browseDLCList_LineEdit, self.browseDLCList_Label)

    def modfolder_LineEditChanged(self):
        self.updateFolderListStatus(self.browseModFolder_LineEdit, self.browseModFolder_Label)
        self.updateFolderListStatus(self.browseOutputFolder_LineEdit, self.browseOutputFolder_Label)

    def outputfolder_LineEditChanged(self):
        self.updateFolderListStatus(self.browseOutputFolder_LineEdit, self.browseOutputFolder_Label)
        self.updateFolderListStatus(self.browseModFolder_LineEdit, self.browseModFolder_Label)

    def openBrowseBaseGameList(self):
        self.openFileNameDialog(self.browseBaseGameList_LineEdit)

    def openBrowseUpdateList(self):
        self.openFileNameDialog(self.browseUpdateList_LineEdit)

    def openBrowseDLCList(self):
        self.openFileNameDialog(self.browseDLCList_LineEdit)

    def openBrowseModFolder(self):
        self.openFolderNameDialog(self.browseModFolder_LineEdit)

    def openBrowseOutputFolder(self):
        self.openFolderNameDialog(self.browseOutputFolder_LineEdit)
        

    def openFileNameDialog(self, pathLineEdit):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QtWidgets.QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            pathLineEdit.setText(fileName)

    def openFolderNameDialog(self, pathLineEdit):
        folderName = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folderName:
            pathLineEdit.setText(folderName)

    def updateLabelsStatus(self):
        self.updatefileListStatus(self.browseBaseGameList_LineEdit, self.browseBaseGameList_Label)
        self.updatefileListStatus(self.browseUpdateList_LineEdit, self.browseUpdateList_Label)
        self.updatefileListStatus(self.browseDLCList_LineEdit, self.browseDLCList_Label)
        self.updateFolderListStatus(self.browseModFolder_LineEdit, self.browseModFolder_Label)
        self.updateFolderListStatus(self.browseOutputFolder_LineEdit, self.browseOutputFolder_Label)

    def updatefileListStatus(self, pathLineEdit, statusLabel):
        if os.path.isfile(pathLineEdit.text()):
            if pathLineEdit.text()[-4:].upper() != ".TXT":
                shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='orange'>Warning: File not a '.txt' file; Though it should still work as long as it's a plain text file.</font>")
                if shouldUpdateFlag:
                    statusLabel.statusOK = True
                    self.updateStartSortingBtn()
            else:
                shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='green'>Status: Ok</font>")
                if shouldUpdateFlag:
                    statusLabel.statusOK = True
                    self.updateStartSortingBtn()
        else:
            shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='red'>Error: Unable to locate file</font>")
            if shouldUpdateFlag:
                    statusLabel.statusOK = False
                    self.updateStartSortingBtn()

    def updateFolderListStatus(self, pathLineEdit, statusLabel):
        if os.path.isdir(pathLineEdit.text()):
            folderName = os.path.basename(os.path.normpath(pathLineEdit.text()))
            if pathLineEdit.objectName() == "browseModFolder_LineEdit" and not (folderName == 'Content' or folderName == 'content'):
                shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='red'>Error: Selcted folder must be named 'Content' or 'content' not '" + folderName + "'</font>")
                if shouldUpdateFlag:
                    statusLabel.statusOK = False
                    self.updateStartSortingBtn()
            else:
                if self.browseModFolder_LineEdit.text() == self.browseOutputFolder_LineEdit.text():
                    shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='red'>Error: 'Folder to Sort' and 'Output Folder' cannot be the same folder.</font>")
                    if shouldUpdateFlag:
                        statusLabel.statusOK = False
                        self.updateStartSortingBtn()
                else:
                    shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='green'>Status: Ok</font>")
                    if shouldUpdateFlag:
                        statusLabel.statusOK = True
                        self.updateStartSortingBtn()
        else:
            shouldUpdateFlag = self.setTextIfDifferent(statusLabel, "<font color='red'>Error: Unable to locate folder</font>")
            if shouldUpdateFlag:
                statusLabel.statusOK = False
                self.updateStartSortingBtn()


    def updateSortingProgress_Label(self):
        allOKFlags = [self.browseBaseGameList_Label.statusOK,
              self.browseUpdateList_Label.statusOK,
              self.browseDLCList_Label.statusOK,
              self.browseModFolder_Label.statusOK,
              self.browseOutputFolder_Label.statusOK]

        self.sortingProgress_Label.displayState = (self.sortingProgress_Label.displayState + 1) % 4
        if self.pathSettingsContainer.isEnabled():
            if False in allOKFlags:
                
                self.sortingProgress_Label.setText("<font color='red'>Waiting for all fields to be properly filled out" + "." * self.sortingProgress_Label.displayState + "</font>")
            else:
                self.sortingProgress_Label.setText("<font color='green'>Status: Good to go</font>")

                self.sorting_ProgressBar.setValue(smf.percentComplete)
        else:
            if self.sortingProgress_Label.text() != smf.OPERATION_COMPLETE_MSG:
                self.sorting_ProgressBar.setValue(smf.percentComplete)
                self.sortingProgress_Label.setText(smf.textStatus + "." * self.sortingProgress_Label.displayState)
            else:
                self.sorting_ProgressBar.setValue(100)

    def setTextIfDifferent(self, targetLabel, targetText):
        if targetLabel.text() != targetText:
            targetLabel.setText(targetText)
            return True
        return False

    def updateStartSortingBtn(self):
        allOKFlags = [self.browseBaseGameList_Label.statusOK,
              self.browseUpdateList_Label.statusOK,
              self.browseDLCList_Label.statusOK,
              self.browseModFolder_Label.statusOK,
              self.browseOutputFolder_Label.statusOK]

        if False in allOKFlags:
            self.startSorting_Btn.setEnabled(False)
        else:
            self.startSorting_Btn.setEnabled(True)

        self.updateSortingProgress_Label()

    def startSortingMod(self):
        self.pathSettingsContainer.setEnabled(False)
        try:
            smf.compareLists(smf.getModFileList(self.browseModFolder_LineEdit.text()),
                  smf.getGameFilesLists(self.browseBaseGameList_LineEdit.text(), self.browseUpdateList_LineEdit.text(), self.browseDLCList_LineEdit.text()),
                  self.browseOutputFolder_LineEdit.text())
        except:
            e = sys.exc_info()
            QtWidgets.QMessageBox.about(self, "Oh No! There Was An Error", "Error: " + str(e))
        else:
            QtWidgets.QMessageBox.about(self, "Sorting Completed", "Sorting completed. Please use caution when using FTPiiU.")
        finally:
            self.pathSettingsContainer.setEnabled(True)

    def saveIniFile(self):
        config = configparser.ConfigParser()
        config['PATHS'] = {'BaseGameListPath' : self.browseBaseGameList_LineEdit.text(),
              'UpdateListPath' : self.browseUpdateList_LineEdit.text(),
              'DLCListPath' : self.browseDLCList_LineEdit.text(),
              'InModFolderPath' : self.browseModFolder_LineEdit.text(),
              'OutputFolderPath' : self.browseOutputFolder_LineEdit.text()
        }

        with open(DEFAULT_INI_PATH, 'w') as configfile:
            config.write(configfile)

        QtWidgets.QMessageBox.about(self, "Save Successful", "The current file/folder paths have been saved as the default values.")

    def loadIniFile(self):
        config = configparser.ConfigParser()
        config.read(DEFAULT_INI_PATH)

        if 'BaseGameListPath' in config['PATHS']:
            self.browseBaseGameList_LineEdit.setText(config['PATHS']['BaseGameListPath'])

        if 'UpdateListPath' in config['PATHS']:
            self.browseUpdateList_LineEdit.setText(config['PATHS']['UpdateListPath'])

        if 'DLCListPath' in config['PATHS']:
            self.browseDLCList_LineEdit.setText(config['PATHS']['DLCListPath'])

        if 'InModFolderPath' in config['PATHS']:
            self.browseModFolder_LineEdit.setText(config['PATHS']['InModFolderPath'])

        if 'OutputFolderPath' in config['PATHS']:
            self.browseOutputFolder_LineEdit.setText(config['PATHS']['OutputFolderPath'])
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
