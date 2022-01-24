# -*- coding: utf-8 -*-
"""
Code to reproduce the Source not in room issue in Pyroomacoustics
=================================================================

"""

#%%
# Package imports
import numpy as np 
import pandas as pd
from stl import mesh
import pyroomacoustics as pra

#%% Load STL mesh file
path_to_stl_file = "data/smaller_slicedup_OC_evenmore_blenderfixed.stl"

material = pra.Material(energy_absorption=0.4, scattering=0.5)
the_mesh = mesh.Mesh.from_file(path_to_stl_file)
ntriang, nvec, npts = the_mesh.vectors.shape


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
# Load the call emission points 
bat12_xyz = pd.read_csv('simulated_2bat_trajectories.csv')
bat1 = bat12_xyz[bat12_xyz['bat_number']==1]
bat2 = bat12_xyz[bat12_xyz['bat_number']==2].reset_index()

#%% Make the 'room'
print('Generating Room...')
room = pra.Room(walls, fs=fs, max_order=1)
room.rt_args['receiver_radius']=0.1


#%% Each point in space that the bats fly are microphones

bat1_t_emissions = np.arange(0,bat1.shape[0],10) # call emitted every 10 frames

# make microphone array - with all points of sound reception 

bat1_callhearing_points = bat1.loc[bat1_t_emissions,['x','y','z']].to_numpy()
bat2_noncallhearing_points = bat2.loc[bat1_t_emissions,['x','y','z']].to_numpy()

mic_array = np.row_stack((bat1_callhearing_points,
                          bat2_noncallhearing_points)).T

# All points in space when bat 1 emitted a call
bat1_call_emission_points = bat1.loc[bat1_t_emissions,['x','y','z']].to_numpy()

#%%
# Add sources and microphone array to room
room.add_microphone_array(mic_array)

for i,each_emission in enumerate(bat1_call_emission_points):
    room.add_source(bat1_call_emission_points[i])

#%% Run sound propagation
print('running sound propagation...')
room.image_source_model()
room.ray_tracing()
room.compute_rir()
print('done with sound prop...')







