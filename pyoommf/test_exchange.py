import exchange
import sys
import os

def test_exchange():
    a = exchange.Exchange(1e4)
    a._save_exchange_mif()
    assert os.path.isfile('exchange.mif')    
