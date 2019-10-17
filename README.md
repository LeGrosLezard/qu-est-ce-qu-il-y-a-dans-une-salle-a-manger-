# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping






       
 -   détecter une assiette
 
  - Scrap
     
              chercher les dimensions de l'objet et les redimensionner
              
              limiter les dimensions ex: fourchette = ca, verre = ca, assiette = ca, bol = assiette
              
              et pour la recherche... ben on peut pas resize et faire la recherche a chaque fois
              
              peut etre faire une recherche a droite les couvert au milieu l'assiette
              

     
  - scrap v2
   

 - travail des images data 
     
           
           
           
           
           faire le crop (soit par forme soit par crop 25 / 50)  
           
           faire le truk des crop et save (croping) -> se calquer sur assiette
           
 <br> <br> <br> <br> <br> <br> <br>
   
   
  en gros on découpe, on scrap, on apprend, on compare, on réapprend
  
  et faire une image qui dit les parties avec une fleche et un rectangle comme yolo
   
 - on remplis le csv /  
  
       
       rpour chaque catégorie faire un csv a par
       

       récupérer la ligne du csv
       
       le mettre dans le ok
 
       
       pour vérigier refaire un position avec le nouveau csv (manche/cuve)
 
 
 - Scrap partie objet

           scrap des items (manche)
 
  - detection/comparaison
 
              remplir par size de crop ou forme
 
            
               faire un premier matching
       
               si plusieurs fois le meme truk et scrap ex: plusieurs fois manche, plusieurs fois detection

 - entrainement model
 
       si ca marche pas télécharger 400 données



 <br> <br> <br> <br> <br> <br> <br> <br> <br> <br>


 



- réentrainement

            on rajoute une ligne au csv
            
            on efface model
            
            on recré model
            
           



- programme

             si csv + 26 + 9 label

            on réécrit directement dans le programme  (algo algo)
            
            via un fichier ou y'a écrit ligne tant ou ca dit fonction with open + model = load
 
 
 
 
 
 
 
 
 
 
 
 
 - BUT
 
        - detection cuillere, fourchette, couteau
        
        - que ca dise detection de manche, detection cuileré et detection objet cuillere

        - que ca dise soit meme manche ne bas autre truk en haut
        
        - que le scrap soit bon
        
        - tant que c pas comme jlimagine
        
        
       

     
     
     
     
     apres yolo
     
     ca sert a rien mais 
     
essayé de faire un fleche detecteur en ne prenant que le bout de la fleche (via un centre du contour on fait un rectangle apres, avant le centre afin de n'avoir que le triangle et caché la queue) et le transformer en triangle parfait (range range detecte les 3 pts faire la ligne voir l'air de se truk) heureusement y demandait pas ca mais ca m'a fatigué un truk de dingue

        
        
        
