import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import open3d as op3

# Generate a random point cloud
np.random.seed(0)
pcd = op3.io.read_point_cloud("110mm PVC Pipe - front.ply")
points  = np.asarray(pcd.points)

# Apply PCA to find the axis of the cylinder
pca = PCA(n_components=3)
pca.fit(points)

# Get the direction of the cylinder axis
axis = pca.components_[0]

# Project the points onto the cylinder axis
projected = np.dot(points, axis.T)

# Fit a line to the projected points
params = np.polyfit(projected, np.zeros_like(projected), 1, full=True)

# Get the center and radius of the cylinder
center = pca.mean_
radius = np.abs(params[0][0])

# Create a grid of points for plotting
theta = np.linspace(0, 2*np.pi, 100)
x = radius * np.cos(theta)
y = radius * np.sin(theta)
z = np.linspace(-5, 5, 100)
X, Y, Z = np.meshgrid(x, y, z)

# Compute the coordinates of the cylinder surface
C = np.sqrt(radius**2 - x**2 - y**2) + np.dot(center, axis)

# Plot the points and the cylinder
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='b')
ax.plot_surface(X, Y, C, color='r', alpha=0.5, cmap=cm.coolwarm) 
plt.show()
