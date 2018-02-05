import PhotoScan, glob

docName = "testProject.psx"
sourceFolder = "Folly_West_rs"

doc = PhotoScan.app.document
doc.open("./" + docName)
chunk = PhotoScan.app.document.addChunk()
photos = []
for photo in glob.glob(sourceFolder + "/*"):
    photos.append(photo)

chunk.addPhotos(photos)
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, generic_preselection=True, reference_preselection=False)
chunk.alignCameras()
chunk.buildDenseCloud(quality=PhotoScan.MediumQuality, filter=PhotoScan.FilterMode.NoFiltering )
chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation)
chunk.buildUV(mapping=PhotoScan.GenericMapping) #find out what this is
chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=8192)
doc.save()

# Need to export dense cloud as .las
# chunk.exportPoints() I think this is it, p24 in api doc

# exportCameras function?

# http://www.agisoft.com/pdf/photoscan_python_api_1_3_3.pdf
