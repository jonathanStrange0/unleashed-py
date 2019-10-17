"""unleashed-py - Python package to connect to the Unleashed Software inventory management API"""
import sys, os
__version__ = '1.0.6'
__author__ = 'Jonathan Mucha <jonmucha@gmail.com>'
sys.path.append(os.path.join(os.path.dirname(__file__)))

# __all__ = []
from .unleashed_py import UnleashedBase
from .unleashed_py import Resource
from .unleashed_py import EditableResource
