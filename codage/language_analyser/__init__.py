def isPrefix(u, v):
    """
    Détermine si u est un préfixe de v.
    Retourne :
        - 1 si u est un vrai préfixe de v
        - 0 si u == v
        - -1 sinon
    """
    if v.startswith(u):
        if u == v:
            return 0
        else:
            return 1
    return -1

def residuel(M, L):
    """
    Fonction qui trouve les résiduels de M par rapport à L.
    Renvoie une liste de résiduels uniques (set).
    """
    residuels = set()  # valeurs uniques, pas de doublons

    for u in M:
        for v in L:
            prefix_status = isPrefix(u, v)
            if prefix_status == 1:
                # u est un vrai préfixe de v => résiduel = suffixe de v après u
                residuels.add(v[len(u):])
            elif prefix_status == 0:
                # u == v => résiduel = mot vide
                residuels.add('')
    return residuels

def sardinas_patterson(L):
    """
    Fonction qui analyse le langage L et génère les résiduels successifs.
    Renvoie :
        - True si L est un code
        - False sinon
    """
    L_residuels = []
    L_residuels.append(list(L))  # L[0] = L d'origine

    # L[1] = residuel(L, L) - {''}
    residuels_1 = residuel(L, L)
    residuels_1.discard('')  # enlever les mots vides
    print(f"L_1 : {residuels_1}")
    L_residuels.append(list(residuels_1))
    

    n = 1
    while n >= 1:
        # L[i] = residuel(L, L[i-1]) + residuel(L[i-1], L)
        res1 = residuel(L, L_residuels[n])
        res2 = residuel(L_residuels[n], L)
        residuels_n1 = res1.union(res2)

        print(f"L_{n+1} : {residuels_n1}")
        # Si l'ensemble contient '', alors ce n'est pas un code
        if '' in residuels_n1:
            print(f"for n = {n} il y a un residu dans : {residuels_n1}")
            return False

        residuels_n1 = list(residuels_n1)
        
        # Si le pattern est déjà présent, on arrête
        if residuels_n1 in L_residuels:
            break

        # Ajouter à la liste des résiduels successifs
        L_residuels.append(residuels_n1)
        n += 1

    return True

def is_code_language(L):
    residus = residuel(L,L)
    residus.discard('')
    if len(residus) == 0:
        return True
    return sardinas_patterson(L)