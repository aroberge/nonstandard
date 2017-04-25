from io import StringIO
import tokenize


def transform_source(source):
    '''Replaces instances of

        nobreak
    by

        else 

    '''

    nobreak_keyword = 'nobreak'

    if source.count(nobreak_keyword) == 0:
        return source

    toks = tokenize.generate_tokens(StringIO(source).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue == nobreak_keyword:
            result.append((tokenize.NAME, 'else'))
            continue
        result.append((toktype, tokvalue))

    new_source = tokenize.untokenize(result)
    last_line = source.split("\n")[-1]

    # Sometimes, in the interactive console, the last line of a block
    # will not be identified after this transformation, since it is not
    # a meaningful "token". To prevent this problem
    # we make sure to add an empty line.
    if last_line.strip() == '':
        new_source += "\n"
    return new_source


