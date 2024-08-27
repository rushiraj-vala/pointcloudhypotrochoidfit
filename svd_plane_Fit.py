import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, RANSACRegressor
from mpl_toolkits.mplot3d import Axes3D
import open3d as op3

def best_fit_plane_ransac(points, max_trials=1000, min_samples=3, residual_threshold=1e-3):
    """
    Calculate the normal vector and distance of the best-fit plane to the origin for a point cloud
    using RANSAC algorithm.
    :param points: n x 3 array of points in 3D space
    :param max_trials: maximum number of trials for finding inliers
    :param min_samples: minimum number of samples for finding the plane
    :param residual_threshold: maximum residual to be considered as inlier
    :return: normal vector and distance of the plane from the origin
    """
    X = points[:, :2]
    y = points[:, 2]
    reg = RANSACRegressor(
        LinearRegression(),
        max_trials=max_trials,
        min_samples=min_samples,
        residual_threshold=residual_threshold
    )
    reg.fit(X, y)
    normal = np.insert(reg.estimator_.coef_, 2, -1)
    normal /= np.linalg.norm(normal)
    d = -reg.estimator_.intercept_ / normal[2]
    return normal, d

def plot_plane(normal, d, ax, color='r', alpha=0.2):
    """
    Plot the best-fit plane in 3D space.
    :param normal: normal vector of the plane
    :param d: distance from the origin
    :param ax: matplotlib 3D axis
    :param color: color of the plane
    :param alpha: transparency of the plane
    """
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(x_min, x_max), np.linspace(y_min, y_max))
    zz = (-normal[0] * xx - normal[1] * yy - d) / normal[2]
    ax.plot_surface(xx, yy, zz, color=color, alpha=alpha)

def visualize_best_fit_plane(points):
    """
    Visualize the best-fit plane for a point cloud.
    :param points: n x 3 array of points in 3D space
    """
    normal, d = best_fit_plane_ransac(points)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2])
    plot_plane(normal, d, ax)
    plt.show()

# Example usage
# Import the point cloud and seperate the XYZ and RGB values
pcd = op3.io.read_point_cloud("110mm PVC Pipe - front.ply")
points  = np.asarray(pcd.points)
visualize_best_fit_plane(points)
