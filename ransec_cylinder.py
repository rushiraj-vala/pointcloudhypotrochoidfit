from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.utils import check_random_state
from sklearn.linear_model import RANSACRegressor

# Generate sample data
np.random.seed(0)
n_samples = 1000
X = np.random.normal(size=(n_samples, 3))
y = np.sqrt(X[:, 0]**2 + X[:, 1]**2) + X[:, 2]

# Define the custom RANSAC estimator
class CylinderRegressor(RANSACRegressor):
    def fit(self, X, y):
        super().fit(X[:, :2], y)

        # Compute the cylinder parameters from the linear regression
        self.center_point_ = np.append(self.estimator_.intercept_, 0)
        self.direction_ = np.append(self.estimator_.coef_, -1)
        distances = pairwise_distances(X[:, :2], self.estimator_.predict(X[:, :2]))
        self.radius_ = np.median(np.min(distances, axis=1))
        self.offset_ = np.median(X[:, 2] - self.estimator_.predict(X[:, :2]))

    def predict(self, X):
        distances = pairwise_distances(X[:, :2], self.estimator_.predict(X[:, :2]))
        return np.sign(self.offset_)*np.sqrt(self.radius_**2 - np.min(distances, axis=1)**2) + self.estimator_.predict(X[:, :2])[:, 1]

# Define the RANSAC estimator
ransac = CylinderRegressor()
ransac.fit(X, y)

# Extract the inliers and outliers
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

# Fit a linear regression model to the inliers
reg = LinearRegression().fit(X[inlier_mask], y[inlier_mask])

# Visualize the data and the cylinder
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[inlier_mask, 0], X[inlier_mask, 1], X[inlier_mask, 2], c='blue', alpha=0.5)
ax.scatter(X[outlier_mask, 0], X[outlier_mask, 1], X[outlier_mask, 2], c='red', alpha=0.5)
cylinder_direction = ransac.direction_
cylinder_center = ransac.center_point_
cylinder_radius = ransac.radius_
cylinder_offset = ransac.offset_
cylinder_height = np.linalg.norm(X.max(axis=0) - X.min(axis=0))

cylinder = np.empty((100, 3))
z = np.linspace(0, cylinder_height, 100)
theta = np.linspace(0, 2 * np.pi, 100)
theta_grid, z_grid = np.meshgrid(theta, z)
cylinder[:, 0] = cylinder_radius * np.cos(theta_grid).ravel() + cylinder_center[0]
cylinder[:, 1] = cylinder_radius * np.sin(theta_grid).ravel() + cylinder_center[1]
cylinder[:, 2] = cylinder_offset + z_grid.ravel()*cylinder_direction[2] + cylinder_center[2]

ax.plot_trisurf(cylinder[:, 0], cylinder[:, 1], cylinder[:, 2], color='grey', alpha=0.5)
plt.show()