import sys
path = '/home/Joshua1414/comp2011/cwk2'
if path not in sys.path:
   sys.path.insert(0, path)

from app import app as application