try:
    import fidimag
try:
    import pyoommf.sim

class SimBackend:
    def __init__(self, backend="oommf"):
        if backend is "oommf":
            try:
                import pyoommf
            except ImportError:
                print("DEBUG: Backend OOMMF failed to import")

        if backend is "fidimag":
            try:
                import pyfidimag
            except ImportError:
                print("DEBUG: Backend Fidimag failed to import")    
