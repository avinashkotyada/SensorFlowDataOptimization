from scipy.spatial import Voronoi, voronoi_plot_2d
# import matplotlib.pyplot as plt

# Set up the input points
points = [(0, 0), (1, 1)]

# Compute the Voronoi diagram
vor = Voronoi(points)

# Plot the Voronoi diagram
fig = voronoi_plot_2d(vor)
# plt.show()