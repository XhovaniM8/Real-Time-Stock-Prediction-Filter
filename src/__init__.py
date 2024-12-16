# src/__init__.py

from .analysis import arburg_vector, arburg_matrix
from .synthesis import gen_ts
from .utils import freqz, arcoeff_to_cep, cep_to_arcoeff
from .plot import real_time_plot
from .stock_simulation import fetch_stock_price
from .convert_to_excel import save_to_excel
from .gui import CreateGUI

__version__ = '0.1.0'
__author__ = 'Your Name'

__all__ = [
    'arburg_vector',
    'arburg_matrix',
    'gen_ts',
    'freqz',
    'arcoeff_to_cep',
    'cep_to_arcoeff',
    'real_time_plot',
    'fetch_stock_price',
    'save_to_excel',
    'CreateGUI',
]
