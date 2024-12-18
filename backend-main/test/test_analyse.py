from app.models.user import User
from .conftest import (
    client,
    client_with_user,
    client_with_user_password_forgotten,
    generate_token_admin,
    generate_token_user,
    client_with_user_and_multiples_analysis,
)
import io

bigtext = """
    Nous avons fait face lors de la réalisation de nos travaux de R&D à un ensemble de verrous techniques, que nous présentons dans la suite. 

-	Comment élaborer un schéma de prédiction générique ? i.e. sur quels modèles se baser pour proposer un outil applicable et/ou généralisable à différents cas de mesures ?
-	Lors de la réalisation d’une l’analyse, sur quelles données se baser pour identifier les éléments à maintenir, et ensuite prévoir en temps réel (au fur et à mesure de l’utilisation) les usures identifiées. Autrement dit, est-il nécessaire de se baser sur un panel grandeur nature des données à utiliser ? Ou, est-il nécessaire de réaliser un échantillonnage des données collectées ?
-	Quelles sont les méthodes les plus efficientes pour identifier les meilleures valeurs d’usures, à injecter au niveau de notre modèle ? Cela permet de retourner avec précisions et en temps réel les meilleures actions correctives sur une pièce donnée. 
-	Comment identifier le niveau de précision toléré dans le cadre des pièces très sensibles (ex. plaquettes de freins, roulements, etc.) ? Cela permet d’améliorer la précision de notre outil.
-	Est-il possible d’identifier les causes générales des usures ? Comment agréger et analyser les masses très importantes de données collectées à partir d’un parc important de véhicules connectés ? 

Nous détaillons dans la suite les travaux de modélisation (étude théorique) et de conception réalisés dans le cadre de notre projet de R&D. 

Nous avons entamé nos travaux de R&D  par une étude théorique nous permettant de tracer les fondements de notre méthode de prédiction, appliquée à un dispositif particulier, i.e. les plaquettes de freins. 

La finalité serait de développer une solution informatique complète intégrant à la fois nos modèles d’analyse et de traitement de données et l’ensemble des modèles d’identification d’usures que nous avons développé. Ce système embarqué, doit permettre le traitement et l’analyse continu des données et une remontée, en temps réel, des degrés d’usures. Dans une première étape nous nous sommes intéressés à un cas particulier et complexe des usures, i.e. les plaquettes de freins. 
.2.1.3.1	Étude théorique 
La méthode de prédiction doit être perçue par l’utilisateur de façon identique à celle établie pour la consommation d’essence. L’utilisateur doit pouvoir savoir en temps réel dans combien de kilomètres ses plaquettes devront être remplacées. Les calculs se basent sur les derniers freinages effectués lors des derniers Km. 

Les données relevées et mise à disposition de l’utilisateur doivent être les plus concrètes possibles. Nous réalisons pour cela un traitement spécifique des données. En effet, les données collectées constituent des masses importantes. Nous devons développer pour cela des solutions logicielles pour l’acquisition, le traitement et le tri des données. Ces données sont collectées par des boitiers connectés aux véhicules. Ces données seront par la suite injectées en entrée de notre modèle de prédiction. 

Par la suite le schéma de prédiction développé, peut être appliqué à d’autres éléments du véhicule. De cette façon l’utilisateur sera informé de l’état réel de son véhicule de la même façon qu’il est informé de l’état de la batterie ou de la mémoire de son smartphone. Le véhicule fera partie des objets connectés et son entretient ne sera plus conservé dans un brouillard de seuils et de limites incomprises.

A.	Détermination de l’usure

La tribologie décrit la science de l’usure et des frottements. C’est une science extrêmement précise qui demande beaucoup de mesures délicates (de l’ordre du nanomètre) et qui implique des formules complexes invoquant de nombreuses données. Les calculs sont donc longs et s’appliquent difficilement à un cas comme le nôtre (problématique de temps réel). Cependant il en ressort des formules simplifiées, dites grossières, mais avec un recul suffisant elles permettent de se faire une idée intéressante de l’usure. 

Les mesures qui vont nous concerner sont de l’ordre du millimètre et s’étendent sur plusieurs milliers de kilomètre. Il n’est donc pas nécessaire d’invoquer des formules complexes. Les formules simples, impliquant un nombre limité de variables offriront un aperçu idéal de l’usure des plaquettes de frein.

Type d’usures rencontrées

L’usure abrasive correspond au cas où un corps dur déforme plastiquement, avec ou sans enlèvement de matière, un corps plus mou. On distingue à cet effet : 

-	L’usure abrasive à deux corps : des sillons sont formés parallèlement à la direction de déplacement, par les aspérités du corps le plus dur, 
-	L’usure abrasive à trois corps : des particules dures présentes dans l’interface déforment plastiquement les surfaces en frottement en créant des empreintes.

Suivant les cas, l’usure abrasive peut engendrer des endommagements par déformation plastique, des enlèvements de matière par phénomène de coupe et/ou par fatigue superficielle. L’usure abrasive est favorisée : 

-	par l’accroissement de température, par l’humidité, l’agressivité chimique de l’ambiance (lorsque l’abrasion agit par effet de coupe).

Dans le cas de l’abrasion à trois corps, la nature et l’acuité des phénomènes dépendent des formes, granulométries des particules abrasives, de la vitesse relative et de l’angle d’attaque de l’abrasif sur le substrat.

L’usure abrasive mettant en jeu, au niveau élémentaire, des phénomènes d’ordre mécanique, les paramètres dépendant des matériaux sont notamment : la dureté ou la limite d’élasticité, les contraintes résiduelles, la ténacité, la structure (homogénéité, taux d’écrouissage...), les propriétés thermomécaniques dans le cas de sollicitations en température. La dureté respective des corps en présence est un élément déterminant. 

Lors du freinage, les plaquettes (corps mou) sont appliquées sur le disque (corps dur) avec une certaine force et sur une certaine distance. La durée de vie d’une plaquette est inférieure à celle du disque, 30000Km pour les plaquettes avant contre 80000Km pour les disques avant, donc on considèrera ici le disque comme peu impacté par l’usure d’un jeu de plaquettes.

L’usure de la plaquette entraine la formation de poussière, raye le disque et prend sa forme. Donc selon la description précédente, on considèrera l’usure du freinage comme abrasive à trois corps. 

B.	Récupération des Données

L’entreprise Dunasys a mis au point un boitier pouvant relever toutes les informations du réseau CAN d’un véhicule. L’objectif de départ était de ne remonter que les défauts signalés par les différents éléments de la voiture (capteur, ordinateur de bord, CDI, etc.). Au final le boitier nous permet d’avoir un visuel sur toutes les informations du véhicule. Nous nous servirons donc dans cette mine d’information en choisissant scrupuleusement les données pertinentes par rapport à l’équipement étudié.

C.	Données du véhicule

Les informations du boitier doivent être corrélées avec les cotations du véhicule. Dans notre cas, nous avons pris en compte les mesures des roues, des disques de frein et des pistons des étriers de frein. La mesure des roues permet de calculer la distance parcourue par tour de roue ainsi que la longueur de la bande de freinage du disque utilisée lors d’un freinage. Le diamètre des pistons permet de calculer la force exercée lors d’un freinage.

Données utiles

Notre objectif est donc de minimiser le nombre de données afin d’en extraire les principales et de ne pas s’encombrer de données inutiles. Ce filtrage nous permet d’identifier les données les plus utiles pour un traitement ultérieur.

-	Les informations du véhicule : 

Le modèle du véhicule au format de la référence chez le constructeur sera nécessaire. Il permettra d’identifier toutes les caractéristiques techniques des équipements présents. Dans le cas de l’étude sur le freinage, cela permet de connaître la taille des roues, des disques de freins, le format des plaquettes, etc. 

-	Les informations relevées par le boitier : 

La sélection de ces informations est importante pour ne pas surcharger le traitement des données. Ainsi nous sélectionnerons exclusivement les trames ou même les variables intéressantes pour nos études en excluant toutes les autres. Cela aura pour effet de faciliter la compréhension des données, leur traitement et leur stockage.

À titre d’exemple, sur toutes les informations pouvant être remontées par le réseau CAN du véhicule, seules trois seront retenues pour les calculs d’usure des plaquettes de frein : 

	la distance parcourue par les roues : DISTANCE_ROUES, unité en mètre, 
	la pression dans le maître-cylindre de frein : PRESSION_MAITRE_CYL, unité en bar,
	le contact du frein, ce contact est divisé en trois signaux différents, un pour chaque signal lumineux : CONTACT_FREIN1, CONTACT_FREIN2, CONTACT_FREIN3, « 1 » ou « 0 ».

Ces données sont remontées à certains intervalles suffisamment rapprochés (quelque dizaine de ms) pour donner une précision suffisante aux différents calculs.

D.	Méthodes de calcul

Pour tous nos calculs, nous considérons une usure uniforme sur les deux plaquettes, ce qui induit que tous nos calculs ne prennent en compte qu’une seule plaquette associée à son piston.

Détermination de l’usure

Les calculs sont basés sur la loi d’usure d’Archard : 

 
Où on a : 

-	U : volume de matière enlevé exprimé en mm3, 
-	K : coefficient d’usure (sans dimension),
-	Q : la force appliquée exprimée en Kgf, 
-	D : la distance sur laquelle le frottement a lieu exprimé en mm (ici la bande de freinage), 
-	H : le coefficient de dureté  de Vickers exprimé en Kgf.mm-2.

Le coefficient « K » dépend de la nature des deux matériaux en contact. Le graphique (cf. Figure 2 5) suivant montre un ordre de grandeur dans le cas de contact non métal/non métal et métal/métal : 

 
Figure 2 5. Présentation d’un ordre de grandeur dans le cas de contact non métal/non métal et métal/métal 
.2.1.3.2	Application à l’expérience
Nous pouvons donc en déduire d’après les conditions d’usures de la plaquette de frein, que nous avons à faire à une abrasion de type polissage dans le cas d’un frottement autre que métal/métal (K=10-6). En effet la composition des plaquettes de frein ne peut être considérée comme une forme de métal du fait de la composition de garniture contenant un alliage de différents composée organique comme le kevlar ou encore la céramique.

-	Le coefficient de dureté H : provient de la mesure de la dureté par la méthode de Vickers. Cette méthode offre une échelle très large dans les essais de dureté de matériau. C’est très souvent l’échelle de référence. Il existe d’autres échelles comme celle de Knoop, Rockwell ou Brindell. Il existe une méthode pour passer facilement de l’échelle de Brindell à celle de Vickers. Ces deux échelles sont très proches mais celle de Vickers reste la plus large et la plus précise. 

La mesure de dureté de Vickers consiste à mesurer l’empreinte laissée par une pointe pyramidale de base carré et d’angle au sommet entre faces égal à 136° (cf. Figure 2 6).
 
Figure 2 6. Schéma de la mesure de dureté de Vickers 
Nous réalisons donc une mesure des diagonales avec un appareil optique. C’est la moyenne des diagonales qui sera prise en compte lors du calcul ainsi que la force et la durée d’appuis qui sont normalisées. 

 

Avec « F » la force appliquée en Newton, « d » la moyenne des diagonales en millimètre. Ce coefficient de dureté est lisible sur un abaque en fonction de la force d’appuis. Les fabricants de matériaux, tels que les fonderies, donnent un coefficient de Vickers pour chaque matériau.

-	La force « Q » est mesurée d’après la pression du liquide dans le maître-cylindre de frein. Nous considérons un freinage normal, ne faisant pas intervenir les systèmes d’assistance au freinage. La pression peut donc être considérée comme la même dans tout le système de freinage. Pour déterminer la force appliquée sur les plaquettes, nous calculons ensuite la force appliquée par les pistons de l’étrier de frein. En connaissant les dimensions de ce dernier, nous pouvons en déduire la force.

Nous savons que la force est égale au produit de la pression par la surface. Il nous faut donc connaître le diamètre d’un piston de l’étrier.

-	La distance « D » est la distance sur laquelle le frottement est effectué. Ici elle correspond à la longueur de la bande de freinage sur le disque de frein. Nous devons donc mettre au point un coefficient permettant de passer de la distance parcourue par la roue, à la distance parcourue sur  le disque.

Il s’avère difficile de trouver un coefficient de dureté pour la garniture des plaquettes de frein (souvent faisant partis du secret de fabrication). Sans avoir de certitude, il faut donc trouver un ordre de grandeur afin de se rapprocher le plus possible du réel. 

Nous prenons dans la suite comme référence la dureté du disque de freins. La grande majorité des véhicules ciblés par notre étude se trouvent équipés de disque en fonte graphite lamellé. Ce matériau possède des coefficients HV compris entre 200 et 350 en fonction de l’utilité à laquelle il est associé. La norme automobile SAE J431 G3000 défini quel type de fonte doit être utilisée pour les disques de frein dans l’automobile sur des véhicules type voiture et petit camion. Cette fonte doit, selon cette norme, posséder un HV de 225.

En considérant la loi d’Archard, nous estimons que le coefficient de dureté est inversement proportionnel à l’usure. 

Le fait que les disques s’usent moins vite que les plaquettes (de l’ordre de 63%). Nous estimons donc la dureté des garnitures de plaquette de frein à 63% de celle des disques, un HV d’environ 141.

Les études précédentes sur l’usure des plaquettes de frein (méthodes empiriques), ont montré que ni la force de freinage ni la vitesse n’influaient sur l’usure de la plaquette. Il se trouve que plus le freinage est long et plus les plaquettes s’usent, peu importe la vitesse ou la température, en restant toujours dans les limites de fonctionnement optimale d’une plaquette de frein. Ces observations découlent du fait de la réglementation qui impose aux fabricants de garniture de plaquette de frein, de conserver un coefficient de frottement stable dans une large plage de température. Cette température étant liée à la vitesse de frottement. La donnée primordiale est la distance sur laquelle les freins sont utilisés. 
.2.1.3.2.1	Détermination de la bande de freinage
Pour commencer il est nécessaire de connaître la distance parcourue en fonction du nombre de tour de roue, il faut donc calculer le périmètre de la roue. Sur une roue de voiture les cotes sont données de la façon suivante : 

Largeur du pneu / hauteur du pneu / diamètre de la jante

-	Largeur du pneu : en mm, 
-	Hauteur du pneu : pourcentage de la largeur, 
-	Diamètre de la jante : en pouce (rappel : 1 pouce = 25,4mm). 

Le diamètre de la roue s’obtient avec le calcul suivant : 

 

Le périmètre est donnée par : 

 

Dans le cas du disque, nous prenons le diamètre moyen = diamètre extérieur – diamètre intérieur. 

Le rapport   donne le pourcentage de tour de roue pour 1 mètre parcouru. Ce pourcentage s’applique au périmètre du disque afin de connaître la longueur de la bande de freinage utilisée pour 1 mètre parcouru. 
.2.1.3.2.2	Application au véhicule Peugeot 407 berline 1.6 HDI
Les dimensions relevées sur les roues sont 205/55/16 : 

 

 

 

Les disques de frein avant ont un diamètre extérieur de 283mm et un diamètre intérieur de 71,1mm, le diamètre moyen « d » est donc de 211,9mm. 

 

 

La longueur de la bande de freinage utilisée pour 1 mètre parcouru est de 335,3mm. 

Pour l’application nous avons relevé les informations suivantes : 

-	La distance parcourue lors du freinage. C’est-à-dire la distance parcourue entre le moment ou la pression dans le maître-cylindre était supérieure à zéro et celle où elle est retournée à zéro. 
-	La pression du maître-cylindre. 

De la distance parcourue nous avons déduit la longueur de la bande de frottement grâce au calcul précédent. Nous avons calculé la pression moyenne lors de ce freinage et en avons déduit la force moyenne exercée par un piston sur une plaquette. Il est important d’adapter nos relevés et d’améliorer notre formule au cas réel : comme expliqué plus haut, l’usure dépend essentiellement de la distance de frottement. Cependant, notre formule fait intervenir la pression de façon significative. Il faut donc que ce chiffre soit proche d’une constante, et c’est pourquoi une moyenne est justifiée. Pour se rapprocher du cas réel au plus possible, il faudra : 

-	Prendre en compte une grande quantité de freinages afin que cette moyenne n’aille pas dans les extrêmes et fausse nos prédictions.  
-	Réduire le nombre de relevés de pression à ceux dépassant un certain seuil.

Les calculs que nous avons présentés précédemment mettent en évidence deux éléments :

-	Le premier calcul permet de définir la quantité de matière retirée de la plaquette de frein lors du freinage. Cette donnée n’apporte pas beaucoup d’information sur l’usure de la plaquette. Sur un freinage d’une trentaine de mètre la quantité est bien entendue infime. 
-	Le deuxième calcul par du principe suivant : en notant qu’un millimètre d’épaisseur de la garniture de la plaquette est la valeur critique. Sur combien de kilomètres devons-nous freiner de la même façon que le dernier freinage, pour user la garniture jusqu’à sa valeur critique ? 

Nous remplaçons donc dans la formule : 

o	La quantité de matière que nous devons enlever pour arriver à la valeur critique, en se basant sur les cotations du modèle de plaquette correspondant au véhicule. 
o	Nous recherchons maintenant la longueur de la bande de roulement nécessaire pour user la garniture jusqu’à sa valeur critique. 

Pour nous permettre de nous faire une idée du bon ordre de grandeur de notre résultat, nous nous somme appuyé sur une étude de PSA qui concernait l’utilisation des freins de plusieurs classes de véhicule sur une période donnée.

Pour notre projet nous n’avons, pour le moment, pris en compte que les données relevées sur l’échantillon de véhicule particulier avec boîte de vitesse automatique de moyenne classe sur le territoire français. L’étude de PSA conclue de la façon suivant : 

Sur une période de 3 ans ou 60000Km, pour les véhicules particuliers à boîte automatique de moyenne classe, la distance parcourue en freinant (exclusion fait de l’activation des freins à l’arrêt) est de l’ordre de 6000Km. Ce qui représente 10% de la distance parcourue. Avec une distance de 24m par freinage.

Si l’on applique ce pourcentage aux 30000Km de durée de vie moyenne des plaquettes de freins nous obtenons 3000 km. Ce chiffre approximatif moyen est proche du résultat obtenu lors de nos calculs.
.2.1.3.3	Mesure et comparaison de données
Grâce aux différentes données relevées à la fois sur le véhicule (caractéristiques des équipements) et sur le réseau CAN de ce dernier, nous avons mis en place des schémas de calculs proches des ordres de grandeurs des études annexes (PSA). Nous visons par cela la réalisation d’un ensemble de tests grandeur nature avec le boitier installé sur notre véhicule et des conditions bien définies : 

-	Nous utilisons un jeu de plaquettes neuves, 
-	Nous définissons des trajets et des temps de roulages, afin d’observer la corrélation entre le réel et les données du boitier. Cela nous permettra d’augmenter le niveau de confiance du relevé de donnée, 
-	Nous mettons en place des mesures à intervalles kilométriques réguliers, 
-	Nos mesures concernent les 4 plaquettes des freins avant, 
-	Nos mesures sont effectuées par dépose des plaquettes avant et contrôles avec pieds à coulisse sur trois endroits de la plaquette (les extrémités et le centre).

Nous réalisons par la suite trois séries d’essais dans différentes conditions afin d’effectuer des comparaisons, i.e. (1) tests en conditions normales, (2) tests en conditions sportives et (3) tests en conditions douces. 

Dans le cadre de nos travaux futurs, nous envisageons de développer un ensemble d’algorithmes intégrant les modèles théoriques que nous avons commencé à tester en 2015. Nous devrons également finaliser notre outil logiciel, au niveau duquel nous allons intégrer ces algorithmes. La solution complète sera testée sur les véhicules connectés à un boitier Dunasys.

Enfin, notre application sera étendue pour intégrer d’autres modèles de prédiction des usures pour d’autres composants d’un véhicule, i.e. pneus, disques de freinage, roulements, courroies, etc.
    """


def test_create_analyse(client_with_user_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )

    response = client_with_user_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200

def test_create_analyse_sub(client_with_user_sub_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )

    response = client_with_user_sub_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200

def test_create_analyse_sub(client_with_user_sub_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )

    response = client_with_user_sub_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200

def test_create_analyse_json_wrong(client_with_user_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        json={"text": "Your input text here"},
    )
    assert response.status_code == 400


def test_create_analyse_not_enough_credit(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    text = "lala"
    response = client_with_user.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(text.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 403

def test_create_analyse_not_enough_credit_sub(client_with_user_sub_outdated):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    text = "lala"
    response = client_with_user_sub_outdated.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(text.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 403

def test_get_all_user_analyse(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user_and_multiples_analysis.get(
        "/api/v1/analyse", headers={"Authorization": enconded_jwt}
    )
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_all_user_analyse_no_analyses(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
    )
    response = client_with_user_and_multiples_analysis.get(
        "/api/v1/analyse", headers={"Authorization": enconded_jwt}
    )
    assert response.status_code == 200
    assert len(response.json) == 0


def test_analyse_integrity(client_with_user_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    response2 = client_with_user_credited.get(
        f"/api/v1/analyse/{response.json['id']}",
        headers={"Authorization": enconded_jwt},
    )
    assert response2.status_code == 200
    assert response2.data == bigtext.encode("latin-1", "ignore")


def test_download_other_user_file(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
    )
    response = client_with_user_and_multiples_analysis.get(
        "/api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 401


def test_get_info_on_analyse(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
    )
    response = client_with_user_and_multiples_analysis.get(
        "/api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15/info",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 200
    assert response.json["id"] == "3ab49c23-120b-4294-89df-27ad88deaf15"


def test_get_info_on_analyse_impostor(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
    )
    response = client_with_user_and_multiples_analysis.get(
        "/api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15/info",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 401


def test_delete_analyse(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
    )
    response = client_with_user_and_multiples_analysis.delete(
        "/api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 200


def test_delete_analyse_impostor(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
    )
    response = client_with_user_and_multiples_analysis.delete(
        "/api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 401


def test_analyse_budget(client_with_user_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    response2 = client_with_user_credited.post(
        f"api/v1/analyse/{response.json['id']}/estimate",
        headers={"Authorization": enconded_jwt},
        json={"budget": 1000, "index": 0},
    )
    assert response2.status_code == 200
    assert response2.data == b"False"


def test_analyse_budget_impostor(client_with_user_credited):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user_credited.post(
        "/api/v1/analyse",
        headers={"Authorization": enconded_jwt},
        data={
            "file": (
                io.BytesIO(bigtext.encode("latin-1", "ignore")),
                "test.txt",
                "plain/text",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    enconded_jwt = generate_token_user(
        User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
    )
    response2 = client_with_user_credited.post(
        f"api/v1/analyse/{response.json['id']}/estimate",
        headers={"Authorization": enconded_jwt},
        json={"budget": 1000, "index": 0},
    )
    assert response2.status_code == 401


def test_non_analysed(client_with_user_and_multiples_analysis):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
    )
    response = client_with_user_and_multiples_analysis.post(
        f"api/v1/analyse/3ab49c23-120b-4294-89df-27ad88deaf15/estimate",
        headers={"Authorization": enconded_jwt},
        json={"budget": 1000, "index": 0},
    )
    assert response.status_code == 400
