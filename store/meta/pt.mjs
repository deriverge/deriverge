// Portugalština (pt-PT v App Store i v Google Play; Play ji dosadí i pro Brazílii).
const LINKS = `Termos de utilização: https://www.deriverge.com/tapkasa/terms.html
Política de privacidade: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'da App Store', gp: 'do Google Play' },
  as: {
    locale: 'pt-PT',
    name: 'Tapkasa: caixa para bancas',
    subtitle: 'Mercado de Natal, feira, bar',
    keywords: 'registadora,pos,venda,vendas,feiras,festival,pedidos,troco,caução,copo,quermesse,arraial,tasquinha',
  },
  play: {
    locale: 'pt-PT',
    title: 'Tapkasa: caixa para bancas',
    shortXmas: 'Caixa para mercados de Natal e feiras: cauções, pedidos numerados, sem internet.',
    shortYear: 'Caixa para bancas, feiras e festas: cauções, pedidos numerados, sem internet.',
  },
  promoXmas: 'Mercado de Natal, feira ou banca de vinho quente? Escreva o menu e cobre sem registo e sem internet. Caução com um toque, pedidos numerados num segundo telemóvel.',
  promoYear: 'Mercado, feira ou festa da escola? Escreva o menu e cobre sem registo e sem internet. Caução com um toque, pedidos numerados num segundo telemóvel.',
  wn108: `• Cauções: a caução de um copo ou de uma caneca é um artigo como os outros e devolve-se com um toque. O resumo mostra em separado as cauções cobradas e devolvidas.
• Limite sem surpresas: a versão gratuita avisa com antecedência antes do limite diário.
• Sem rede na banca? Pode terminar a conta aberta e recebe uma única vez uma reserva de 10 pagamentos.`,
  wn109: `Correções e afinações para a época dos mercados.

Novo desde a 1.0.8:
• Cauções: a caução de um copo ou de uma caneca é um artigo como os outros e devolve-se com um toque.
• A versão gratuita avisa com antecedência antes do limite diário.
• Sem rede na banca? Pode terminar a conta aberta e recebe uma única vez uma reserva de 10 pagamentos.`,
  desc: (store) => `A caixa para bancas, mercados de Natal, feiras, bares e festas de associações. Escreva o menu e em dois minutos está a vender: sem registo, sem conta e sem internet.

A Tapkasa faz as contas e regista as vendas, mas não processa pagamentos. Por isso não bloqueia nem verifica nada e não cobra comissões sobre os pagamentos. O dinheiro vai para a sua caixa e o cartão passa pelo seu próprio terminal.

Um segundo telemóvel mostra os pedidos numerados e lê-os em voz alta. A caução de copos e canecas regista-se com um toque. Grátis: 10 pagamentos por dia. Para uma feira inteira, experimente o Tapkasa Pro grátis durante 14 dias.

UMA VENDA EM TRÊS TOQUES
• Cada artigo é um cartão colorido. A equipa reconhece-o antes de ler o nome.
• Um toque junta o artigo à conta, manter premido retira uma unidade.
• «+ Outro valor» para tudo o que não está no menu.
• Enganou-se? Um toque anula a última conta.

DINHEIRO E CARTÃO
• Em dinheiro, escreva o que o cliente entrega e a Tapkasa mostra o troco.
• Com cartão, cobra no seu próprio terminal e apenas confirma o valor.

CAUÇÕES
• A caução de um copo reutilizável ou de uma caneca é um cartão como os outros; a devolução da caução é um cartão com preço negativo.
• A devolução é descontada da conta. Uma conta só com devoluções não conta para o limite diário nem entra na fila de pedidos.
• O resumo mostra em separado as cauções cobradas e as devolvidas a clientes.

PEDIDOS E BALCÃO
• Cada conta paga torna-se um pedido numerado.
• Um segundo telemóvel ou tablet passa ao papel Balcão: os pedidos aparecem sozinhos, marca os artigos e «Entregue» fecha o pedido.
• O balcão pode ler os novos pedidos em voz alta.
• Dois iPhones ou dois telemóveis Android (Android 13 ou mais recente) ligam-se também sem internet. Um iPhone e um Android precisam de internet para se ligarem.

RESUMO E FECHO
• Receita total, dinheiro e cartão, unidades vendidas por artigo.
• Resumo de vendas em PDF de qualquer período, com os seus dados e, se precisar, o resumo do IVA.
• Vários eventos em paralelo, fecho com arquivo.
• 9 idiomas e 33 moedas.

OS SEUS DADOS SÃO SEUS
• Tudo fica no aparelho. Sem contas, sem análises, sem publicidade.
• A cópia de segurança guarda-se gratuitamente num ficheiro e repõe-se quando quiser, também num telemóvel novo.
• Se a rede falhar, continua a vender.

GRÁTIS E PRO
Grátis: a caixa completa num aparelho, 10 contas pagas por dia. A app avisa com antecedência antes do limite. Se nesse momento não tiver rede, pode terminar a conta aberta e recebe uma única vez uma reserva de 10 pagamentos.
Tapkasa Pro (subscrição): vendas ilimitadas e ligação a um segundo aparelho. Basta uma subscrição por banca, o balcão liga-se gratuitamente. Os novos subscritores têm 14 dias de experiência grátis. Faturado através ${store}, cancelável a qualquer momento nas definições da conta.

O QUE A TAPKASA NÃO É
• Não processa pagamentos nem é um terminal de pagamento.
• Não é um programa de faturação certificado pela AT. Use-a onde as regras o permitem: associações, festas escolares e de beneficência, registo interno.
• Não faz gestão de stock nem contabilidade.

${LINKS}`,
};
