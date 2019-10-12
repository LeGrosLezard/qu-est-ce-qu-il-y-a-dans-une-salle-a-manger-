# qu-est-ce-qu-il-y-a-dans-une-salle-a-manger-

#download from penseeartificielle/google-image-scrapping

-   Attention

         - tout bien faire pour y reveninr plus tard


 -   détecter une assiette


  - Scrap
  
 
           
   - scrap v2
   
           -> liste de mot du genre: lame, manche, tine, cuilléré qu'on rempli
           
          
   
 
 - travail des images data 
 
        -> mettre les crop dans de nouvelles images
        
        -> enregistrer les images dans un nouveau dossier
        
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

        
        
        
       
 - faire un truk lstm apres yolo
     
     

        
        
        
