# Script allows users to add an offset in three directions (XYZ) to ALL
# the cameras in the Reference Panel.
#
# Note that this scripts does not apply any check to the inputs and adds an
# arbitrary value to the camera coordinates, regardless of the Coordinate
# Reference System of the Project/Cameras.
# e.g., if the CRS is a Local System or a Cartographic Reference System,
# one may provide an offset in meters, respectively for the East, North
# and altitude direction.
# if the CRS is WGS84, one has to provide the shift in degreees for
# latitude and longitude and meters for altitude.
#
# This script may be useful when one has to correct (e.g., due to a base shift)
# the coordinates of a UAV camera acquired by RTK and saved in image exif
#
# Author: Francesco Ioli (Politecnico di Milano), francesco.ioli@polimi.it
#  01/09/2022


import Metashape

print("Script started...")

# Checking compatibility
compatible_major_version = "2.2"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


def get_input(axis_name):
    offset = Metashape.app.getFloat(
        "Please specify offset value for axis {}:".format(axis_name), 0.)
    return offset


def add_offset(coord, offset):
    return Metashape.Vector([coord.x + offset.x, coord.y + offset.y, coord.z + offset.z])


def get_cartesian_crs(crs):
    cartesian_crs = crs.geoccs
    if cartesian_crs is None:
        cartesian_crs = Metashape.CoordinateSystem("LOCAL")
    return cartesian_crs


def apply_offset_to_references(items, offset):
    count = 0
    for item in items:
        if item.reference.location:
            item.reference.location = add_offset(item.reference.location, offset)
            count += 1
    return count


def apply_offset_to_chunk_transform(chunk, offset):
    has_point_cloud = bool(chunk.point_cloud)
    has_dense_cloud = bool(getattr(chunk, "dense_cloud", None))

    if not (has_point_cloud or has_dense_cloud):
        return 0

    transform = chunk.transform.matrix
    if transform is None:
        return 0

    shift = offset
    if chunk.crs:
        cartesian_crs = get_cartesian_crs(chunk.crs)
        origin = transform.translation()
        origin_coord = Metashape.CoordinateSystem.transform(origin, cartesian_crs, chunk.crs)
        shifted_origin = Metashape.CoordinateSystem.transform(add_offset(origin_coord, offset), chunk.crs, cartesian_crs)
        shift = shifted_origin - origin

    chunk.transform.matrix = Metashape.Matrix.Translation(shift) * transform
    return int(has_point_cloud) + int(has_dense_cloud)


def apply_xyz_offset():
    doc = Metashape.app.document
    chunk = doc.chunk

    if not len(doc.chunks):
        raise Exception("No chunks!")

    only_selected = False
    if len([c for c in Metashape.app.document.chunk.cameras if c.selected]) > 0:
        # if at least one camera is selected - apply offset only to selected cameras
        only_selected = True
        print("cameras selection detected - applying offset only to selected cameras...")

    offset_x = get_input("X")
    if offset_x is None:
        return
    offset_y = get_input("Y")
    if offset_y is None:
        return
    offset_z = get_input("Z")
    if offset_z is None:
        return

    offset = Metashape.Vector([offset_x, offset_y, offset_z])

    cameras = [camera for camera in chunk.cameras if not only_selected or camera.selected]
    ncameras = apply_offset_to_references(cameras, offset)

    nmarkers = 0
    nclouds = 0
    if only_selected:
        print("camera selection detected - markers and point/dense clouds were not shifted")
    else:
        nmarkers = apply_offset_to_references(chunk.markers, offset)
        nclouds = apply_offset_to_chunk_transform(chunk, offset)

    print("Offset dx={}, dy={}, dz={} applied successfully to {} cameras, {} markers and {} point/dense cloud assets".format(
        offset_x, offset_y, offset_z, ncameras, nmarkers, nclouds))


label = "Scripts/Add reference offset"
Metashape.app.addMenuItem(label, apply_xyz_offset)
print("To execute this script press {}".format(label))
