from utils.one2one import translate

def transform_source(source):
    '''Replaces instances of
        nobreak
    by
        else 
    '''
    return translate(source, {'nobreak': 'else'})

