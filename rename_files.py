import os

def rename_files() :
	# get file names from the folder

	file_list = os.listdir(r"/Users/PammuTeha/Downloads/prank")

	# get current path 
	saved_path = os.getcwd()
	print(saved_path)
	os.chdir(r"/Users/PammuTeha/Downloads/prank")

	for file_name in file_list :
		os.rename(file_name,file_name.translate(None,"0123456789"))

	os.chdir(saved_path)

rename_files()