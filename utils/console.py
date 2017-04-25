import code
import sys

from . import transforms

class NonStandardInteractiveConsole(code.InteractiveConsole):
    last_source = ''
    def push(self, line):
        """Push a line to the interpreter.

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

        if transforms.from_nonstandard.match(line):
            transforms.add_transformers(line)
        else:
            self.buffer.append(line)

        source = "\n".join(self.buffer)
        source = transforms.transform(source)

        # transformations may result in the last line of code being 
        # dropped if it is empty. We take care of this as follows:
        if source == self.last_source:
            source += "\n"
        self.last_source = source
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