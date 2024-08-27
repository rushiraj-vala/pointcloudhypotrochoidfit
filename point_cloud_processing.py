import open3d as op3
import random
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from mpl_toolkits import mplot3d

# Import the point cloud and seperate the XYZ and RGB values
pcd = op3.io.read_point_cloud("110mm PVC Pipe - front.ply")
points  = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
print(len(points))

# Print the Point Cloud
plt.figure(figsize=(8,5),dpi=150)
# plt.scatter(points[:,0],points[:,1],c=colors/255,s=0.05)
# plt.show()

# Define the Number of Iterations for RANSAC
iterations = 1000

# Find the average of distances of each point w.r.t. entire cloud
from sklearn.neighbors import KDTree
tree = KDTree(np.array(points), leaf_size=2)

# find the k nearest neighbors, in our case 8
nearest_dist, nearest_ind =  tree.query(points, k=8)

print(np.mean(nearest_dist[:,1:],axis=0))   

# FINDING THE PLANE
# Generate t
idx_samples = random.sample(range(len(points)),3)
pts = points[idx_samples]
print(pts)

# Vectors from 3 point
vecA = pts[1] - pts[0]
vecB = pts[2] - pts[0]
normal = np.cross(vecA, vecB)

# co-eff of plane equation
a,b,c = normal / np.linalg.norm(normal)
d= - np.sum(normal*pts[1])

# Normal distance of each point from the plane
distance = (a*points[:,0]+b*points[:,1]+c*points[:,2]+d)/np.sqrt(a**2 + b**2 + c**2)

print(distance)

def ransac_plane(xyz, threshold=0.05, iterations=1000):
  inliers=[]
  n_points=len(xyz)
  i=1
  while i<iterations:
    idx_samples = random.sample(range(n_points), 3)
    pts = xyz[idx_samples]
    vecA = pts[1] - pts[0]
    vecB = pts[2] - pts[0]
    normal = np.cross(vecA, vecB)
    a,b,c = normal / np.linalg.norm(normal)
    d=-np.sum(normal*pts[1])
    distance = (a * xyz[:,0] + b * xyz[:,1] + c * xyz[:,2] + d
                ) / np.sqrt(a ** 2 + b ** 2 + c ** 2)
    idx_candidates = np.where(np.abs(distance) <= threshold)[0]
    if len(idx_candidates) > len(inliers):
      equation = [a,b,c,d]
      inliers = idx_candidates
    
    i+=1
    print(i)

  return equation, inliers

eq,idx_inliers=ransac_plane(points,0.005,10000)
inliers=points[idx_inliers]

mask = np.ones(len(points), dtype=bool)
mask[idx_inliers]=False
outliers=points[mask]

ax = plt.axes(projection='3d')
ax.scatter(inliers[:,0], inliers[:,1], inliers[:,2], c = 'cornflowerblue', s=0.02) 
ax.scatter(outliers[:,0], outliers[:,1], outliers[:,2], c = 'salmon', s=0.02)
plt.show()