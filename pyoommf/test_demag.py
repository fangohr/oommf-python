import demag

def test_demag():
    a = demag.Demag()
    assert 'Specify Oxs_Demag {}' in a.get_mif() 
 
