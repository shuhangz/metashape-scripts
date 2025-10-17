import Metashape

"""


"""
MAX_CONFIDENCE = 255;
MIN_CONFIDENCE = 2;


compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

print("Script started...")
doc = Metashape.app.document
chunks = doc.chunks

for chunk in chunks:
    if chunk.enabled is True:
        cloud = chunk.dense_cloud
        cloud.setConfidenceFilter(MIN_CONFIDENCE,MAX_CONFIDENCE);
        print(chunk.label);
print("dense cloud in all chunks are filtered by confidence %d to %d" %(MIN_CONFIDENCE,MAX_CONFIDENCE))
print("Script finished...")