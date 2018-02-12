
from PIL import Image
import os
import shutil

#"C:\\Users\\RAVI TEJA\\Downloads\\drive-download-20180211T194222Z-001"
#"F:\\Careers\\temp"

def rename_move_images(SOURCE_DIR,DESTINATION_DIR):
    files = os.listdir(SOURCE_DIR)
    for file in files:
        try:
            pathAndFilename = os.path.join(SOURCE_DIR,file)
            time_stamp = Image.open(pathAndFilename)._getexif()[36867]
        
            directory = os.path.join(DESTINATION_DIR,time_stamp.split(' ')[0].replace(':','-'))
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            newfilename = time_stamp.replace(':','-')+" "+file
            newpathAndFilename = os.path.join(directory,newfilename)
            shutil.copy(pathAndFilename,newpathAndFilename)
            print(file," renamed to ",newfilename," and moved to ",directory)
        except Exception as e:
            continue

if __name__ == "__main__":
    SOURCE_DIR =  input("Enter the path of source directory : ")
    if SOURCE_DIR == '':
        SOURCE_DIR = os.path.dirname(os.getcwd())
    os.chdir(SOURCE_DIR)

    DESTINATION_DIR = input("Enter the path of destination directory : ")
    if DESTINATION_DIR == '':
        DESTINATION_DIR = os.path.dirname(os.getcwd())
    os.chdir(DESTINATION_DIR)

    rename_move_images(SOURCE_DIR,DESTINATION_DIR)


