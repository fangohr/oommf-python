"""
sim.py

This module contains the Sim class which Joommf uses to run simulations


"""


import os
import subprocess
from joommf.drivers.evolver import LLG
from joommf.drivers.evolver import Minimiser
from joommf.drivers.evolver import Evolver
import joommf.fields
import joommf.odtreader as odtreader
import joommf.oommfmif as o
import textwrap
from joommf.exceptions import JoommfError
import glob

"""Soon to be supported outputs"""

time_evolver_outputs = ['time', 'Iteration', 'Stage iteration', 'Stage',
                        'Last time step', 'Simulation time',
                        'mx', 'my', 'mz',
                        'Magnetization', 'Spin']

minimizer_outputs = ['H', 'Total energy density', 'mxHxm',
                     'Magnetization', 'Spin']

field_outputs = ['UniformExchange', 'Demag', 'FixedZeeman', 'UZeeman',
                 'UniaxialAnisotropy', 'CubicAnisotropy', 'ExchangePtwise',
                 'Exchange6Ngbr']


"""
Outputs from OOMMF:

DataTable contains ALL Scalar Outputs for the given Simulation

Energies:
Oxs_UniformExchange::Energy density
Oxs_UniformExchange::Field
Oxs_UniformExchange::Max Spin Ang
Oxs_UniformExchange::Stage Max Spin Ang
Oxs_UniformExchange::Run Max Spin Ang
Oxs_UniformExchange::Energy

Oxs_Demag::Energy density
Oxs_Demag::Field
Oxs_Demag::Energy

Oxs_FixedZeeman::Energy density
Oxs_FixedZeeman::Field
Oxs_FixedZeeman::Energy

Oxs_UniaxialAnisotropy::Field
Oxs_UniaxialAnisotropy::Energy density
Oxs_UniaxialAnisotropy::Energy

Oxs_CubicAnisotropy::Energy density
Oxs_CubicAnisotropy::Field
Oxs_CubicAnisotropy::Energy

Oxs_ExchangePtwise::Energy density
Oxs_ExchangePtwise::Field
Oxs_ExchangePtwise::Energy

Oxs_UZeeman::Energy density
Oxs_UZeeman::Field
Oxs_UZeeman::Energy
Oxs_UZeeman::B
Oxs_UZeeman::Bx
Oxs_UZeeman::By
Oxs_UZeeman::Bz

Oxs_Exchange6Ngbr:Field
Oxs_Exchange6Ngbr:Energy density
Oxs_Exchange6Ngbr:Energy

Time Evolvers:
Oxs RungeKuttaEvolve:evolver:Total energy
Oxs_RungeKuttaEvolve:evolver:Energy calc count
Oxs_RungeKuttaEvolve:evolver:Max dm/dt
Oxs_RungeKuttaEvolve:evolver:dE/dt
Oxs_RungeKuttaEvolve:evolver:Delta E
Oxs_RungeKuttaEvolve:evolver:Total energy density
Oxs_RungeKuttaEvolve:evolver:Total field
Oxs_RungeKuttaEvolve:evolver:dm/dt
Oxs_RungeKuttaEvolve:evolver:mxH


Oxs_TimeDriver::Magnetization
Oxs_TimeDriver::Spin
Oxs_TimeDriver::Last time step
Oxs_TimeDriver::Simulation time
Oxs_TimeDriver::mx
Oxs_TimeDriver::my
Oxs_TimeDriver::mz
Oxs_TimeDriver::Iteration
Oxs_TimeDriver::Stage iteration
Oxs_TimeDriver::Stage

Minimisation Evolvers:
Oxs_CGEvolve::H
Oxs_CGEvolve::Total energy density
Oxs_CGEvolve::mxHxm
Oxs_MinDriver::Magnetization
Oxs_MinDriver::Spin

"""


class Sim(object):

    def __init__(self, mesh, Ms, name=None, debug=False):
        self.mesh = mesh
        self.Ms = Ms
        self.name = name
        self.energies = []
        self._oommf_stdout = ''
        self._oommf_stderr = ''
        self.field_outputs = []
        self.evolver_outputs = []
        self.evolver = None
        self._oommf_stdout = b''
        self._oommf_stderr = b''
        self.debug = debug

    def __repr__(self):
        string = "Joommf Sim Object - Mesh: {}\n Ms: {}\n ".format(
                 self.mesh.__repr__(), self.Ms)
        if self.evolver:
            string += "Evolver: {}".format(self.evolver.__repr__())
        return string

    def add_energy(self, energy):
        self.energies.append(energy)

    def set_evolver(self, evolver):
        if isinstance(evolver, Evolver):
            if self.evolver:
                print("Joommf: Evolver already set for this Sim object."
                      "\n This will be replaced with the new object")
            self.evolver = evolver

        else:
            raise JoommfError("Joommf: You must add a valid evolver from"
                              "the drivers/evolver module. If you are "
                              "trying to extend the functionality by adding"
                              "support for a new evolver, the new evolver "
                              "must be a subclass of Evolver")

    def add_output(self, output, stage=1):
        if not self.evolver:
            raise JoommfError("Joommf: You must add an evolver before "
                              "scheduling outputs, as some evolvers do "
                              "not support certain outputs.")
        if isinstance(self.evolver, LLG):
            if output in time_evolver_outputs:
                self.evolver_outputs.append([output, stage])
            elif output in minimizer_outputs:
                raise JoommfError("Joommf: This output is not supported by"
                                  " time integrator evolvers.")
        elif isinstance(self.evolver, Minimiser):
            if output in minimizer_outputs:
                self.evolver_outputs.append([output, stage])
            elif output in time_evolver_outputs:
                raise JoommfError("Joommf: This output is not supported by"
                                  " minimization evolvers.")
        elif output in field_outputs:
            self.field_outputs.append([output, stage])
        else:
            raise JoommfError("Joommf: This output was not understood."
                              " Please check that it is supported.")

    def create_mif(self, overwrite=False):
        if self.name is None:
            self.name = 'unnamed'
        if os.path.isfile(self.name + '.mif'):
            var = 1
            while os.path.isfile(self.name + str(var) + '.mif'):
                var += 1
            self.name += str(var)
        self.mif_filename = self.name + '.mif'
        os.path.isfile(self.mif_filename)
        mif_file = open(self.mif_filename, 'w')
        mif_file.write('# MIF 2.1\n\n')
        mif_file.write(self.mesh.get_mif())
        for energy in self.energies:
            mif_file.write(energy.get_mif())
        self.evolver._setname(self.name)
        if isinstance(self.evolver, LLG):
            mif_file.write(self.evolver.get_mif())
        else:
            mif_file.write(self.evolver.get_mif())
        mif_file.write(self._schedule_outputs())
        mif_file.close()

    def run(self, stages=1):
        if isinstance(self.evolver, LLG):
            self.stages = stages
            self.create_mif()
            self.execute_mif()
        else:
            raise JoommfError("Joommf: You must add a valid time"
                              " evolver to the simulation object")

    def _schedule_outputs(self):
        mif = ""
        if isinstance(self.evolver, LLG):
            evolverstr = "Oxs_TimeDriver"
        elif isinstance(self.evolver, Minimiser):
            evolverstr = "Oxs_MinDriver"
        for i, output in enumerate(self.evolver_outputs):
            mif += textwrap.dedent("""\
                Destination archive{} mmArchive
                Schedule {}::{} archive{} Stage {}
                """.format(i, evolverstr,
                           output[0], i,
                           output[1]))

        mif += textwrap.dedent("""\
              Destination archive mmArchive
              Schedule DataTable archive Step 1
              """).format(evolverstr)
        return mif

    def minimise(self):
        if isinstance(self.evolver, Minimiser):
            self.create_mif()
            self.execute_mif()
        else:
            raise JoommfError("Joommf: You must add a valid minimisation"
                              " evolver to the simulation object")
    minimize = minimise

    def execute_mif(self):
        process = o.call_oommf('boxsi ' + self.mif_filename)
        while True:
            output = process.stdout.readline()
            stderr = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            elif self.debug:
                print(output)
                print(stderr)
        return_code = process.poll()
        if return_code != 0:
            raise JoommfError("Joommf: OOMMF failed to execute.")
        self.ODTFile = odtreader.ODTFile(self.mif_filename[:-3] + 'odt')
        self.df = self.ODTFile.df
