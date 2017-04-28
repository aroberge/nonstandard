import code
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
            self.buffer.append('')
        elif not line:  # 
            self.buffer.append("\n") # ensure that a block ends
        else:
            # Lines of code can be invalid Python syntax if:
            #   1. they are indented
            #   2. they end with ":" indicating the beginning of a block
            # We take care of these two problems as follows:
            #   1. we remove any indent of the line prior to the transformation
            #      and reinsert it after the transformation
            #   2. we add a pass statement as a block prior to the
            #      transformation and we remove it afterwards.
            before_len = len(line)
            line = line.lstrip()
            indent = before_len - len(line)

            if line.endswith(":"):
                line = line + " pass"

            line = transforms.transform(line)

            if line.endswith(": pass"):
                line = line[:-5]
                
            line = " " * indent + line
            self.buffer.append(line)

        source = "\n".join(self.buffer)

        more = self.runsource(source, self.filename)

        if not more:
            self.resetbuffer()
        return more


banner = """Python version: %s

    Python console with easily modifiable syntax.\n""" % sys.version

def start_console():
    sys.ps1 = "~~> "
    console = NonStandardInteractiveConsole()
    try:
        console.interact(banner=banner)
    except SystemExit:
        print("Leaving non-standard console.\n")
        sys.ps1 = ">>> "