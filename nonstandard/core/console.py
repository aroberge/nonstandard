import code
import platform
import sys

from . import transforms

class NonStandardInteractiveConsole(code.InteractiveConsole):

    def push(self, line):
        """Transform and push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).

        """

        # In the console, we do transformations on one line at a time,
        # and try to execute it.

        

        if transforms.from_nonstandard.match(line):
            transforms.add_transformers(line)
            self.buffer.append("\n")
        elif not line:  # 
            self.buffer.append(" ") # ensure that a block ends
        else:
            self.buffer.append(line)

        add_pass = False
        if line.rstrip().endswith(":"):
            add_pass = True
        source = "\n".join(self.buffer)
        if add_pass:
            source += "pass"
        source = transforms.transform(source)
        if add_pass:
            source = source.rstrip()[:-4]

        more = self.runsource(source, self.filename)

        if not more:
            self.resetbuffer()
        return more


banner = "nonstandard console. [Python version: %s]\n" % platform.python_version()

def start_console(locals={}):
    sys.ps1 = "~~> "
    console = NonStandardInteractiveConsole(locals=locals)
    try:
        console.interact(banner=banner)
    except SystemExit:
        print("Leaving nonstandard console.\n")
        sys.ps1 = ">>> "