To run larnd-sim, edep-sim must first be run and a .h5 file created.

larnd-sim can be run two ways:

1) Run un a jupyter noebook; see `Pixel Induced Current.ipynb`. This is a good resource to see what is going on more indepth and to see some plots of the final product.

2) Run the `simulate_pixels.py` script in a console or terminal. The usage is the following:

Usage: simulate_pixels.py INPUT_FILENAME PIXEL_LAYOUT DETECTOR_PROPERTIES `<flags>`
  optional flags:        --output_filename | --n_tracks
    
So, for example:
                            input edep-sim file                                       detector properties
                                      |                                                        |
                                      V                                                        V
    'python3 simulate_pixels.py ../edep-sim_scripts/output.h5 multi_tile_layout-2.2.16.yaml module0.yaml --output_filename larndsim_test.h5'
                                                                    ^
                                                                    |                             
                                                        pixel layout for detector 
    
The source for larnd-sim is located [here](https://github.com/DUNE/larnd-sim). Module0 corresponds to the prototype DUNE Near Detector geometry. There also exists corresponding files for a single TPC.
    
After running the `simulate_pixels.py`, we need to convert our files to evd files (event display files). To do this use the `to_evd_file.py` with the following syntax:
    
    `python3 event-display/to_evd_file.py --in_filename larndsim_test.h5 --out_filename larndsim_test_evd.h5 --geometry_file multi_tile_layout-2.2.16.yaml`

Then run the event-display scipt as follows:

    'python3 event-display/quick_display.py -i larndsim_test_evd.h5'
    