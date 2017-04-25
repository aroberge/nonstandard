

import sys

from utils import console, import_hook, transforms

'''
In the following explanation, when we mention "the console" we refer to 
a session using the nonstandard interactive console included in this package.

Possible invocations of this module:

1. python nonstandard.py: we want to start the console
2. python nonstandard.py script: we want to run "script" as the main program
                                but do not want to start the console
3. python -i nonstandard.py script: we want to run "script" as the main program
                                and we do want to start the console after
                                script has ended
4. python nonstandard.py trans1 trans2 script: we want to run "script" as the
                                main program, after registering the
                                tansformers "trans1" and "trans2";
                                we do not want to start the console
5. python -i nonstandard.py trans1 trans2 script: same as 4 except that we
                                want to start the console when script ends                      
'''


if __name__ == '__main__':
    if len(sys.argv) > 1:
        __name__ = __file__[:-3]  # this module is not meant as __main__

        for i in range(1, len(sys.argv)-1):
            transforms.transformers.add(sys.argv[i])

        import_hook.import_main(sys.argv[-1])
        
        if sys.flags.interactive:
            console.start_console()
    else:
        console.start_console()
else:
    console.start_console()


