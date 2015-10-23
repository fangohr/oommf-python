def assemble_mif(sim_object):
    """
    assemble_mif(sim_object, output)
    
    Function to take a simulation instance and return a string which 
    can be used as a MIF file.
   
    Parameters
    ----------
    sim_object : instance
        A simulation instance.

    Returns
    -------
    string
        The constructed MIF string for the simulation..
    """

    mif = "# MIF 2.1\n\nset pi [expr 4*atan(1.0)]\nset mu0 [expr 4*$pi1e-7]\n"
    



    return mif
    
