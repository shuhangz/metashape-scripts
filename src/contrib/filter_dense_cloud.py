from asyncio.windows_events import NULL
import Metashape

"""
resize the region of every chunk equas to the first chunk

"""

compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

print("Script started...")
doc = Metashape.app.document
chunks = doc.chunks
region_first =  doc.chunk.region
i=1;
while i < len(chunks):
    chunk = chunks[i]
    if chunk.enabled is True:        
        print(i)
        print(chunk.label)
        print("current region size:%f" % chunk.region.size.norm())
        print("first region size:%f" % region_first.size.norm())
        chunk.region = region_first.copy()
        # if (chunk.region.size.norm() > region_first.size.norm()):
        #     chunk.region = region_first.copy()
        # else:
        #     raise Exception("The region size of other chunks must be smaller than the first one.")
    i=i+1
      
        
print("Script finished...")