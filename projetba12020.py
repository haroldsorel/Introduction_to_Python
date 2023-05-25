"""
My Escape Game
Auteur : Harold Sorel
Date : 21/10/2020
Travail réalisé dans le cadre du cours d'informatique de BA1 polytech 2020
Petit jeu ayant comme but de s'orienter dans un labyrinth
dans lequel il faudra repondre à des questions
et s'armer d'objects que l'on rencontrera sur le chemin
pour arriver à la case finale et ainsi gagner le jeu.
"""

import turtle
import time

POINT_AFFICHAGE_ANNONCES = (-240, 240)  # Point d'origine de l'affichage des annonces
POINT_AFFICHAGE_INVENTAIRE = (80, 180)  # Point d'origine de l'affichage de l'inventaire

# Couleur et dimension du personnage
RATIO_PERSONNAGE = 0.9  # Rapport entre diamètre du personnage et dimension des cases
POSITION_DEPART = (0, 1)  # Porte d'entrée du château

# Désignation des fichiers de données à utiliser
fichier_plan = 'plan_chateau.txt'
fichier_questions = 'dico_portes.txt'
fichier_objets = 'dico_objets.txt'

# composantes matriciels variantes
x = 0
y = 1

# chiffre inventaire variant
n = 0


def lire_matrice(fichier):
    mat = []
    with open(fichier) as f:
        for ligne in f:
            list_ligne = []
            for elem in ligne:
                if elem.isalnum() is True:
                    list_ligne.append(int(elem))
            mat.append(list_ligne)
    return mat


def calculer_pas(matrice):
    nombre_de_colonne = len(matrice[0])
    dimension_case_colonne = 290/nombre_de_colonne
    nombre_de_ligne = len(matrice)
    dimension_case_ligne = 440/nombre_de_ligne
    return max(dimension_case_colonne, dimension_case_ligne)


def coordonnees(case):
    coord_x = -240 + (pas * case[1])
    coord_y = (200 - pas) - (pas * case[0])
    return coord_x, coord_y


def tracer_carre(dimension):
    turtle.setheading(90)
    for x in range(3):
        turtle.pendown()
        turtle.forward(dimension)
        turtle.right(90)
        turtle.penup()


def tracer_case(case, couleur):
    coord = coordonnees(case)
    turtle.goto(coord)
    turtle.color(couleur, couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()


def afficher_plan(matrice):
    for x in range(len(matrice)):
        for y in range(len(matrice[0])):
            if matrice[x][y] == 0:
                tracer_case((x, y), 'white')
            elif matrice[x][y] == 1:
                tracer_case((x, y), 'grey')
            elif matrice[x][y] == 2:
                tracer_case((x, y),'yellow')
            elif matrice[x][y] == 3:
                tracer_case((x, y), 'orange')
            elif matrice[x][y] == 4:
                tracer_case((x, y), 'green')


def deplacement(mouvement):
    global x, y
    if mouvement == 'gauche' :
        turtle.setheading(180)
        if matrice[x][y - 1] != 1:
            if matrice[x][y - 1] == 3:
                pos = (x, y-1)
                question(mouvement, pos)
            else:
                y -= 1
                turtle.forward(pas)
                modification('wheat')
    elif mouvement == 'droite':
        turtle.setheading(0)
        if matrice[x][y + 1] != 1:
            if matrice[x][y + 1] == 3:
                pos = (x, y+1)
                question(mouvement, pos)
            else:
                y += 1
                turtle.forward(pas)
                modification('wheat')
    elif mouvement == 'arriere':
        turtle.setheading(90)
        if matrice[x - 1][y] != 1:
            if matrice[x - 1][y] == 3:
                pos = (x-1, y)
                question(mouvement, pos)
            else:
                x -= 1
                turtle.forward(pas)
                modification('wheat')
    elif mouvement == 'avant':
        turtle.setheading(270)
        if matrice[x + 1][y] != 1:
            if matrice[x + 1][y] == 3:
                pos = (x+1, y)
                question(mouvement, pos)
            else:
                x += 1
                turtle.forward(pas)
                modification('wheat')
    if matrice[x][y] == 4:
        ramasse_objet()
    if matrice[x][y] == 2:
        gagne()


def gauche():
    deplacement('gauche')


def droite():
    deplacement('droite')


def avant():
    deplacement('avant')


def arriere():
    deplacement('arriere')


def creer_dictionnaire_des_objets(fichier):
    dic = {}
    with open(fichier) as f:
        for ligne in f:
            a, b = eval(ligne.strip())
            dic[a] = b
    return dic


def ramasse_objet():
    global x, y, matrice, n
    modification('wheat')
    matrice[x][y] = 0
    n += 1
    annonce.clear()
    annonce.write('Vous avez trouvé un objet : ' + dic_objet[(x, y)], font=('Arial', 16, "bold"))
    inventaire.goto(inventaire.xcor(), inventaire.ycor() - 2 * pas)
    inventaire.write('objet n.' + str(n) + ' : ' + dic_objet[(x, y)], font=('Arial', 10, 'normal'))
    del dic_objet[(x, y)]


def question(mouvement, pos_prochaine):
    global x, y, matrice
    annonce.clear()
    annonce.write('La porte est fermée', font=('Arial', 16, 'bold'))
    time.sleep(1)
    if turtle.textinput('Question', dic_question[pos_prochaine][0]) == dic_question[pos_prochaine][1]:
        annonce.clear()
        annonce.write("La porte s'ouvre", font=('Arial', 16, 'bold'))
        turtle.forward(pas)
        if mouvement == 'gauche':
            matrice[x][y - 1] = 0
            y -= 1
        elif mouvement == 'droite':
            matrice[x][y + 1] = 0
            y += 1
        elif mouvement == 'avant':
            matrice[x + 1][y] = 0
            x += 1
        elif mouvement == 'arriere':
            matrice[x - 1][y] = 0
            x -= 1
        turtle.listen()
        modification('wheat')
        del[dic_question[(x, y)]]

    else:
        annonce.clear()
        annonce.write('Mauvaise réponse', font=('Arial', 16, 'bold'))
        turtle.listen()


def gagne():
    global x
    if dic_question == {} and dic_objet == {}:
        annonce.clear()
        annonce.write('Bravo! Vous avez gagné!', font=('Arial', 16, 'bold'))
        time.sleep(2)
        annonce.clear()
        annonce.write("Merci d'avoir joué.", font=('Arial', 16, 'bold'))
        time.sleep(2)
        annonce.clear()
        annonce.write('Aurevoir.', font=('Arial', 16, 'bold'))
        time.sleep(2)
        turtle.done()
    else:
        annonce.clear()
        annonce.write('Il vous manque quelque chose, revenez en arrière.', font=('Arial', 16, 'bold'))
        turtle.backward(pas)
        x -= 1


def modification(couleur):
    modif.goto(coordonnees((x, y)))
    modif.color(couleur, couleur)
    modif.begin_fill()
    modif.setheading(90)
    for cote in range(3):
        modif.forward(pas)
        modif.right(90)
    modif.end_fill()
    turtle.showturtle()


# initialisation
turtle.speed(0)
turtle.penup()
turtle.hideturtle()
matrice = lire_matrice(fichier_plan)
pas = calculer_pas(matrice)
afficher_plan(matrice)

# clone inventaire
inventaire = turtle.Turtle()
inventaire.hideturtle()
inventaire.penup()
inventaire.goto(POINT_AFFICHAGE_INVENTAIRE)
inventaire.write('Inventaire :', font=('Arial', 15, 'bold'))

# clone annonce
annonce = turtle.Turtle()
annonce.hideturtle()
annonce.penup()
annonce.goto(POINT_AFFICHAGE_ANNONCES)

# clone modification
modif = turtle.Turtle()
modif.speed(0)
modif.hideturtle()
modif.penup()



# création du personnage
turtle.color('red', 'red')
turtle.shape('circle')
turtle.shapesize(1/21 * 0.8 * pas)

# annonce début
annonce.write('Bienvenu dans le labyrinth.', font=('Arial', 15, 'bold'))
time.sleep(3)
annonce.clear()
annonce.write('Pour gagner, vous devez recolter tout les objects, en vert...', font=('Arial', 15, 'bold'))
time.sleep(3)
annonce.clear()
annonce.write('Repondre à toute les question, en orange...', font=('Arial', 15, 'bold'))
time.sleep(3)
annonce.clear()
annonce.write('Et finalement, trouver la sortie.', font=('Arial', 15, 'bold'))
time.sleep(3)
annonce.clear()
annonce.write('Bonne chance!',font=('Arial', 15, 'bold'))

# début du jeu
turtle.goto((coordonnees(POSITION_DEPART)[0] + pas/2, coordonnees(POSITION_DEPART)[1] + pas/2))
modification('wheat')
turtle.setheading(270)
turtle.showturtle()

# dictionnaires
dic_objet = creer_dictionnaire_des_objets(fichier_objets)
dic_question = creer_dictionnaire_des_objets(fichier_questions)

# deplacement
turtle.listen()
turtle.onkeypress(gauche, "Left")
turtle.onkeypress(droite, "Right")
turtle.onkeypress(arriere, "Up")
turtle.onkeypress(avant, "Down")
turtle.mainloop()
