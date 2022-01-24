# -*- coding: utf-8 -*-
"""
Troubleshooting the 'source should be in room'
==============================================
@author: theja
"""

#%%
# Package imports
import numpy as np 
import pyvista as pv
from stl import mesh
import pyroomacoustics as pra

#%% Load STL mesh file
path_to_stl_file = "data/smaller_slicedup_OC_evenmore_blenderfixed.stl"

material = pra.Material(energy_absorption=0.4, scattering=0.5)
the_mesh = mesh.Mesh.from_file(path_to_stl_file)
ntriang, nvec, npts = the_mesh.vectors.shape

# also load the mesh in PyVista for visualisation in case of error
cave_mesh = pv.read(path_to_stl_file)

#%% Make the 'room' from the mesh - each triangle in the mesh is a 'wall'. 

walls = []
for w in range(ntriang):
    walls.append(
        pra.wall_factory(
            the_mesh.vectors[w].T,
            material.energy_absorption["coeffs"],
            material.scattering["coeffs"],
        )
    )
#%% Make the 'room'
fs = 192000 # Hz
room = pra.Room(walls, fs=fs, max_order=1)

# Load the call emission points 
bat12_xyz = pd.read_csv('simulated_2bat_trajectories.csv')
bat1 = bat12_xyz[bat12_xyz['bat_number']==1]
bat2 = bat12_xyz[bat12_xyz['bat_number']==2].reset_index(drop=True)

#%% Make the 'room'
print('Generating Room...')
room = pra.Room(walls, fs=fs, max_order=1)
room.rt_args['receiver_radius']=0.1


#%% Visualise the 'problem' source point with pyvista

problem_point = pv.Sphere(radius=0.1, center=each_emission)

view = pv.Plotter()
view.add_mesh(cave_mesh)
view.add_mesh(problem_point,color='red')

view.show()




