#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Creates meshes on a cube.
'''
import numpy as np
#from math import sin, pi, atan, sqrt
import time

import voropy
# ==============================================================================
def _main():

    # get the file name to be written to
    args = _parse_options()

    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # create the mesh data structure
    print 'Create mesh...',
    start = time.time()
    if args.nx != 0:
        mesh = _canonical(l, [args.nx, args.nx, args.nx])
    elif args.maxvol != 0.0:
        mesh = _meshpy(l, args.maxvol)
    else:
        raise RuntimeError('Set either -c or -m.')
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    num_nodes = len(mesh.nodes)
    print '\n%d nodes, %d elements\n' % (num_nodes, len(mesh.cellsNodes))

    # write the mesh with data
    print 'Write to file...',
    start = time.time()
    mesh.write(args.filename)
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return
# ==============================================================================
def _canonical(l, N):
    '''Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    '''

    # Generate suitable ranges for parametrization
    x_range = np.linspace( -0.5*l[0], 0.5*l[0], N[0] )
    y_range = np.linspace( -0.5*l[1], 0.5*l[1], N[1] )
    z_range = np.linspace( -0.5*l[2], 0.5*l[2], N[2] )

    # Create the vertices.
    num_nodes = len(x_range) * len(y_range) * len(z_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 3)))
    k = 0
    for x in x_range:
        for y in y_range:
            for z in z_range:
                nodes[k] = np.array([x, y, z])
                k += 1

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See <http://private.mcnet.ch/baumann/Splitting%20a%20cube%20in%20tetrahedras2.htm>.
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    num_cells = 5 * (N[0]-1) * (N[1]-1) * (N[2]-1)
    cellNodes = np.empty(num_cells, dtype=np.dtype((int,4)))
    l = 0
    for i in range(N[0] - 1):
        for j in range(N[1] - 1):
            for k in range(N[2] - 1):
                # Switch the element styles to make sure the edges match at
                # the faces of the cubes.
                if ( i+j+k ) % 2 == 0:
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1])
                    l += 1
                else:
                    # Like the previous one, but flipped along the first
                    # coordinate: i+1 -> i, i -> i+1.
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1,
                                             N[2] * ( N[1]*i     + j   ) + k+1])
                    l += 1

    mesh = voropy.mesh3d(nodes, cellNodes)

    return mesh
# ==============================================================================
def _meshpy(l, max_volume):

    import meshpy.tet

    # Corner points of the cube
    points = [ ( -0.5*l[0], -0.5*l[1], -0.5*l[2] ),
               (  0.5*l[0], -0.5*l[1], -0.5*l[2] ),
               (  0.5*l[0],  0.5*l[1], -0.5*l[2] ),
               ( -0.5*l[0],  0.5*l[1], -0.5*l[2] ),
               ( -0.5*l[0], -0.5*l[1],  0.5*l[2] ),
               (  0.5*l[0], -0.5*l[1],  0.5*l[2] ),
               (  0.5*l[0],  0.5*l[1],  0.5*l[2] ),
               ( -0.5*l[0],  0.5*l[1],  0.5*l[2] ) ]
    facets = [ [0,1,2,3],
               [4,5,6,7],
               [0,4,5,1],
               [1,5,6,2],
               [2,6,7,3],
               [3,7,4,0] ]

    # create the mesh
    print 'Create mesh...',
    start = time.time()
    info = meshpy.tet.MeshInfo()
    info.set_points( points )
    info.set_facets( facets )
    meshpy_mesh = meshpy.tet.build(info, max_volume = max_volume )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    #print 'Recreate cells to make sure the mesh is Delaunay...',
    #start = time.time()
    #mesh.recreate_cells_with_qhull()
    #elapsed = time.time()-start
    #print 'done. (%gs)' % elapsed

    return voropy.mesh3d(meshpy_mesh.points, meshpy_mesh.elements)
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Construct a trival tetrahedrization of a cube.' )


    parser.add_argument( 'filename',
                         metavar = 'FILE',
                         type    = str,
                         help    = 'file to be written to'
                       )

    parser.add_argument( '--canonical', '-c',
                         metavar = 'NX',
                         dest='nx',
                         nargs='?',
                         type=int,
                         const=0,
                         default=0,
                         help='canonical tetrahedrization with NX discretization points along each axis'
                       )

    parser.add_argument( '--meshpy', '-m',
                         metavar = 'MAXVOL',
                         dest='maxvol',
                         nargs='?',
                         type=float,
                         const=0.0,
                         default=0.0,
                         help='meshpy tetrahedrization with MAXVOL maximum tetrahedron volume'
                       )

    args = parser.parse_args()

    return args
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
