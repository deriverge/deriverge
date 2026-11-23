# Portuguese texts of the Tapkasa landing pages, European Portuguese like the app itself (telemóvel, ecrã).
# Facts follow tapkasa/README.md and the app texts (version 1.0.8). No prices, Tapkasa is not certified invoicing
# software and issues no invoices. No long dashes.

T = dict(
    html_lang='pt-PT', hreflang='pt', og_locale='pt_PT', name='Português', currency='EUR',
    gp_badge='badge-googleplay-en.png', as_alt='Descarregar na App Store', gp_alt='Disponível no Google Play',
    brand_sub='A caixa de bolso', menu='Idioma',
    try_btn='Experimentar no navegador',
    qr_alt='Código QR para descarregar a app Tapkasa',
    qr_text='Aponte a câmara do telemóvel para o código e descarregue a Tapkasa.',
    note='Grátis até 10 contas pagas por dia. Sem registo.',
    sticky='A caixa de bolso',
    ld_desc='Uma caixa simples no telemóvel para bancas de feira, mercados de Natal, festas da escola e '
            'associações. Calcula o troco, numera os pedidos, gere cauções de copos e funciona sem internet. Os '
            'dados ficam no dispositivo.',
    offer='Grátis até 10 contas pagas por dia. A Tapkasa Pro é uma subscrição na app (mensal ou anual).',
    h_how='Como funciona',
    how=[
        ('Escreva o menu', 'Cada artigo tem nome, preço e cor. São uns minutos em casa, ou comece pelo menu de '
                           'exemplo.'),
        ('Toque nos cartões', 'Um toque junta uma unidade, um toque longo retira-a. Em baixo vê sempre quanto o '
                              'cliente tem de pagar.'),
        ('Dinheiro ou cartão', 'Em dinheiro, a Tapkasa calcula o troco. O cartão passa no seu próprio terminal e na '
                               'Tapkasa apenas assinala o pagamento.'),
    ],
    h_feat='O que a Tapkasa faz',
    feats=[
        ('Troco sem contas de cabeça', 'Toca na nota que recebeu e vê quanto devolver.'),
        ('Fila de pedidos numerados', 'Cada conta paga recebe um número e espera na fila até a marcar como '
                                      'entregue.'),
        ('Caixa e balcão em dois telemóveis', 'O segundo dispositivo mostra os pedidos e pode lê-los em voz alta. A '
                                              'ligação entre dispositivos faz parte da Tapkasa Pro.'),
        ('Funciona sem rede', 'Tudo corre no telemóvel. Dois iPhones ou dois telemóveis Android ligam-se mesmo sem '
                              'internet.'),
        ('Cauções', 'A caução do copo ou da caneca e a sua devolução são artigos à parte, separados das vendas no '
                    'resumo.'),
        ('Os dados ficam consigo', 'Sem conta e sem nuvem. Guarda uma cópia de segurança num ficheiro, onde '
                                   'quiser.'),
    ],
    h_shots='Como é a Tapkasa',
    shot_alts=['Ecrã de venda da Tapkasa: cartões coloridos dos artigos com os preços e o valor a pagar',
               'Fila de pedidos numerados no segundo telemóvel',
               'Resumo de vendas com o detalhe do IVA'],
    h_not='O que a Tapkasa não é',
    nots=[
        'Não é um programa de faturação certificado pela Autoridade Tributária e não comunica nada às Finanças. O '
        'resumo de vendas não é uma fatura nem um talão.',
        'Não processa pagamentos com cartão. O cartão passa no seu próprio terminal e a Tapkasa só regista a venda.',
        'Não imprime talões nem senhas.',
    ],
    not_p='Serve onde não há obrigação de usar um programa de faturação certificado, ou como ajuda ao lado dele. '
          'Confirme as suas obrigações com o seu contabilista.',
    h_price='Quanto custa',
    price=[
        'Grátis: todo o menu, os resumos, as cauções e a cópia de segurança num dispositivo, com 10 contas pagas por '
        'dia. Uma conta que só devolve uma caução não conta para o limite.',
        'Tapkasa Pro: contas ilimitadas e ligação entre a caixa e o balcão. É uma subscrição mensal ou anual através '
        'da App Store ou do Google Play, com 14 dias de experiência grátis para novos subscritores. O preço na sua '
        'moeda aparece na app antes da compra e pode cancelar quando quiser nas definições da loja.',
        'Para uma banca basta uma subscrição: o segundo telemóvel liga-se gratuitamente ao dispositivo com a '
        'Tapkasa Pro.',
    ],
    h_faq='Perguntas frequentes',
    faq=[
        ('A Tapkasa é grátis?',
         'Sim, até 10 contas pagas por dia num dispositivo. As contas ilimitadas e a ligação de dois dispositivos '
         'pedem a subscrição Tapkasa Pro, que os novos subscritores podem experimentar grátis durante 14 dias.'),
        ('É uma caixa registadora certificada?',
         'Não. A Tapkasa conta e regista as vendas, mas não é um programa de faturação certificado, não comunica '
         'dados às Finanças e não emite faturas nem talões.'),
        ('Onde ficam os meus dados?',
         'Apenas no seu dispositivo. A Tapkasa não tem contas nem nuvem. Pode guardar uma cópia de segurança num '
         'ficheiro e carregá-la num telemóvel novo.'),
        ('Em que línguas e moedas funciona?',
         'Em nove línguas (português, inglês, espanhol, francês, alemão, italiano, polaco, checo e eslovaco) e em '
         '33 moedas, incluindo o euro e o real.'),
    ],
    cta_h='Experimente a Tapkasa antes do evento',
    h_more='Mais guias',
    f_support='Apoio', f_privacy='Privacidade', f_terms='Termos', f_app='Abrir a Tapkasa no navegador',
    f_langs='Idiomas', f_operator='Operador',
    pages=dict(
        stall=dict(
            path='pt/', card='Caixa para banca de feira',
            title='Caixa para banca de feira no telemóvel, sem rede | Tapkasa',
            desc='Uma caixa simples para a sua banca, no telemóvel: cartões coloridos, troco calculado, pedidos '
                 'numerados num segundo telemóvel e cauções de copos. Funciona sem internet e sem registo.',
            h1='A caixa da sua banca cabe no bolso',
            eyebrow='Para iPhone, Android e navegador',
            lede='Escreve o menu, toca nos cartões coloridos e a Tapkasa faz as contas: quanto cobrar, quanto dar '
                 'de troco e quanto vendeu hoje. Sem registo, sem equipamento e sem internet.',
            sections=[
                ('Como é na banca',
                 '<p>Um cliente pede duas bifanas e uma sopa. Toca duas vezes na bifana, uma vez na sopa e o valor '
                 'aparece em baixo. Ele entrega uma nota de 20, toca em 20 e a Tapkasa mostra o troco. São uns '
                 'segundos e ninguém faz contas de cabeça, nem quem está na banca pela primeira vez.</p>'),
                ('Dois telemóveis: caixa e balcão',
                 '<p>Quando se forma fila, um telemóvel cobra e o outro mostra os pedidos com o número. No balcão '
                 'assinala o que está pronto e os pedidos novos podem ser lidos em voz alta, sem olhar para o ecrã '
                 'com as mãos ocupadas. Dois iPhones ou dois telemóveis Android ligam-se diretamente, sem internet. '
                 'Um iPhone com um Android precisa de ligação.</p>'),
                ('A caução do copo',
                 '<p>O botão «+ Adicionar caução» cria dois artigos: Caução e Devolução caução. O copo devolvido é '
                 'descontado da conta e no resumo as cauções recebidas e devolvidas aparecem à parte, sem se '
                 'misturarem com as vendas.</p>'),
                ('À noite sabe quanto fez',
                 '<p>O resumo mostra o total vendido, dinheiro e cartão em separado e as unidades vendidas de cada '
                 'artigo. Pode guardar o resumo de vendas em PDF, por exemplo para o contabilista.</p>'),
            ],
            faq=[
                ('É preciso ligação à internet?',
                 'Não. A venda, os resumos e a cópia de segurança funcionam no telemóvel. A internet só é precisa '
                 'para descarregar a app, comprar a Tapkasa Pro e ligar um iPhone a um Android.'),
                ('Um ajudante ou voluntário consegue usá-la?',
                 'Sim. Uma venda é um toque num cartão colorido e a escolha Dinheiro ou Cartão. Um artigo '
                 'adicionado por engano sai com um toque longo.'),
            ],
        ),
        xmas=dict(
            path='pt/mercado-de-natal/', card='Caixa para mercado de Natal',
            title='Caixa para mercado de Natal: caução do copo e troco | Tapkasa',
            desc='Uma caixa no telemóvel para o mercado de Natal: cada artigo com um toque, caução do copo ou da '
                 'caneca, troco calculado. Funciona sem rede e sem registo, 10 contas por dia grátis.',
            h1='Uma caixa para o mercado de Natal: bebidas quentes, doces e caução do copo',
            eyebrow='Mercados de Natal e feiras de artesanato',
            lede='A praça está cheia, a rede não aguenta e há fila à frente da banca. A Tapkasa funciona no '
                 'telemóvel sem internet, calcula o troco e controla as cauções dos copos. Fica pronta em poucos '
                 'minutos.',
            sections=[
                ('A caução do copo sem confusões',
                 '<p>No Menu toque em «+ Adicionar caução» e escreva o valor, por exemplo 1 €. A Tapkasa cria dois '
                 'artigos: Caução e Devolução caução. Com a bebida junta a caução, quando o copo volta toca na '
                 'devolução e o valor é descontado da conta. Se o cliente só devolve o copo, a Tapkasa mostra '
                 'quanto lhe entregar.</p>'
                 '<p>No resumo, as cauções recebidas e devolvidas ficam à parte. À noite sabe quantos copos ainda '
                 'andam fora e qual foi a venda real.</p>'),
                ('Quando a rede cai na praça',
                 '<p>A venda, o troco e o resumo correm no próprio telemóvel. A Tapkasa não inicia sessão em lado '
                 'nenhum nem verifica nada online: uma rede saturada ou os dados esgotados não o param em plena '
                 'hora de ponta.</p>'),
                ('Artesanato e preços avulsos',
                 '<p>Guarde os artigos habituais como cartões coloridos. Para uma peça única que não está no menu, '
                 'toque em «+ Outro valor», escreva o preço e continue. No fim do dia o resumo mostra o que se '
                 'vendeu e quantas unidades.</p>'),
                ('Dicas para os dias frios',
                 '<ul><li>Arredonde os preços para dar o troco com facilidade: 3, 4, 5 €.</li>'
                 '<li>Prepare o menu em casa e ponha em cima o que mais se vende.</li>'
                 '<li>Leve uma powerbank. O ecrã fica ligado durante a venda e com o frio a bateria dura '
                 'menos.</li>'
                 '<li>Guarde uma cópia de segurança num ficheiro antes do primeiro dia de mercado.</li></ul>'),
            ],
            faq=[
                ('A devolução da caução conta para o limite gratuito diário?',
                 'Não. Uma conta que só devolve uma caução não conta para as 10 contas pagas por dia.'),
                ('A versão gratuita chega para um mercado de Natal?',
                 'Para uma banca pequena com poucas vendas por dia, sim. Para um mercado com muito movimento '
                 'compensa a Tapkasa Pro: os novos subscritores têm 14 dias grátis, o que cobre dois fins de '
                 'semana. A Tapkasa avisa com antecedência quando o limite se aproxima.'),
            ],
        ),
        club=dict(
            path='pt/festa-da-escola/', card='Caixa para festa da escola e associação',
            title='Caixa para festa da escola, arraial e associação | Tapkasa',
            desc='Uma caixa no telemóvel para a festa da escola, o arraial ou o bar da associação: os voluntários '
                 'tocam nos artigos, o troco é calculado e o tesoureiro recebe o total em PDF. Sem registo.',
            h1='Uma caixa para a festa da escola e o bar da associação',
            eyebrow='Festas da escola, arraiais, coletividades, quermesses',
            lede='Os voluntários revezam-se no bar e à noite o tesoureiro quer saber quanto entrou. A Tapkasa '
                 'guarda os preços, calcula o troco e soma a receita num telemóvel. Sem registo e sem formação.',
            sections=[
                ('Qualquer voluntário sabe usar',
                 '<p>Os artigos são cartões grandes e coloridos: ninguém procura numa lista nem faz contas de '
                 'cabeça. Toca-se no que o cliente pede, escolhe-se Dinheiro ou Cartão e, em dinheiro, o ecrã '
                 'mostra o troco. Para trocar de turno basta passar o telemóvel.</p>'),
                ('À noite, um total exato para o tesoureiro',
                 '<p>O resumo mostra o total vendido, dinheiro e cartão em separado e quantas unidades se venderam. '
                 'Envie-o em PDF ao tesoureiro ou à direção. Depois da festa escolha «Fechar evento»: a receita '
                 'passa para o arquivo e da próxima vez começa do zero.</p>'),
                ('Sem conta, sem verificação, sem comissões',
                 '<p>A Tapkasa não pede registo, NIF nem conta bancária e não fica com nada da receita. O dinheiro '
                 'vai para a vossa caixa. Os dados ficam no telemóvel usado no bar.</p>'),
                ('Festas maiores: bar e cozinha separados',
                 '<p>Num arraial ou numa festa da aldeia, um telemóvel pode cobrar no bar enquanto outro mostra os '
                 'pedidos na cozinha. Basta uma subscrição Tapkasa Pro, com 14 dias de experiência grátis para '
                 'novos subscritores.</p>'),
            ],
            faq=[
                ('A versão gratuita chega para a festa da escola?',
                 'Para uma festa pequena, sim: 10 contas pagas por dia são grátis. Se esperam mais gente, ativem '
                 'antes a Tapkasa Pro; os novos subscritores têm 14 dias de experiência grátis.'),
                ('A associação tem de se registar?',
                 'Não. Descarrega-se a Tapkasa e abre-se. Não se cria nenhuma conta e nada é verificado.'),
            ],
        ),
    ),
)
