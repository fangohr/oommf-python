import oommfmif as o


def test_get_oommf_version_return_type():
    assert isinstance(o.get_version(), str)


def test_get_oommf_version():
    assert o.get_version()[0:4] == "1.2."


def test_get_oommf_path():
    assert isinstance(o.get_oommf_path(), str)


def test_run_oommf_simulation(tmpdir):

    bigbar_mif_1 = """# MIF 2.1
# Sample problem description for muMAG Standard Problem #1
set pi [expr 4*atan(1.0)]
set mu0 [expr 4*$pi*1e-7]

Specify Oxs_BoxAtlas:atlas {
  xrange {0 30e-9}
  yrange {0 30e-9}
  zrange {0 100e-9}
}

Specify Oxs_RectangularMesh:mesh {
  cellsize {2.5e-9 2.5e-9 2.5e-9}
  atlas :atlas
}

Specify Oxs_UniformExchange {A  13e-12}


Specify Oxs_Demag {}

#Specify Oxs_UZeeman "Hrange { { 0.5e6 0 0 0.5e6 0 0 0 } }"

Specify Oxs_EulerEvolve {
  alpha 0.5
  start_dm 0.0001
  gamma_G 0.2211e6
  absolute_step_error 0.02
  relative_step_error 0.02
}


Specify Oxs_TimeDriver {
 basename bigbar
 evolver Oxs_EulerEvolve
 stopping_dm_dt 0.01
 mesh :mesh
 stage_count 1
 stage_iteration_limit 550000
 total_iteration_limit 2
 Ms { Oxs_UniformScalarField { value 0.86e6 } }
 m0 { Oxs_UniformVectorField {
  norm 1
  vector {1 0 1}
 } }
}

Destination archive mmArchive

Schedule DataTable archive Step 10
Schedule Oxs_TimeDriver::Magnetization archive Stage 500
"""

    print("tmpdir is {}".format(str(tmpdir)))
    print("cwd is")
    import os
    os.system('pwd')
    os.system('cd {}'.format(tmpdir))
    os.system('pwd')

    import os.path
    open(os.path.join(str(tmpdir), 'bigbar.mif'), 'w').write(bigbar_mif_1)

    process = o.call_oommf('boxsi bigbar.mif', workdir=tmpdir)
    process.wait()
    assert os.path.exists(os.path.join(str(tmpdir),
                          'bigbar-Oxs_TimeDriver-Magnetization-00-0000002.omf')
                          )
