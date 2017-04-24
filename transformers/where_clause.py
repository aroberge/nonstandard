from io import StringIO
import tokenize

sample_in = '''
def twice(i, next):
    where:
        i: int
        next: Function[[int], int]
        return: int
    return next(next(i))
'''

sample_out = '''
def twice (i ,next ):
    return next (next (i ))
'''

variable_in = '''
x = 3
where:
    x: int
'''

variable_out = '''
x=3
'''


def transform_source(text):
    '''removes a "where" clause which is identified by the use of "where"
    as an identifier and ends at the first DEDENT (i.e. decrease in indentation)'''
    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    where_clause = False
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue == "where":
            where_clause = True
        elif where_clause and toktype == tokenize.DEDENT:
            where_clause = False
            continue

        if not where_clause:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)

if __name__ == '__main__':
    assert sample_out == transform_source(sample_in)

    # the transformation process may leave extra spaces at the end which
    # prevent an exact comparison from working.  Removing what are clearly
    # superfluous spaces, the following works.
    assert variable_out == transform_source(variable_in).replace(' ', '')
