# French texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices, Tapkasa is not a certified cash register software. The build adds no-break spaces before : ; ? !
# No long dashes.

T = dict(
    html_lang='fr', hreflang='fr', og_locale='fr_FR', name='Français', currency='EUR',
    gp_badge='badge-googleplay-en.png', as_alt="Télécharger dans l'App Store", gp_alt='Disponible sur Google Play',
    brand_sub='La caisse de poche', menu='Langue',
    try_btn='Essayer dans le navigateur',
    qr_alt="Code QR pour télécharger l'application Tapkasa",
    qr_text="Visez le code avec l'appareil photo de votre téléphone pour télécharger Tapkasa.",
    note='Gratuit pour 10 notes payées par jour. Sans inscription.',
    sticky='La caisse de poche',
    ld_desc="Une caisse simple sur téléphone pour les stands de marché, marchés de Noël, kermesses et fêtes "
            "d'association. Elle calcule la monnaie à rendre, numérote les commandes, gère les consignes et "
            "fonctionne sans internet. Les données restent sur l'appareil.",
    offer="Gratuit pour 10 notes payées par jour. Tapkasa Pro est un abonnement dans l'application (mensuel ou "
          "annuel).",
    h_how='Comment ça marche',
    how=[
        ('Saisissez votre carte', 'Chaque article a un nom, un prix et une couleur. Quelques minutes suffisent à la '
                                  "maison, ou partez de la carte d'exemple."),
        ('Touchez les cartes', "Un appui ajoute un article, un appui long en retire un. Le montant à payer reste "
                               "affiché en bas de l'écran."),
        ('Espèces ou carte', 'En espèces, Tapkasa calcule la monnaie à rendre. La carte bancaire passe sur votre '
                             'propre terminal et vous indiquez simplement le paiement dans Tapkasa.'),
    ],
    h_feat='Ce que fait Tapkasa',
    feats=[
        ('La monnaie sans calcul mental', 'Touchez le billet que vous avez reçu et vous voyez combien rendre.'),
        ('File de commandes numérotées', "Chaque note payée reçoit un numéro et attend dans la file jusqu'à ce que "
                                         'vous la marquiez comme servie.'),
        ('Caisse et comptoir sur deux téléphones', 'Le second appareil affiche les commandes et peut les lire à voix '
                                                   'haute. La liaison fait partie de Tapkasa Pro.'),
        ('Fonctionne sans réseau', 'Tout tourne sur le téléphone. Deux iPhone ou deux téléphones Android se relient '
                                   'même sans internet.'),
        ('Consignes', 'La consigne du gobelet ou de la tasse et son retour sont des articles à part, séparés des '
                      'ventes dans le récapitulatif.'),
        ('Vos données restent chez vous', 'Ni compte ni cloud. Vous enregistrez une sauvegarde dans un fichier, où '
                                          'vous voulez.'),
    ],
    h_shots='À quoi ressemble Tapkasa',
    shot_alts=["Écran de vente de Tapkasa : cartes d'articles en couleur avec les prix et le montant à payer",
               'File de commandes numérotées sur le second téléphone',
               'Récapitulatif des ventes avec le détail de la TVA'],
    h_not="Ce que Tapkasa n'est pas",
    nots=[
        "Ce n'est pas un logiciel de caisse certifié (NF525 ou équivalent) et il ne transmet rien à l'administration "
        "fiscale. Le récapitulatif des ventes n'est ni un ticket de caisse ni une facture.",
        "Il n'encaisse pas les paiements par carte. Vous prenez la carte sur votre propre terminal, Tapkasa note "
        "seulement la vente.",
        "Il n'imprime ni tickets ni jetons.",
    ],
    not_p="Il convient aux associations, aux kermesses et aux ventes occasionnelles qui n'ont pas l'obligation "
          "d'utiliser un logiciel de caisse certifié, ou comme aide à côté de celui-ci. Vérifiez vos obligations "
          "auprès de votre comptable ou du service des impôts.",
    h_price='Combien ça coûte',
    price=[
        'Gratuit : toute la carte, les récapitulatifs, les consignes et la sauvegarde sur un appareil, avec 10 notes '
        'payées par jour. Une note qui ne fait que rendre une consigne ne compte pas dans la limite.',
        "Tapkasa Pro : notes illimitées et liaison entre la caisse et le comptoir. C'est un abonnement mensuel ou "
        "annuel via l'App Store ou Google Play, avec 14 jours d'essai gratuit pour les nouveaux abonnés. Le prix "
        "dans votre devise s'affiche dans l'application avant l'achat et vous pouvez résilier à tout moment dans "
        "les réglages de la boutique.",
        "Un seul abonnement suffit pour un stand : le second téléphone se relie gratuitement à l'appareil qui a "
        "Tapkasa Pro.",
    ],
    h_faq='Questions fréquentes',
    faq=[
        ('Tapkasa est-il gratuit ?',
         "Oui, jusqu'à 10 notes payées par jour sur un appareil. Les notes illimitées et la liaison de deux "
         "appareils demandent l'abonnement Tapkasa Pro, que les nouveaux abonnés peuvent essayer gratuitement "
         "pendant 14 jours."),
        ('Est-ce un logiciel de caisse certifié ?',
         "Non. Tapkasa compte et enregistre vos ventes, mais ce n'est pas un logiciel de caisse certifié, il ne "
         "transmet rien à l'administration et n'émet ni tickets ni factures."),
        ('Où sont mes données ?',
         "Uniquement sur votre appareil. Tapkasa n'a ni comptes ni cloud. Vous pouvez enregistrer une sauvegarde "
         "dans un fichier et la charger sur un nouveau téléphone."),
        ('Quelles langues et quelles devises ?',
         'Neuf langues (français, anglais, allemand, espagnol, italien, portugais, polonais, tchèque et slovaque) et '
         "33 devises, dont l'euro et le franc suisse."),
    ],
    cta_h='Essayez Tapkasa avant votre événement',
    h_more='Autres guides',
    f_support='Assistance', f_privacy='Confidentialité', f_terms="Conditions d'utilisation",
    f_app='Ouvrir Tapkasa dans le navigateur', f_langs='Langues', f_operator='Éditeur',
    pages=dict(
        stall=dict(
            path='fr/', card='Caisse pour stand de marché',
            title='Caisse pour stand de marché sur téléphone, sans réseau | Tapkasa',
            desc="Une caisse simple pour votre stand, sur votre téléphone : cartes d'articles en couleur, monnaie "
                 "calculée, commandes numérotées sur un second téléphone, consignes. Fonctionne sans internet.",
            h1='La caisse de votre stand tient dans la poche',
            eyebrow='Pour iPhone, Android et navigateur',
            lede="Vous saisissez votre carte, vous touchez les cartes de couleur et Tapkasa compte : le montant à "
                 "payer, la monnaie à rendre et la recette de la journée. Sans inscription, sans matériel et sans "
                 "internet.",
            sections=[
                ('Sur le stand, concrètement',
                 "<p>Un client demande deux vins chauds et une crêpe. Vous touchez deux fois le vin chaud, une fois "
                 "la crêpe, et le montant s'affiche en bas. Il vous tend un billet de 20, vous touchez 20 et Tapkasa "
                 "indique la monnaie à rendre. Cela prend quelques secondes et personne ne calcule de tête, pas même "
                 "le bénévole qui tient la caisse pour la première fois.</p>"),
                ('Deux téléphones : caisse et comptoir',
                 "<p>Quand la file s'allonge, un téléphone encaisse et l'autre affiche les commandes avec leur "
                 "numéro. Au comptoir, vous cochez ce qui est prêt et les nouvelles commandes peuvent être lues à "
                 "voix haute, sans regarder l'écran les mains pleines. Deux iPhone ou deux téléphones Android se "
                 "relient directement, sans internet. Un iPhone avec un Android a besoin d'une connexion.</p>"),
                ('La consigne du gobelet',
                 "<p>Le bouton « + Ajouter une consigne » crée deux articles : Consigne et Retour consigne. Le "
                 "gobelet rendu est déduit de la note et le récapitulatif affiche à part les consignes encaissées "
                 "et rendues, sans les mélanger aux ventes.</p>"),
                ('Le soir, vous connaissez votre recette',
                 "<p>Le récapitulatif donne le total des ventes, les espèces et la carte séparément, et le nombre "
                 "d'articles vendus. Vous pouvez enregistrer le récapitulatif en PDF, par exemple pour votre "
                 "comptable.</p>"),
            ],
            faq=[
                ('Faut-il une connexion internet ?',
                 "Non. La vente, les récapitulatifs et la sauvegarde fonctionnent sur le téléphone. Internet ne sert "
                 "qu'à télécharger l'application, à acheter Tapkasa Pro et à relier un iPhone à un Android."),
                ('Un bénévole peut-il tenir la caisse ?',
                 "Oui. Une vente, c'est un appui sur une carte de couleur puis le choix Espèces ou Carte. Un article "
                 "ajouté par erreur s'enlève par un appui long."),
            ],
        ),
        xmas=dict(
            path='fr/marche-de-noel/', card='Caisse pour marché de Noël',
            title='Caisse pour marché de Noël : consigne et monnaie | Tapkasa',
            desc="Une caisse sur téléphone pour le marché de Noël : vin chaud en un geste, consigne du gobelet, "
                 "monnaie calculée. Fonctionne sans réseau et sans inscription, 10 notes par jour gratuites.",
            h1='Une caisse pour le marché de Noël : vin chaud, crêpes et consigne',
            eyebrow="Marchés de Noël et marchés de l'Avent",
            lede="La place est noire de monde, le réseau sature et la file s'allonge devant le chalet. Tapkasa "
                 "fonctionne sur votre téléphone sans internet, calcule la monnaie et suit les consignes des "
                 "gobelets. La préparation prend quelques minutes.",
            sections=[
                ('La consigne du gobelet sans pagaille',
                 "<p>Dans Menu, touchez « + Ajouter une consigne » et saisissez le montant, par exemple 1 €. Tapkasa "
                 "crée deux articles : Consigne et Retour consigne. Vous ajoutez la consigne avec le vin chaud, vous "
                 "touchez le retour quand le gobelet revient et le montant est déduit de la note. Si le client rend "
                 "seulement son gobelet, Tapkasa indique combien lui rendre.</p>"
                 "<p>Le récapitulatif sépare les consignes encaissées et rendues. Le soir, vous savez combien de "
                 "gobelets sont encore dehors et quelle est la vraie recette.</p>"),
                ('Quand le réseau tombe sur la place',
                 "<p>La vente, la monnaie et le récapitulatif tournent sur le téléphone lui-même. Tapkasa ne se "
                 "connecte nulle part et ne vérifie rien en ligne : un réseau saturé ou un forfait épuisé ne vous "
                 "arrête pas en plein coup de feu.</p>"),
                ('La file devant le vin chaud',
                 "<p>Un téléphone encaisse, le second affiche au comptoir les commandes numérotées et les lit à "
                 "voix haute. Le client reçoit un numéro et personne ne crie d'un bout à l'autre du chalet. Deux "
                 "iPhone ou deux téléphones Android se relient directement, sans Wi-Fi ni données mobiles.</p>"),
                ('Conseils pour les jours de froid',
                 "<ul><li>Arrondissez vos prix pour rendre la monnaie facilement : 3, 4, 5 €.</li>"
                 "<li>Préparez la carte chez vous, au chaud, et placez les meilleures ventes en haut.</li>"
                 "<li>Prenez une batterie externe. L'écran reste allumé pendant la vente et le froid vide plus vite "
                 "la batterie.</li>"
                 "<li>Enregistrez une sauvegarde dans un fichier avant le premier jour de marché.</li></ul>"),
            ],
            faq=[
                ('Le retour de consigne compte-t-il dans la limite gratuite ?',
                 'Non. Une note qui ne fait que rendre une consigne ne compte pas dans les 10 notes payées par '
                 'jour.'),
                ('La version gratuite suffit-elle pour un marché de Noël ?',
                 "Pour un petit stand avec quelques ventes par jour, oui. Pour un marché très fréquenté, Tapkasa Pro "
                 "est plus adapté : les nouveaux abonnés ont 14 jours gratuits, soit deux week-ends de l'Avent. "
                 "Tapkasa vous prévient avant que la limite soit atteinte."),
            ],
        ),
        club=dict(
            path='fr/kermesse/', card="Caisse pour kermesse et fête d'association",
            title="Caisse pour kermesse et fête d'association sur téléphone | Tapkasa",
            desc="Une caisse sur téléphone pour la kermesse de l'école, la buvette ou la fête de l'association : les "
                 "bénévoles touchent les articles, la monnaie est calculée, le trésorier reçoit le total en PDF.",
            h1="Une caisse pour la kermesse et la fête de l'association",
            eyebrow='Kermesses, buvettes, lotos, vide-greniers',
            lede="Les bénévoles se relaient à la buvette et le soir, le trésorier veut savoir ce qui est rentré. "
                 "Tapkasa garde les prix, calcule la monnaie et additionne la recette sur un téléphone. Sans "
                 "inscription et sans formation.",
            sections=[
                ('Tous les bénévoles savent s’en servir',
                 "<p>Les articles sont de grandes cartes de couleur : personne ne cherche dans une liste ni ne "
                 "calcule de tête. On touche ce que le client demande, on choisit Espèces ou Carte, et en espèces "
                 "l'écran indique la monnaie à rendre. Pour la relève, il suffit de passer le téléphone.</p>"),
                ('Le soir, un total exact pour le trésorier',
                 "<p>Le récapitulatif donne le total des ventes, les espèces et la carte séparément, et le nombre "
                 "d'articles vendus. Envoyez-le en PDF au trésorier ou au bureau. Après la fête, choisissez "
                 "« Clôturer l’événement » : la recette part dans les archives et vous repartez de zéro la fois "
                 "suivante.</p>"),
                ('Ni compte, ni vérification, ni commission',
                 "<p>Tapkasa ne demande ni inscription, ni numéro d'association, ni coordonnées bancaires, et ne "
                 "prélève rien sur la recette. L'argent va dans votre caisse. Les données restent sur le téléphone "
                 "utilisé à la buvette.</p>"),
                ('Grande fête : buvette et cuisine séparées',
                 "<p>Pour un bal ou une fête de village, un téléphone peut encaisser à la buvette pendant qu'un "
                 "autre affiche les commandes en cuisine. Un seul abonnement Tapkasa Pro suffit, avec 14 jours "
                 "d'essai gratuit pour les nouveaux abonnés.</p>"),
            ],
            faq=[
                ("La version gratuite suffit-elle pour la kermesse de l'école ?",
                 "Pour une petite fête, oui : 10 notes payées par jour sont gratuites. Si vous attendez plus de "
                 "monde, activez Tapkasa Pro à l'avance ; les nouveaux abonnés ont 14 jours d'essai gratuit."),
                ("L'association doit-elle s'inscrire ?",
                 "Non. Vous téléchargez Tapkasa et vous l'ouvrez. Aucun compte n'est créé et rien n'est vérifié."),
            ],
        ),
    ),
)
