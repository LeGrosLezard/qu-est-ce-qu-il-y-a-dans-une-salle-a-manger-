# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping






       
 -   détecter une assiette
 
  - Scrap
     
  - scrap v2
   

 - travail des images data 
     
           effacer les objets qui sont pas sont dégommer ou pas ok
           
           faire le crop (soit par forme soit par crop 25 / 50)
              
           supprimer les images ou les objets sont pas décollés + les images dégommés par le contour
           
           faire le truk des crop et save (croping) -> se calquer sur assiette
           
           
   
 - on remplis le csv avec le nouveau label
  
       rpour chaque catégorie faire un csv a par
       
       remplir par size de crop ou forme
       
       faire un premier matching
       
       si plusieurs fois le meme truk et scrap ex: plusieurs fois manche, plusieurs fois detection
       
       récupérer la ligne du csv
       
       le mettre dans le ok
       
       
  
       récupérer les parties de l'objet via les crop 
        
        
 - entrainement model
 
         si ca marche pas télécharger 400 données
 
         faire l'apprentissage des croping

- Scrap partie objet

           scrap des items (manche)
 
 - detection/comparaison
 
           ex : cuillere + fourchette + couteau a detection a stendroit
 
            on dit c le manche
            
            on récupere les parties


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
        
        
       

     
     

        
        
        
