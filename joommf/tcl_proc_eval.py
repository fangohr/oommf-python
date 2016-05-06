def evaluate_tcl_proc(function, functionname, x, y, z):
    test.tk.eval(function)
    return [float(x) for x in test.tk.eval("{} {} {} {}".format(functionname, x, y, z)).split()]
