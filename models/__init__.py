from os.path import dirname, basename, isfile
import glob

# All the files in this package
modules = glob.glob(dirname(__file__)+"/*.py")

# https://stackoverflow.com/questions/17236895/python-module-and-all
# Listing names in __all__ does not, by itself, import items into a module. All it does is list names to import from that module if you used from database import * syntax.
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py') and not f.endswith('base_model.py')]
