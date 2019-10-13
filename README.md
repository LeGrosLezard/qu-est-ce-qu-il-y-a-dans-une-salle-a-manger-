# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping




-   Attention

         - le but c de detecter un objet par un objet via un crop MAIS
         
         - on doit faire un hog pour detecter le manche et les extrémités pointues par exemple !
         
         - on veut que ce machin se dise a lui meme manche en bas lame en haut via cuillere
         
         - et en plus d'une phase de scrap mais ca... j'en ai eu ma dose avec bobo ^^ jdeteste ca mtn jcrois en plus ca donne la gerbe


 -   détecter une assiette


  - Scrap
  
 
           
   - scrap v2
   

           
          
   
 
 - travail des images data 
 
        -> selon le scrappage identifier les parties -> manche + rond => cuillere avec les contours
        

        
 - on remplis le csv avec le nouveau label
  
       - partie de l'objet (1 csv manche / 1 csv cuilleré 1 csv objet complet)
        
        ss phrase = constitué .... ET ...
        
 -  entrainement model
 
        -> faut faire: slider hog mais on veut le manche donc on fait partie objet hog + detection svm
 
        -> on récupere toutes les parties des objets
        
        -> on les mets dans un model

        -> entrainer un model de forme (ou le faire sous opencv)
       
        -> supprimer image




        
 
 - BUT
 
        - detection cuillere, fourchette, couteau
        
        - que ca dise detection de manche, detection cuileré et detection objet cuillere

        - que ca dise soit meme manche ne bas autre truk en haut
        
        - que le scrap soit bon
        
        - tant que c pas comme jlimagine
        
        
       
 - faire un truk lstm apres yolo
     
     

        
        
        
