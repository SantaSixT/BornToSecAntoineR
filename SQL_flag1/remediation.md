Analyse de la Cause 

L'application construit ses requêtes de base de données en concaténant directement la saisie de l'utilisateur (le paramètre id) avec la commande SQL. 

Code vulnérable probable (PHP) : 

$id = $_GET['id']; 

// L'entrée utilisateur est collée directement -> DANGER 

$query = "SELECT first_name, surname FROM users WHERE id = " . $id; 

$result = $conn->query($query); 

Comme l'entrée n'est ni nettoyée ni typée, l'attaquant peut injecter UNION SELECT... pour lire d'autres tables. 

2. La Solution Royale : Requêtes Préparées (Prepared Statements) 

C'est la seule méthode fiable à 100%. Au lieu d'injecter la donnée dans la requête, on utilise des "marqueurs" (? ou :id). La base de données traite alors la requête et la donnée séparément, ce qui empêche toute interprétation de code SQL malveillant. 

Correctif recommandé (PHP avec PDO) : 

$id = $_GET['id']; 

  

// 1. On prépare la structure de la requête avec un marqueur (?) 

$stmt = $pdo->prepare('SELECT first_name, surname FROM users WHERE id = ?'); 

  

// 2. On exécute en passant la donnée séparément 

$stmt->execute([$id]); 

  

$user = $stmt->fetch(); 

3. Défense en Profondeur (Input Validation) 

Puisque le champ id est censé être un nombre entier, on doit valider son type avant même d'interroger la base de données. 

Exemple de validation (Cast to Int) : 

// Si l'ID n'est pas numérique, on arrête tout. 

if (!filter_var($_GET['id'], FILTER_VALIDATE_INT)) { 

    die("Erreur : ID invalide."); 

} 

// Ou on force le type entier (Cast) 

$id = (int) $_GET['id']; 

Si un attaquant envoie -1 UNION SELECT..., le cast (int) le transformera en -1 et l'attaque échouera. 

4. Principe de Moindre Privilège 

L'utilisateur de base de données utilisé par l'application web ne devrait avoir accès qu'aux tables nécessaires au site. 

    Problème observé : Nous avons pu lire information_schema. 

    Remédiation : Restreindre les droits de l'utilisateur SQL (ne pas utiliser root ou un super-admin pour la connexion web).

    