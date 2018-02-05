import PhotoScan, glob, sys

# All arguments need to be enclosed in their own set of " " when executing script in Photoscan GUI
# Ex. "U:/Documents/GIS/Photoscan/" "testProject3.psx" "Folly_West_rs"
# Executing from Windows Command Line:
    # open command line in file containing photoscan executable or
    # first type path to photoscan executable then a space
    # then type -r
    # then the direct file path to the python script, include the name of script in the path, then a space
    # then type the file path to where you like your project to be saved then a space
    # then type the desired project name with a .psx extension then a space
    # then type the name of the folder where your photos are stored
    # OPTIONAL!
    # if your folder of photos has a different path than the destination folder for your project then,
    # type a space after your folder name and then type out the path to your folder
    # Ex:
    #   photoscan.exe -r U:/Documents/GIS/Photoscan/initialScript2.py U:/Documents/GIS/Photoscan/ testProject1.psx Folly_West_rs optional/alternate/filepath/to/source/folder
    #
    #   or
    #
    # C:/Program Files/Agisoft/Photoscan Pro/photoscan.exe -r U:/Documents/GIS/Photoscan/initialScript2.py U:/Documents/GIS/Photoscan/ testProject1.psx Folly_West_rs optional/alternate/path/to/source/folder
    

path = (sys.argv[1]) # user will designate the file path for their project as the first argument
docName = (sys.argv[2]) # user will designate the file name for their project with a .psx file type ending
sourceFolder = (sys.argv[3]) # user will designate the name of the folder where their source folders are stored
sourceFolderPath = ""

if(len(sys.argv) == 4):
    sourceFolderPath = path + sourceFolder + "/*"
else:
    sourceFolderPath = sys.argv[4] + sourceFolder + "/*"
filePath = (path + docName)

# this block will create an instance of a Photoscan document and store that in doc,
# then it will create a new project in a designated folder, doc.save(),
# then it will open that project and add a new chunk to the project
# then creates a photo list and then a for loop will loop through the deisgnated
# photo folder and add the photos to the list.
doc = PhotoScan.app.document
doc.save(filePath)
doc.open(filePath)
chunk = PhotoScan.app.document.addChunk()
photos = []
for photo in glob.glob(path + sourceFolder + "/*"):
    photos.append(photo)

# this block will add all the photos from the list to the chunk,
# it then will perform the function that matches images for the chunk frame
# after immages have been matched then it perfroms photo alignment for the chunck and
# when the alignment is completed a dense cloud in created using the data in the chunk
# for time saving purposes, quality has been set equal to MediumQuality.
chunk.addPhotos(photos)
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, generic_preselection=True, reference_preselection=False)
chunk.alignCameras()
#chunk.buildDenseCloud(quality=PhotoScan.MediumQuality, filter=PhotoScan.FilterMode.NoFiltering )
chunk.buildDepthMaps()
chunk.buildDenseCloud()

doc.save()



# http://www.agisoft.com/pdf/photoscan_python_api_1_3_3.pdf
# http://www.agisoft.com/pdf/photoscan_python_api_1_3_1.pdf
# edited last by Justin Dowd 01/25/18 jmdowd@g.clemson.edu
# Tested on Photoscan Pro Version 1.3.1
