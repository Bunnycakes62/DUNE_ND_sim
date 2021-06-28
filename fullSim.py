import os

import configargparse

# Example Syntax
# run fullSim.py --event_gen edep-sim_scripts/macros/singlemuon.mac

p = configargparse.ArgumentParser()

p.add_argument('--num_events', type=int, default=1, help='the number of times you want the particle generator to run')
p.add_argument('--geometry', type=str, default='./edep-sim_scripts/Module0.gdml' , help='Name of the geometry file as a .gdml file')
p.add_argument('--output', type=str, default='output', help='Name of the output root file. This is saved as an intermediary step.')
p.add_argument('--event_gen', type=str, required=True, help='Name of the macro file where event generation information is stored. File is of the form .mac')
p.add_argument('--pixel_layout', type=str, default='multi_tile_layout-2.2.16.yaml', 
               help='The pixel layout of the detector stored in larnd-sim_scripts. Default is multi_tile_layout-2.2.16.yaml')
p.add_argument('--detector_prop', type=str, default='module0.yaml', help='Detector properties stored in larnd-sim_scripts. Default is module0.yaml')

opt = p.parse_args()
edep_path = './edep-sim_scripts'
larnd_path = './larnd-sim_scripts'

''' 
    STEP 1:

    Call edepsim. Has a CLI. Input is a geometry file, particle macro file, number of events, and output file.

    Example syntax:
    edep-sim -u -e 10 -g Module0.gdml -o output.root muon-50.mac
    
    Input: 
        num_events -> int
        geometry -> .gdml file
        output -> .root file
        event_gen -> .mac file
    
'''

if '.' in opt.output:
    opt.output = opt.output.slice['.'][0]
    
# Make directory if it doesn't exist
if not os.path.exists('./output/edepsim/'):
    os.makedirs('./output/edepsim/')
if not os.path.exists('./output/larndsim/'):
    os.makedirs('./output/larndsim/')


print('Generating edep-sim outputs...')    
os.system(f'edep-sim -u -e {opt.num_events} -g {opt.geometry} -o ./output/edepsim/{opt.output}.root {opt.event_gen}')
print('Complete.')


''' 
    STEP 2:

    Call dumpTree.py. Once the root file has been produced, it must be converted to a friendlier format. The following script should be run:

    Example syntax:
    `python3 dumpTree.py output.root output.h5`

    Input: 
        output -> .root file
   
    Output:
        output.h5 -> same name as output file name, just with an h5 extension
'''


print('Dumping edepsim outputs into h5 file...')
os.system(f'python3 {edep_path}/dumpTree.py ./output/edepsim/{opt.output}.root ./output/edepsim/{opt.output}.h5')
print('Complete.')


'''
    STEP 3: 
    Run through the LArNDSIM detector simulator. 
    
    Example syntax:
        'python3 simulate_pixels.py ../edep-sim_scripts/output.h5 multi_tile_layout-2.2.16.yaml module0.yaml --output_filename larndsim_test.h5'
        
    Input:
        file_in -> .h5 file; output of edep-sim_script
        pixel_layout -> .yaml file; contains the pixel layout for the detector
        detector_prop -> .yaml file; contains the detector properties
    
    
    Output: 
        output -> .h5 file 

'''
# Have to change directories because original package uses relative paths.
print('Feeding edepsim outputs in larndsim pipeline...')
os.chdir(larnd_path)
os.system(f'python3 simulate_pixels.py ../output/edepsim/{opt.output}.h5 {opt.pixel_layout} {opt.detector_prop} --output_filename ../output/larndsim/{opt.output}.h5')
print('Complete.')



# Run through visualization function
