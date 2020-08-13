# PhotoscanMetashapePythonPipeline
 A step by step pipeline for accessing Agisoft Photoscan/Metashpe as part of Python applications in headless mode.
 
 Code requires Photoscan or Metashape Pro version - https://www.agisoft.com/
 
 Currently there is another way, by installing directly the dedicated version from [HERE](https://agisoft.freshdesk.com/support/solutions/articles/31000148930-how-to-install-metashape-stand-alone-python-module). The code is still useful, as it contains a step by step example on:
 1. Setup triangulation
 2. Filter errors in the sparse point cloud
 3. Setup accuracies for calculating the point cloud and mesh
 4. Extract dense points, normals, faces, color
 5. Calculate the absolute scale of the 3D reconstruction from positioning data and calculate the uncertainty of the scale using the uncertainty of the positioning sensor using the method from the paper - Nikolov, I., & Madsen, C. B. (2019). Performance Characterization of Absolute Scale Computation for 3D Structure from Motion Reconstruction. In VISIGRAPP (5: VISAPP) (pp. 884-891).
 6. Slice the 3D reconstruction in 2D chunks if needed for additional processing
 
 
# Requirements

The code requires Numpy and subprocess libraries
