import sys

from child_process.Child import Child
from parents.LocalParent import LocalParent

par = LocalParent(sys.argv[1])
Child(par, True)