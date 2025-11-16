import numpy as np
BEV_IMAGE_BEV_SCALE = 5
BEV_RANGE = [-50, 50, -25, 25]


def plot_lidar_bev_map(unprojected_lidar):
    """
    Create a BEV visualization of lidar points with proper ego car positioning.
    Uses the same coordinate system and scale as other BEV visualizations.
    """
    # Create LiDAR BEV image using the BEV range-based structure (consistent with other BEV functions)
    lidar_bev = np.ones((
        BEV_IMAGE_BEV_SCALE * (BEV_RANGE[1] - BEV_RANGE[0]),
        BEV_IMAGE_BEV_SCALE * (BEV_RANGE[3] - BEV_RANGE[2]),
        3
    ), dtype=np.int32) * 255

    for lidar_point in unprojected_lidar:
        # Skip points that are all zeros (padding)
        if np.all(lidar_point[:3] == 0):
            continue

        # Extract x, y coordinates (world coordinates) and convert to float scalars
        world_x = float(lidar_point[0])
        world_y = float(lidar_point[1])

        # Apply the EXACT same coordinate transformation as draw_annotation_bev:
        # points = bev_scale * (-points[:, :2] + np.array([bev_range[1], bev_range[3]]))
        points = (BEV_IMAGE_BEV_SCALE * (-np.array([world_x, world_y]) +
                                         np.array([BEV_RANGE[1], BEV_RANGE[3]])))

        # Convert to integer coordinates
        x1 = int(points[0])
        y1 = int(points[1])

        # Check bounds after transformation
        if (x1 < 0 or y1 < 0 or
            x1 >= lidar_bev.shape[0] or
            y1 >= lidar_bev.shape[1]):
            continue

        # Use the same coordinate indexing as draw_annotation_bev:
        # cv2.line(image, pt1=(y1, x1), pt2=(y2, x2), ...)
        # This means image[x1, y1] for point plotting
        lidar_bev[x1, y1] = [0, 0, 255]

    # Add ego car using the standard _draw_ego_vehicle function
    # _draw_ego_vehicle(
    #     image=lidar_bev,
    #     map_size=self.bev_range,
    #     scale=self.bev_image_bev_scale,
    #     use_bgr=True  # LiDAR uses RGB format
    # )

    lidar_bev = lidar_bev.astype(np.uint8)
    return lidar_bev
