import Metashape

# Checking compatibility
compatible_major_version = "1.5"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

doc = Metashape.app.document
if not len(doc.chunks):
    raise Exception("No chunks!")

print("Script started...")
chunk = doc.chunk

for camera in chunk.cameras:
    if camera.reference.location:
        coord = camera.reference.location
        camera.reference.location = None

print("Script finished!")