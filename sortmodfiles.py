import sys
import os
import string
import errno
import shutil

PROGRAM_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_BASEGAMELIST_PATH = PROGRAM_DIR + os.sep + "filelists" + os.sep + "basegamelist.txt"
DEFAULT_UPDATELIST_PATH = PROGRAM_DIR + os.sep + "filelists" + os.sep + "updatelist.txt"
DEFAULT_DLCFILELIST_PATH = PROGRAM_DIR + os.sep + "filelists" + os.sep + "DLCfilelist.txt"

def getModFileList(modpath):
	modFileList = []
	for root, dirs, files in os.walk(modpath):
		for f in files:
			modFileList.append(os.path.join(root, f))
	return modFileList

def getGameFilesLists(bgl=DEFAULT_BASEGAMELIST_PATH, udl=DEFAULT_UPDATELIST_PATH, dlcl=DEFAULT_DLCFILELIST_PATH):
	with open(bgl, "r") as bgl:
		bgFileList = bgl.readlines()

	with open(udl, "r") as udl:
		udFileList = udl.readlines()

	with open(dlcl, "r") as dlcl:
		dlcFileList = dlcl.readlines()

	return(bgFileList, udFileList, dlcFileList)

def compareLists(modFileList, gameLists, ftpiiu_dir, statusLabel=None, statusBar=None):

	updateData_dir = ftpiiu_dir + os.sep + "Update Data"
	#updateDataContent_dir = updateData_dir + os.sep + "Content"

	baseGame_dir = ftpiiu_dir + os.sep + "Base Game"
	#baseGameContent_dir = baseGame_dir + os.sep + "Content"

	dlcData_dir = ftpiiu_dir + os.sep + "DLC Data"
	#dlcDataContent_dir = dlcData_dir + os.sep + "Content"

	customFiles_dir = ftpiiu_dir + os.sep + "Custom Files (put into update folder)"
	#customFilesContent_dir = customFiles_dir + os.sep + "Content"


	if not os.path.isdir(ftpiiu_dir):
		os.mkdir(ftpiiu_dir)
		print("Created FTPiiU_Easy_Install directory.")
	else:
		print("Warning: Using existing FTPiiU_Easy_Install directory.")

	for f in modFileList:
		inGameData = False
		inUpdateData = False
		inDLCData = False

		textStatus = "Comparing File " + str(modFileList.index(f)) + " of " + str(len(modFileList))
		if statusBar != None:
			statusBar.setValue((float(modFileList.index(f)) / float(len(modFileList))) * 100)
			statusLabel.setText(textStatus)

		if (modFileList.index(f) % 10) == 0:
			
			if statusBar == None:
				print(textStatus)
			

		for bgf in gameLists[0]:
			if pathsMatch(f, bgf):
				inGameData = True

		for udf in gameLists[1]:
			if pathsMatch(f, udf):
				inUpdateData = True

		for dlcf in gameLists[2]:
			if pathsMatch(f, dlcf):
				inDLCData = True

		if inUpdateData:
			moveFile(updateData_dir, f)

		elif inGameData and (not inUpdateData):
			moveFile(baseGame_dir, f)

		elif inDLCData:
			moveFile(dlcData_dir, f)

		elif (not inUpdateData) and (not inGameData) and (not inDLCData):
			moveFile(customFiles_dir, f)

def pathsMatch(path1, path2):
	installPath1 = path1.lower().split("content")[1].rstrip()
	installPath2 = path2.lower().split("content")[1].rstrip()

	return (installPath1 == installPath2)

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def moveFile(folder, f):
	if not os.path.isdir(folder):
		os.mkdir(folder)

	if "Content" in f:
		newFilePath = folder + os.sep + "content" + f.split("Content")[1]
	elif "content" in f:
		newFilePath = folder + os.sep + "content" + f.split("content")[1]

	print(newFilePath)
	mkdir_p(os.path.dirname(os.path.abspath(newFilePath)))
	shutil.copy2(f, newFilePath)


if __name__ == "__main__":
	modcontentpath = sys.argv[1]
	workingFolder = os.path.dirname(os.path.realpath(__file__)) + os.sep + "FTPiiU_Easy_Install"
	compareLists(getModFileList(modcontentpath), getGameFilesLists(), workingFolder)
