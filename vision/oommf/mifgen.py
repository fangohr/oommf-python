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
    
def save_mif(sim_object, target):
    """
    save_mif(sim_object)

    Function takes a simulation instance and then saves the mif to file in
    order to run a simulation, and also += 1 to the N_mifs in order to keep
    track of multiple simulation steps, ie if a parameter will change.
    
    Parameters
    ----------
    sim_object : instance
        A simulation instance.
    
    Returns
    -------
    string
         The path to the mif file
    """
    
    path = sim_object.name + "_" + str(sim_object.t) + "_" + str(target) + ".mif"
    f = open(path, 'w')
    f.write(sim_object.mif)
    return path
    
