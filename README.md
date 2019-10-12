# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping

-   Attention

         - faudrait que ca fasse une boucle et que ca se renouvelle a chaque fois marteau peut etre un pillon inversement que ca se remette a jour quoi par contre STOP pcque la deja ca va etre une vrai galere


 -   détecter une assiette

         -> scrap dimension obj
         
         -> et crop chaque objet en donnant manche par exemple
         
         -> mettre assiette (comme yolo rectangle rouge)

  - Scrap
        -> avec les truk long comme marteau y'a le menu
        
        -> avec marteau -> on veut clou ou scie mais on a a la place marteau pillon

        -> chercher les dimensions/formes ex: cuillere != assiette
   
        -> detection des couleurs comme bobo (truk gris -> marteau)
      
        -> forme
   
   
   
   
 - travail des images data 
 
        -> essayer avec une nape
    
        -> voir si y'a un model qui s'enregistre image par image et si on lui presente un nouveau ca dit ok ou non
        
        -> essayer avec verre mais ca marche qu'avec ce type d'objet jcrois
        
        -> mettre les crop dans de nouvelles images
        
        -> enregistrer les images dans un nouveau dossier
        
        
        
 -  entrainement model
 
        -> normalement faut faire direct chui perdu la
        
        -> faut faire: slider hog mais on veut le manche donc on fait pas partie objet hog + detection svm
 
 
        -> on récupere toutes les parties des objets
        
        -> on les mets dans un model

        -> entrainer un model de forme (ou le faire sous opencv)
       
        -> supprimer image


 - on remplis le csv avec le nouveau label
  
        faire plusieurs csv si y'a plus de 26 + 9
 
        effacer images ou les transferer vers google drive
 
 
 - nouvelle detection
 
        scrapping web collect info qui manque ex: manche + truk carré gris
        
        detection partie objet -> déduction
 
        de haut en bas de gauche a droite -> ex tien il y a un manche, mais c de forme carré ca ! c un marteau !
        
 
 - BUT
 
        - quelle est stobjet ? (c rond, c a coté d'une cuillere -> bol !!!!) (y'a un manche, c carré et gris -> marteau !!!)
             
        - montre moi une salle a manger/dessine moi une salle a manger
