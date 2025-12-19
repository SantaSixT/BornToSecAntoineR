Code de base : 

echo $row['comment']; 

 

Code corrigé  

echo htmlspecialchars($row['comment'], ENT_QUOTES, 'UTF-8'); 

 

convertir les caractères spéciaux en entités HTML inoffensives avant de les afficher à l'écran. 

    < devient &lt; 

    > devient &gt; 

    " devient &quot; 

    ' devient &#x27; 