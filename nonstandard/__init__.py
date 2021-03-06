#pylint: disable=C0103, W0212
'''
In the following explanation, when we mention "the console" we refer to
a session using the nonstandard interactive console included in this package.

Possible invocations of this module:

1. python -m nonstandard: we want to start the console
2. python -m nonstandard script: we want to run "script" as the main program
                                but do not want to start the console
3. python -i -m nonstandard script: we want to run "script" as the main program
                                and we do want to start the console after
                                script has ended
4. python -m nonstandard trans1 trans2 script: we want to run "script" as the
                                main program, after registering the
                                tansformers "trans1" and "trans2";
                                we do not want to start the console
5. python -i -m nonstandard trans1 trans2 script: same as 4 except that we
                                want to start the console when script ends

Note that a console is started in all cases except 4 above.
'''
import os
import sys

from .core import console, import_hook, transforms
from .transformers import utils
start_console = console.start_console

if "-m" in sys.argv:
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)-1):
            print("Should import ", sys.argv[i])
            transforms.import_transformer(sys.argv[i])

        main_module = import_hook.import_main(sys.argv[-1])

        if sys.flags.interactive:
            main_vars = {}
            for var in dir(main_module):
                if var in ["__builtins__", "__cached__", "__loader__",
                           "__package__", "__spec__"]:
                    continue
                main_vars[var] = getattr(main_module, var)
            start_console(main_vars)
            # The following is the only way to prevent exiting into
            # the a "faulty" version of the normal Python console;
            # [for exemple, the help() is broken]
            # Executing sys.exit() or the equivalent
            # raise SystemExit
            # would not do the trick; however, os_exit does.
            os._exit(1)
    else:
        start_console()
