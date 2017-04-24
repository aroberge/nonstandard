from io import StringIO
import tokenize


def transform_source(text):
    '''Replaces instances of

        nobreak
    by

        else 

    '''

    nobreak_keyword = 'nobreak'

    if text.count(nobreak_keyword) == 0:
        return text

    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue == nobreak_keyword:
            result.append((tokenize.NAME, 'else'))
            continue
        result.append((toktype, tokvalue))
    return tokenize.untokenize(result)


