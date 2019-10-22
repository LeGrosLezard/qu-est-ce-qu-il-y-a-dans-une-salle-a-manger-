# Jojo

#download from penseeartificielle/google-image-scrapping

tache en cours


      - raccorder label et detection depuis main. En effet, il faut récupérer les différentes informations via les différents objets que l'on a.
      - mettre sur une image (current.jpg) les elements détectés sinon mettre un ?
  
      

      



<br><br><br><br>

Memo

- label -> nom du label; nom du csv; label; nombre de partie, nom partie1, nom partie2,... ; dimension;

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


