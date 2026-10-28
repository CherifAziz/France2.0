# Avenant méthodologique de la reprise du 28 octobre 2026

Cet avenant complète le protocole hérité. Il ne modifie ni les sources brutes ni les objectifs du commanditaire. Les statuts de preuve et la séparation PP/ETP/EQTP demeurent obligatoires.

## Accès, archivage et lecture

L'ancien outil temporaire Claude est remplacé par `scripts/fetch.py`. Il archive l'original, une conversion texte lorsque possible, l'URL demandée et finale, le statut HTTP, l'heure UTC, le type de contenu, les octets et le SHA-256 complet. Un changement de contenu sous le même nom est refusé : l'ancien instantané et son manifeste sont conservés. Un échec de réaccès est enregistré séparément. Le contenu téléchargé n'est jamais exécuté.

`html2text` est disponible dans les dépendances locales du projet. `pdftotext` n'est pas présent dans le PATH vérifié ; le repli `pypdf` est déclaré dans chaque manifeste. Ses repères `[PAGE N]` sont les pages du fichier PDF, à distinguer de la pagination imprimée. Des avertissements sur les textes tournés ou les polices interdisent de considérer l'absence d'un mot dans la conversion comme preuve de son absence dans le document. Les tableaux XLSX sont privilégiés pour les nombres ; une page complexe doit être relue visuellement avant citation déterminante.

Un HTTP 200 n'est pas une preuve suffisante d'accès au document : certains index budget.gouv.fr renvoient un défi Incapsula de quelques centaines d'octets. Le téléchargement détecte ce cas, et les registres distinguent ces pages des PDF directement accessibles. Une URL d'API erronée retournant 404 ne démontre pas un blocage de l'API entière. Le flux OCDE SHA vérifié a répondu après correction du premier identifiant testé.

Le routage de recherche `agent-reach` a été consulté ; ses exécutables, `conda` et `mcporter` n'étaient pas disponibles dans le PATH. Les recherches utilisent donc le moteur connecté et la lecture des sources primaires via `requests`, sans changement de configuration globale.

## Trois périmètres financiers distincts

Le prompt de reprise indique que la contribution de retraite « ne disparaît pas quand un poste est supprimé ». Cette phrase doit être précisée selon le niveau d'analyse, sans changer l'exigence d'éviter une économie fictive de pensions.

1. **Budget de l'employeur complet** : à taux de cotisation donné, un emploi non pourvu peut effectivement réduire la cotisation versée par cet employeur. C'est notamment pertinent pour la collectivité ou l'hôpital versant à la CNRACL.
2. **Coût normalisé hors retraite** : on exclut les financements de pensions pour isoler le coût d'emploi directement comparable. « Hors CAS Pensions » dans un PAP n'exclut pas nécessairement les autres cotisations vieillesse. Il faut vérifier CNAV, Ircantec, RAFP et autres régimes avant d'appeler une donnée « hors toutes pensions ».
3. **APU consolidées** : la baisse de la cotisation d'un employeur vers un régime classé dans les APU diminue aussi la recette de ce régime, dont les pensions liquidées restent dues. La baisse d'un transfert interne n'est pas une économie consolidée du même montant. Le CAS est en outre doté d'une contribution d'équilibre ; sa lecture budgétaire diffère des cotisations imputées des comptes nationaux.

Le détail des sources primaires, pages et coûts PAP figure dans le volet `01c_couts_entree_pensions.md` dès sa production. Le paramètre du moteur `cout_entree_hors_pension` ne doit pas recevoir automatiquement une moyenne PAP HCAS, encore moins le salaire d'un partant. Les coûts du programme 156 ou 218 ne constituent pas une moyenne nationale administrative.

Un redéploiement conserve un emploi et une rémunération ; un transfert entre deux APU appelle des effectifs et coûts de destination. Le moteur les distingue désormais. Le registre national des viviers devra également garantir que les effectifs d'arrivée ne sont pas oubliés ou comptés comme supprimés ailleurs.

## Statut du modèle

Les cas synthétiques des tests démontrent la cohérence de calcul du moteur dans les situations contrôlées. Ils n'établissent aucun potentiel de réforme national. Les hypothèses économiques, départs mobilisables, taux de conversion des gains IA, trajectoires de service et viviers disjoints doivent encore provenir des recherches. Aucun résultat de test ne sera repris comme donnée française.

Le modèle applique les réformes par ordre au reliquat du vivier et partage annuellement les départs réellement disponibles. Il distingue les flux d'ETP de l'année, les stocks de postes évités et les cumuls de montants. L'investissement antérieur à l'horizon doit être explicite et est présenté séparément. La convention de première année, pleine ou fractionnée, doit être affichée.

## Livraisons successives

Le cahier des charges autorise des livrables successifs si le travail dépasse une seule réponse. Les premières notes de recherche et bases sont livrées comme telles, avec les lacunes documentées. Elles ne doivent pas être rebaptisées « rapport final », ni être prolongées artificiellement en 80 pages. Le rapport en 17 parties, les 25 fiches A–M, les quatre scénarios nationaux, le classeur financier et la synthèse finale restent soumis aux phases de preuve, diagnostic, chiffrage et contradiction prévues dans le prompt.
