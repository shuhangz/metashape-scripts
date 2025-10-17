import Metashape
import os

# 1. Iterate all camera objects in the chunk, group each camera object according to its storage path (camera.photo path), and calculate the average xy coordinates (camera.reference.location.x and camera.reference.location.y) of all cameras in each group, and output these averages on the console.
# 2. Modify the xy coordinates of all cameras in other groups except the first group, so that the average values of all camera coordinates in other groups are equal to that of the cameras in the first group.

def main():
    # Initialize Metashape and get the current chunk
    doc = Metashape.app.document
    chunk = doc.chunk

    # Dictionary to hold cameras by their photo path
    camera_groups = {}

    # Iterate over all cameras and group them by their containing folder
    for camera in chunk.cameras:
        if camera.photo is not None:
            folder = os.path.dirname(camera.photo.path)  # Get the containing folder
            if folder not in camera_groups:
                camera_groups[folder] = []
            camera_groups[folder].append(camera)

    # Calculate and output average xy coordinates for each group
    averages = {}
    for path, cameras in camera_groups.items():
        x_sum = sum(camera.reference.location.x for camera in cameras)
        y_sum = sum(camera.reference.location.y for camera in cameras)
        count = len(cameras)
        avg_x = x_sum / count
        avg_y = y_sum / count
        averages[path] = (avg_x, avg_y)
        print(f"Group: {path}, Average X: {avg_x}, Average Y: {avg_y}")

    # Move cameras in other groups in the xy direction to match the first group's averages
    first_group_avg = next(iter(averages.values()))  # Get the average of the first group
    print(f"First group average: {first_group_avg}")

    for camera in chunk.cameras:
        if camera.photo is not None:
            folder = os.path.dirname(camera.photo.path)
            if folder in averages:
                delta_x = first_group_avg[0] - averages[folder][0]
                delta_y = first_group_avg[1] - averages[folder][1]
                # print(f"Moving camera in group {folder} by ({delta_x}, {delta_y})")
                coord = camera.reference.location
                camera.reference.location = Metashape.Vector(
                [coord.x + delta_x, coord.y + delta_y, coord.z])    


if __name__ == "__main__":
    main()
    print("Script completed.")