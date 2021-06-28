## Generating Events

Particles are generated using a Geant4 macro with edep-sim acting as the wrapper, simulating the energy deposition in some detector.

```more about how to generate particles```

## Running the simulation

After generating your particle macro, use the following line in bash to generate a root file which contains the following:

`edep-sim -u -e 10 -g Module0.gdml -o output.root singlemuon.mac`

`-e 10` generates 10 muons (see previous section for how to generate)

`-g Module0.gdml` loads the geometry for the dectector we want to use

`-o output.root` specifices the name of the output file, which at this point should be a .root file. Possible updates coming soon

`-u` does an update before running the macros 

Once the root file has been produced, it must be converted to a friendlier format. The following script should be run:
`python3 dumpTree.py output.root output.h5`

This runs a script that converts the root file to an h5py format .h5. See `explore_h5.ipynb` for an example of how to open and read h5py files. This step is necessary since the pipeline for larnd-sim, the other half of the detector simulation process, takes in h5 files containing numpy arrays as input.

## What's in the file? 

The root file contains all of the following:
```
TG4Primary Particle Object Properties:
Class
Track Id
Name
PDG Code
Momentum (X,Y,Z,E,P,M)

TG4PrimaryVertex Object Properties:
Class
Position
Generator
Reaction
Filename
InteractionNumber
Depth (whatever that means)

TG4TrajectoryPoint Object Properties
Class
Position (X,Y,Z,T)
Momentum(X,Y,Z,Mag)
Process
Subprocess

TG4Trajectory Object
Class
TrackId
ParentId
Name
PGD Code
Initial Momentum(X,Y,Z,E,P,M)

TG4 HitSegment
Class
Primary ID
Energy Deposit
Secondary Deposit
Track Length
Start(X,Y,Z,T)
Stop(X,Y,Z,T)
Contributor
```


The h5 file generates the following properties as a numpy array:

```
Segments:
eventID
trackID
x_start
y_start
z_start
x_end
y_end
z_end
dE
t
t_start
t_end
dx = sqrt(xd**2 + yd**2 + zd**2)
x = (x_start+x_end)/2
y = (y_start+y_end)/2
z = (z_start+z_end)/2
dEdx = Energy deposited/dx if dx>0 else 0
pdgId
n_electrons
long_diff
tran_diff
pixel_plane
```


## Ideas for streamlining this process
1) Combine the root to h5 process. This is a bit annoying.
2) Make particle generation script which allows us to specify standard geometry, particle type (assumes direction) and energy (for now simply monoenergtic).