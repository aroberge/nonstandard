from translate import translate

def transform_source(source):
    '''Input text is assumed to contain some French equivalent words to
       normal Python keywords and a few builtin functions.
       These are transformed into normal Python keywords and functions.
    '''
    # continue, def, global, lambda, nonlocal remain unchanged by choice

    dictionary = {'Faux': 'False', 'Aucun': 'None', 'Vrai': 'True',
                   'et': 'and', 'comme': 'as', 'affirme': 'assert',
                   'sortir': 'break', 'classe': 'class', 'élimine': 'del',
                   'ousi': 'elif', 'autrement': 'else', 'exception': 'except',
                   'finalement': 'finally', 'pour': 'for', 'de': 'from',
                   'si': 'if', 'importe': 'import', 'dans': 'in', 'est': 'is',
                   'non': 'not', 'ou': 'or', 'passe': 'pass',
                   'soulever': 'raise', 'retourne': 'return', 'essayer': 'try',
                   'pendant': 'while', 'avec': 'with', 'céder': 'yield',
                   'imprime': 'print', 'intervalle': 'range'}

    return translate(source, dictionary)
