// Francouzština (fr-FR v App Store i v Google Play).
const LINKS = `Conditions d’utilisation : https://www.deriverge.com/tapkasa/terms.html
Politique de confidentialité : https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'l’App Store', gp: 'Google Play' },
  as: {
    locale: 'fr-FR',
    name: 'Tapkasa : caisse pour stands',
    subtitle: 'Marché de Noël, kermesse, bar',
    keywords: 'buvette,association,enregistreuse,brocante,vide-grenier,consigne,gobelet,commandes,monnaie,fête,club',
  },
  play: {
    locale: 'fr-FR',
    title: 'Tapkasa : caisse pour stands',
    shortXmas: 'Caisse pour marché de Noël et kermesse : consignes, commandes, sans internet.',
    shortYear: 'Caisse pour stand, kermesse et buvette : consignes, commandes, sans internet.',
  },
  promoXmas: 'Marché de Noël, kermesse ou vin chaud ? Saisissez le menu et encaissez sans inscription ni internet. Consigne en un geste, commandes numérotées sur un second téléphone.',
  promoYear: 'Marché, kermesse ou buvette de club ? Saisissez le menu et encaissez sans inscription ni internet. Consigne en un geste, commandes numérotées sur un second téléphone.',
  wn108: `• Consignes : la consigne d’un gobelet ou d’une tasse devient un article, le retour se fait d’un geste. Le bilan affiche séparément les consignes encaissées et rendues.
• Pas de surprise à la limite : la version gratuite vous prévient avant la limite du jour.
• Pas de réseau sur le stand ? Vous terminez quand même l’addition en cours et recevez une seule fois une réserve de 10 paiements.`,
  wn109: `Corrections et finitions pour la saison des marchés.

Nouveau depuis la 1.0.8 :
• Consignes : la consigne d’un gobelet ou d’une tasse devient un article, le retour se fait d’un geste.
• La version gratuite vous prévient avant la limite du jour.
• Pas de réseau sur le stand ? Vous terminez quand même l’addition en cours et recevez une seule fois une réserve de 10 paiements.`,
  desc: (store) => `La caisse pour stand, marché de Noël, kermesse, buvette et fête d’association. Saisissez votre menu et encaissez en deux minutes : sans inscription, sans compte, sans internet.

Tapkasa calcule et enregistre vos ventes, mais ne traite aucun paiement. Rien n’est donc bloqué ni vérifié, et il n’y a aucune commission sur les paiements. Les espèces vont dans votre caisse, la carte passe par votre propre terminal.

Un second téléphone affiche les commandes numérotées et les lit à voix haute. La consigne des gobelets et des tasses se gère d’un geste. Gratuit : 10 paiements par jour. Pour tout un marché, essayez Tapkasa Pro gratuitement pendant 14 jours.

UNE VENTE EN TROIS GESTES
• Chaque article est une carte de couleur. L’équipe la reconnaît avant même de lire le nom.
• Un appui ajoute l’article à l’addition, un appui long en retire un.
• « + Autre montant » pour tout ce qui n’est pas au menu.
• Une erreur ? Un appui annule la dernière addition.

ESPÈCES ET CARTE
• En espèces, saisissez ce que le client vous donne et Tapkasa affiche la monnaie à rendre.
• Par carte, vous encaissez sur votre propre terminal et confirmez simplement le montant.

CONSIGNES
• La consigne d’un gobelet ou d’une tasse de vin chaud est une carte comme les autres, le retour de consigne une carte à prix négatif.
• Le retour est déduit de l’addition. Une addition qui ne contient que des retours ne compte pas dans la limite du jour et n’apparaît pas dans les commandes.
• Le bilan affiche séparément les consignes encaissées et celles rendues aux clients.

COMMANDES ET COMPTOIR
• Chaque addition payée devient une commande numérotée.
• Un second téléphone ou une tablette passe en rôle Comptoir : les commandes y arrivent toutes seules, vous cochez les articles et « Servie » clôt la commande.
• Le comptoir peut lire les nouvelles commandes à voix haute.
• Deux iPhone ou deux téléphones Android (Android 13 ou plus récent) s’appairent même sans internet. Un iPhone et un Android ont besoin d’internet pour s’appairer.

BILAN ET CLÔTURE
• Recette totale, espèces et carte, quantités vendues par article.
• Récapitulatif des ventes en PDF pour n’importe quelle période, avec vos coordonnées et, au besoin, le détail de la TVA.
• Plusieurs événements en parallèle, clôture avec archive.
• 9 langues et 33 devises.

VOS DONNÉES VOUS APPARTIENNENT
• Tout reste sur l’appareil. Pas de compte, pas d’analytique, pas de publicité.
• La sauvegarde s’enregistre gratuitement dans un fichier et se restaure à tout moment, y compris sur un nouveau téléphone.
• Une coupure de réseau n’arrête pas la vente.

GRATUIT ET PRO
Gratuit : la caisse complète sur un appareil, 10 additions payées par jour. L’application vous prévient avant d’atteindre la limite. Si vous n’avez pas de réseau à ce moment-là, vous terminez quand même l’addition en cours et recevez une seule fois une réserve de 10 paiements.
Tapkasa Pro (abonnement) : encaissements illimités et appairage d’un second appareil. Un seul abonnement suffit pour le stand, le comptoir se connecte gratuitement. Les nouveaux abonnés profitent de 14 jours d’essai gratuit. Facturé via ${store}, résiliable à tout moment dans les réglages de votre compte.

CE QUE TAPKASA N’EST PAS
• Elle ne traite pas les paiements et n’est pas un terminal de paiement.
• Ce n’est pas un logiciel de caisse certifié (NF525). Utilisez-la là où la réglementation le permet : associations, kermesses, ventes caritatives, suivi interne.
• Pas de gestion de stock ni de comptabilité.

${LINKS}`,
};
