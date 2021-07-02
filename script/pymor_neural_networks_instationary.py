#!/usr/bin/env python
# This file is part of the pyMOR project (https://www.pymor.org).
# Copyright 2013-2021 pyMOR developers and contributors. All rights reserved.
# License: BSD 2-Clause License (https://opensource.org/licenses/BSD-2-Clause)

import numpy as np
from typer import Argument, run

from pymor.basic import *
from pymor.core.config import config
from pymor.core.exceptions import TorchMissing


def main(
    grid_intervals: int = Argument(10, help='Grid interval count.'),
    time_steps: int = Argument(
        10, help='Number of time steps used for discretization.'),
    training_samples: int = Argument(
        100, help='Number of samples used for training the neural network.'),
    validation_samples: int = Argument(
        100, help='Number of samples used for validation during the training phase.'),
):
    """Model oder reduction with neural networks for an instationary problem

    Using the approach by Hesthaven and Ubbiali.
    """
    if not config.HAVE_TORCH:
        raise TorchMissing()

    fom = create_fom(grid_intervals, time_steps)

    parameter_space = fom.parameters.space(1., 2.)

    from pymor.reductors.neural_network import NeuralNetworkInstationaryReductor

    training_set = parameter_space.sample_uniformly(training_samples)
    validation_set = parameter_space.sample_randomly(validation_samples)

    reductor = NeuralNetworkInstationaryReductor(
        fom, training_set, validation_set, basis_size=10)
    rom = reductor.reduce(hidden_layers='[30, 30, 30]', restarts=100)

    test_set = parameter_space.sample_randomly(10)

    speedups = []

    import time

    print(f'Performing test on set of size {len(test_set)} ...')

    U = fom.solution_space.empty(reserve=len(test_set))
    U_red = fom.solution_space.empty(reserve=len(test_set))

    for mu in test_set:
        tic = time.time()
        U.append(fom.solve(mu))
        time_fom = time.time() - tic

        tic = time.time()
        U_red.append(reductor.reconstruct(rom.solve(mu)))
        time_red = time.time() - tic

        speedups.append(time_fom / time_red)

    absolute_errors = (U - U_red).norm2()
    relative_errors = (U - U_red).norm2() / U.norm2()

    print(f'Average absolute error: {np.average(absolute_errors)}')
    print(f'Average relative error: {np.average(relative_errors)}')
    print(f'Median of speedup: {np.median(speedups)}')


def create_fom(grid_intervals, time_steps):
    problem = burgers_problem()

    print('Discretize ...')
    discretizer = discretize_instationary_fv
    fom, _ = discretizer(problem, diameter=1. / grid_intervals, nt=time_steps)

    return fom


if __name__ == '__main__':
    run(main)

    # OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
    # OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program.
    #
    # That is dangerous, since it can degrade performance or cause incorrect results.
    # The best thing to do is to ensure that only a single OpenMP runtime is linked into the process,
    # e.g. by avoiding static linking of the OpenMP runtime in any library.
    # As an unsafe, unsupported, undocumented workaround
    # you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute,
    # but that may cause crashes or silently produce incorrect results.
    # For more information, please see http://www.intel.com/software/products/support/.
