from __nonstandard__ import french_syntax
de math importe pi

imprime("The first 5 odd integers are:")
pour i dans intervalle(1, 11, 2):
    imprime(i)

imprime("\nThis should be False:", Vrai et Faux)
print("\nIf this is meant as the main script,",
       "there should be one more statement printed.")

if __name__ == '__main__':
    si pi == 3:
        imprime("We must be in Indiana.") # should not print
    ousi pi < 3.14 ou pi > 3.15 :
        print("Non-Euclidean space.") # should not print
    autrement:
        print("\nThis should be the last statement for this test.\n")
