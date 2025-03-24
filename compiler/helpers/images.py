from pathlib import Path
import os, re, shutil, logging
from config import failedImages
from config import IGNORE_FOLDERS, ERROR_IMAGE_NOT_USED, ERROR_IMAGE_NOT_FOUND, TODO_ITEMS_ICON, IMAGE_REGEX
from report.table import createImageTableTow


"""
Search for image links in the markdown content, and copy the images from the source/
folder to the build/ folder, preserving the folder structure.

Args:
    content (str): Content of the markdown file.
    src_dir_name (str): Source directory (only the name of the folder itself)
    dest_dir_name (str): Destination directory (only the name of the folder itself)
"""
def copyImages(content, srcDir, destDir):
    errors = []
    if content is None:
        return errors
    
    imageLinks = re.findall(IMAGE_REGEX, content)

    for imageLink in imageLinks:
        if imageLink[0]:
            imagePath = imageLink[0].strip()
        elif imageLink[2]:
            imagePath = imageLink[2].strip()

        if not imagePath:
            continue

        if imagePath.startswith('http://') or imagePath.startswith('https://'):
            continue

        foundImagePath = None
        for root, dirs, files in os.walk(srcDir):
            if imagePath in files:
                foundImagePath = Path(root) / imagePath
                break

        if foundImagePath and foundImagePath.exists():
            relativePath = foundImagePath.relative_to(srcDir)
            newImagePath = destDir / relativePath
            newImagePath.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy(foundImagePath, newImagePath)
        else:
            error_msg = f"{ERROR_IMAGE_NOT_FOUND} `{imagePath}`"
            logging.warning(error_msg)
            errors.append(ERROR_IMAGE_NOT_FOUND)

    return errors

"""
Fills the image Report with data from the images in the folders
"""
def fillFailedImages(srcDir, destDir):
    srcDirPath = Path(srcDir).resolve()
    destDirPath = Path(destDir).resolve()
    
    srcImages = getImagesInFolder(srcDirPath)
    destImages = getImagesInFolder(destDirPath)

    for image in srcImages: 
        if str(image.stem) not in {str(img.stem) for img in destImages}:
            logging.warning(f"{ERROR_IMAGE_NOT_USED} `{image.stem}`")
            failedImages.append(createImageTableTow(TODO_ITEMS_ICON, image, srcDirPath, ERROR_IMAGE_NOT_USED))

# Helper method to populate the image report
def getImagesInFolder(dir):
    folders = [folder for folder in Path(dir).rglob("src") if folder.is_dir()]

    images = set()
    
    for folder in folders:
        if any(ignoreFolder in str(folder) for ignoreFolder in IGNORE_FOLDERS):
            continue
        
        images.update(filePath for filePath in folder.rglob("*")) 
    return images
