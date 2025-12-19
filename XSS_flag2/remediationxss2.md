http://192.168.10.135/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg== 

L'application récupère le paramètre GET src et l'insère directement dans un attribut HTML (probablement <object data="..."> ou <embed src="...">) sans valider le protocole. 

Le développeur s'attendait à recevoir un nom de fichier (ex: nsa), mais le navigateur accepte d'autres protocoles comme : 

    javascript:alert(1) (souvent bloqué par les navigateurs modernes dans les images). 

    data:text/html;base64,... (Interprété comme un fichier HTML complet encodé, contenant des scripts). 

2. Mesures Correctives (PHP) 

A. Validation du Protocole (Liste Blanche) Il faut refuser tout ce qui ne ressemble pas à un chemin d'image standard ou à une URL HTTP(S) 

$src = $_GET['src']; 

 

if (ctype_alnum($src)) { echo "<object data='images/" . htmlspecialchars($src, ENT_QUOTES, 'UTF-8') . ".jpg'></object>"; } else { // 2. Ou on vérifie que cela commence par http:// ou https:// (si on autorise les URL externes) if (filter_var($src, FILTER_VALIDATE_URL) && (strpos($src, 'http://') === 0 || strpos($src, 'https://') === 0)) { echo "<object data='" . htmlspecialchars($src, ENT_QUOTES, 'UTF-8') . "'></object>"; } else { echo "Erreur : Image non autorisée."; } } 
B. Content Security Policy (CSP) Configurer l'en-tête HTTP CSP pour interdire l'exécution de données inline (data:). 

Content-Security-Policy: default-src 'self'; object-src 'none'; script-src 'self'; 