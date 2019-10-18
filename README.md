# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping

si ca marche pas faire que manche/haut et ensutie dire si manche ou haut

50/50 assiette par 25 / couvert 50/150 par 25 et 50
 
<br><br><br><br>
 

il faut detecter le manche le reste c'est bon

il faut au moins deux detections du manche

legume/fouchette/cuillere = 2 manches

du coup normalement y'a au moins deux detections de manche

mais c'est parce que j'avais pas crop les images en partie




5 - on supprime le csv 

6 - on en fait un nouveau avec le label

7 - le reste ou tout l'objet dans le csv assiette

8 - detection de l'assiette + couvert stp

    8-1 si manche + assiette -> assiette/cuillere ou vis versa recherche geometrie manche + assiette/cuillere -> cuillere / assiete/cuillere -> assiette merde mais c bon sinon jcrois


9 - essayer tout d'un coup


 <br> <br> <br> <br> <br> <br> <br> <br>

 
 
  - Scrap
              
     
              chercher les dimensions de l'objet et les redimensionner
              
              limiter les dimensions ex: fourchette = ca, verre = ca, assiette = ca, bol = assiette tournevis = fourchette= marteau
              
              et pour la recherche... ben on peut pas resize et faire la recherche a chaque fois
              
              peut etre faire une recherche a droite les couvert au milieu l'assiette
              
              sinon la forme, si manche alors 50/150 si rond = 50/50 chai pas


- ajouté des carré a la scene assiete + couvert

- la redimensionner ?
  

- programme

             si csv + 26 + 9 label

            on réécrit directement dans le programme  (algo algo)
            
            via un fichier ou y'a écrit ligne tant ou ca dit fonction with open + model = load
 
 
 
 
 
 
 
 
 
 
 
 
 - BUT
 
        - detection cuillere, fourchette, couteau
        
        - que ca dise detection de manche, detection cuileré et detection objet cuillere

        - que ca dise soit meme manche ne bas autre truk en haut
        
        - que le scrap soit bon
        
        - lui montrer un trk ac un manche + un objet connu et qu'il le trouve le trouve
        
        - lui trouver un nom qui pete
        
        - tant que c pas comme jlimagine a peu pres
        
        
       

     
     
     
     
     apres yolo
     
     ca sert a rien mais 
     
essayé de faire un fleche detecteur en ne prenant que le bout de la fleche (via un centre du contour on fait un rectangle apres, avant le centre afin de n'avoir que le triangle et caché la queue) et le transformer en triangle parfait (range range detecte les 3 pts faire la ligne voir l'air de se truk) heureusement y demandait pas ca mais ca m'a fatigué un truk de dingue

        
        
        
