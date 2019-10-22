# Jojo

#download from penseeartificielle/google-image-scrapping

tache en cours


      - Si detection l'afficher sur une image avec une fleche en bleu ou rouge. Dessus mettre le nom de la detection ici le nom du label. 


 
 Reflichis
 
 Comparaison avec 5 labels = 1 minutes, avec 20.... 
      

      



<br><br><br><br>

Memo

- label -> nom du csv; nom du label; label; nom partie1, nom partie2,... ; dimension;

- On récupère les dimensions de l'objet afin de modifier la taille de l'array pour l'entrainement -> dimension.py

      -> une assiette -> 50x50
      
      -> le haut de la fourchette -> 100x200 -> sinon il n'y a pas de detection entre cuillere/fourchette cela permet de mettre en valeur les dents de la fourchette

- Il faut chercher les différentes parties de l'objet via le scrap -> find_part.py
      
      - puis les mettre dans un csv
      
      -> manche / cuve
      
    


- si le csv contient deja 10 labels il faut modifier les programmes de training

- la detection des objets se fait par -> detection.py



tant qu'on ne trouve pas l'objet il faut faire:

  - 1) thread scrap/téléchargement
  
  - 2) traitement/apprentissage/comparaison


