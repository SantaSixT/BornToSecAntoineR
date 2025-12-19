1. La Cause (Code Vulnérable) 

Le problème vient du fait que l'application concatène directement l'entrée utilisateur (le paramètre id) dans la chaîne de requête SQL, sans vérification ni échappement. 

Exemple de code PHP vulnérable (ce qui tourne probablement sur le serveur) : 

$id = $_GET['id']; 

// L'entrée est collée directement : DANGER 

$query = "SELECT url, title, comment FROM list_images WHERE id = " . $id; 

$db->query($query); 

Cela permet à ton payload -1 UNION SELECT... de modifier la structure même de la commande envoyée à la base de données. 

2. La Solution Recommandée : Requêtes Préparées (Prepared Statements) 

C'est la protection standard de l'industrie. Au lieu d'injecter la variable $id directement, on utilise un marqueur (placeholder). La base de données traite alors la requête et la donnée séparément, rendant l'injection impossible, même si l'utilisateur envoie du code SQL. 

Correctif (PHP avec PDO) : 

$id = $_GET['id']; 

  

// 1. On prépare la structure avec un marqueur (?) 

$stmt = $pdo->prepare("SELECT url, title, comment FROM list_images WHERE id = ?"); 

  

// 2. On exécute en passant la donnée séparément 

$stmt->execute([$id]); 

  

$results = $stmt->fetchAll(); 

3. Défense en Profondeur : Validation des Entrées (Input Validation) 

Puisque le champ id est censé être un nombre entier, l'application ne devrait jamais accepter de caractères comme U, N, I, O, N, ' ou des espaces. 

Il faut valider le type de donnée avant d'interroger la base de données. 