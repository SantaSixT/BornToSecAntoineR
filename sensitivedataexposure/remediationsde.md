Nom de la faille : Exposition de Données Sensibles (Sensitive Data Exposure) via "Sécurité par l'obscurité". 

1. Le Problème (L'erreur du développeur) Le développeur a cru que cacher un fichier important (le flag) dans une arborescence complexe (/.hidden/.../.../README) suffirait à le protéger. 

    Erreur 1 : Il a indiqué l'existence du dossier caché dans robots.txt. C'est comme mettre une pancarte "Ne regardez pas sous le tapis" devant sa maison. 

    Erreur 2 : Il n'a mis aucune restriction d'accès (pas de mot de passe, pas de vérification d'utilisateur). N'importe qui connaissant l'URL peut lire le fichier. 

2. Pourquoi c'est grave ? Les attaquants utilisent des outils automatisés (comme ton script Python crawler.py) qui ne se fatiguent jamais. Si une ressource est accessible publiquement sur le web, elle sera trouvée, peu importe la profondeur du dossier. 

3. Remédiation (Comment corriger ?) 

    Ne jamais utiliser robots.txt pour cacher des secrets : Ce fichier est public. Il sert au référencement, pas à la sécurité. 

    Contrôle d'accès (Authentication) : Si un dossier doit être privé, il doit être protégé par un mot de passe (ex: .htaccess + .htpasswd sous Apache) ou inaccessible depuis le web (placé hors du dossier /var/www/html). 

    Désactiver le listing de répertoires : Empêcher le serveur d'afficher la liste des dossiers (Options -Indexes dans Apache/Nginx). 