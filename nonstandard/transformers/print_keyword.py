
from utils.simple2to3 import MyRefactoringTool, get_single_fixer

try:
    my_fixes = MyRefactoringTool( [get_single_fixer("print")] )
except:
    print("Cannot create MyRefactoringTool in print_keyword.")
    my_fixes = None

def transform_source(source):
    if my_fixes is None:
        return source
    try:
        return my_fixes.refactor_source(source)
    except:
        return source
