1. Analyse de la Cause (Code Vulnérable)

L'application prend la valeur fournie par l'utilisateur (via $_GET['page']) et l'utilise directement pour construire un chemin de fichier à inclure ou à lire, sans vérifier si l'utilisateur essaie de sortir du dossier prévu.
$page = $_GET['page']; // L'utilisateur envoie "../../../etc/passwd"
include($page);        // Le serveur exécute include("../../../etc/passwd")
Le serveur interprète les ../ comme "remonter au dossier parent", permettant à l'attaquant d'atteindre la racine du système.
2. La Solution Royale : Liste Blanche (Whitelisting)

C'est la méthode la plus sécurisée. Au lieu d'essayer de bloquer les "mauvais" caractères, on autorise uniquement une liste précise de fichiers valides.

Correctif recommandé (PHP) :
//////////////////////////////////////////
$page = $_GET['page'];

// 1. Liste stricte des pages autorisées
$authorized_pages = [
    'home' => 'home.php',
    'member' => 'member.php',
    'contact' => 'contact.php'
];

// 2. Vérification : Est-ce que la page demandée est dans la liste ?
if (array_key_exists($page, $authorized_pages)) {
    include($authorized_pages[$page]);
} else {
    // Si la page n'est pas autorisée, on affiche une erreur ou la page d'accueil
    include('404.php');
}
////////////////////////////////////////////////
Avec ce code, si un attaquant envoie ../../etc/passwd, le script vérifie la liste, ne trouve pas de correspondance, et affiche une erreur.
3. Solution Alternative : Nettoyage du Chemin (Sanitization)

Si une liste blanche n'est pas possible (trop de pages dynamiques), on doit forcer le nom de fichier à ne contenir aucun répertoire parent. La fonction basename() en PHP est idéale pour cela : 
elle ne garde que la partie finale du nom de fichier, supprimant tous les / et ...
/////////////////////////////////////////////////////////
$page = $_GET['page'];

// basename() transforme "../../../etc/passwd" en "passwd"
$clean_page = basename($page); 

// On force le dossier "pages/" pour empêcher l'accès ailleurs
include('pages/' . $clean_page . '.php');
/////////////////////////////////////////////////////
ci, l'attaque chercherait le fichier pages/passwd.php, qui n'existe pas, et l'attaque échoue.
4. Défense en Profondeur : Configuration Serveur (php.ini)

Pour limiter la casse même si le code est vulnérable, on peut configurer PHP pour empêcher l'accès aux fichiers hors du dossier web.

    open_basedir : Cette directive dans le fichier php.ini limite les fichiers que PHP peut ouvrir à un arbre de répertoires spécifique (ex: /var/www/html/). 
Si un script tente d'accéder à /etc/passwd, PHP bloquera l'accès au niveau système.
