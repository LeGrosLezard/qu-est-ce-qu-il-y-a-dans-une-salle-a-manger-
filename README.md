# Jojo

#download from penseeartificielle/google-image-scrapping

tache en cours

    - Sur la bordure ajouter l'image de l'objet relié a l'image principale via une fleche. En sommes il faut -> scene principale ligne bleu image crop de l'image, et sa détection. Une fleche au lieu du point ? soh cah toa ? ajouter une bordure noir de 2 pixels aux crop


 

      

      



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


