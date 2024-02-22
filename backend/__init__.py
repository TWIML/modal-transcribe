'''
The entry point to the `backend` folder 

Here we are making it available to import from across the repo
'''

import os, sys

backend_root_module_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_root_module_directory)