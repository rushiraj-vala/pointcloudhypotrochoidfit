import open3d as o3d
import numpy as np

# Load the .ply file
pcd = o3d.io.read_point_cloud("110mm PVC Pipe - front.ply")

# Preprocess the point cloud data
pcd = pcd.voxel_down_sample(voxel_size=0.05)

# Fit a cylinder
pcd_tree = o3d.geometry.KDTreeFlann(pcd)
[_, idx, _] = pcd_tree.search_radius_vector_3d(pcd.points, 0.1)
cylinder_model, inliers = o3d.registration.registration_ransac_based_on_feature_matching(
        pcd, pcd, 0.05, transformation_estimation=o3d.registration.TransformationEstimationPointToPoint(False),
        init=np.eye(4), num_of_ransac_iterations=100, feature_distance_threshold=0.1,
        inlier_ratio=0.25, max_correspondence_distance=0.05, n_threads=1)

# Visualize the results
pcd_inliers = pcd.select_by_index(inliers)
o3d.visualization.draw_geometries([pcd_inliers, cylinder_model])
