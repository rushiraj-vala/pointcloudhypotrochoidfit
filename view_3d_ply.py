import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

pcd = o3d.io.read_point_cloud("test new1.ply")
pcd_1= pcd.voxel_down_sample(voxel_size=0.01)
points  = np.asarray(pcd_1.points)
colors = np.asarray(pcd_1.colors)
print(len(points))

# # Print the Point Cloud
# plt.figure(figsize=(8,5),dpi=150)
# plt.scatter(points[:,0],points[:,1],c=colors/255,s=0.05)
# plt.show()

print(colors[0])

# filter based on color
def color_filter(point,color):
    final_points = []
    for i in range(len(color)):
        if color[i][2] > 0.98 and color[i][1]<0.1:
            final_points.append(point[i])
    print(len(final_points))
    return final_points

final_points = np.asarray(color_filter(points,colors))
# o3d.visualization.draw_geometries([pcd])

ax = plt.axes(projection='3d')
ax.scatter(final_points[:,0], final_points[:,1], final_points[:,2], c = 'blue', s=0.1) 
ax.set_xlim((-0.5,0.5))
ax.set_ylim((-0.5,0.5))
plt.show()