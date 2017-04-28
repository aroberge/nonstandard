from utils.simple2to3 import MyRefactoringTool, get_lib2to3_fixers


try:
    my_fixes = MyRefactoringTool(get_lib2to3_fixers())
except:
    print("Cannot create MyRefactoringTool in convert_py2.")
    my_fixes = None

def transform_source(source):
    if my_fixes is None:
        return source
    try:
        return my_fixes.refactor_source(source)
    except:
        return source