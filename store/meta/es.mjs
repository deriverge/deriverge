// Španělština (es-ES v App Store i v Google Play; Play ji dosadí i pro Latinskou Ameriku).
const LINKS = `Términos de uso: https://www.deriverge.com/tapkasa/terms.html
Política de privacidad: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'App Store', gp: 'Google Play' },
  as: {
    locale: 'es-ES',
    name: 'Tapkasa: TPV para puestos',
    subtitle: 'Caja para mercadillos y ferias',
    keywords: 'registradora,mercadillo,navideño,feria,fiestas,barra,caseta,cobrar,cambio,pedidos,vasos,depósito',
  },
  play: {
    locale: 'es-ES',
    title: 'Tapkasa: TPV para puestos',
    shortXmas: 'Caja para mercadillos navideños y ferias: depósitos, pedidos, sin internet.',
    shortYear: 'Caja para puestos, ferias y barras: depósitos de vasos, pedidos, sin internet.',
  },
  promoXmas: '¿Mercadillo navideño, feria o barra del AMPA? Escriba el menú y cobre sin registro y sin internet. Depósito de vasos con un toque, pedidos numerados en un segundo móvil.',
  promoYear: '¿Mercadillo, feria o barra de fiestas? Escriba el menú y cobre sin registro y sin internet. Depósito de vasos con un toque, pedidos numerados en un segundo móvil.',
  wn108: `• Depósitos: el depósito de un vaso o una taza es un artículo más y se devuelve con un toque. El resumen muestra por separado los depósitos cobrados y los devueltos.
• Límite sin sorpresas: la versión gratuita avisa con tiempo antes del límite diario.
• ¿Sin cobertura en el puesto? Puede terminar la cuenta abierta y recibe una sola vez una reserva de 10 pagos.`,
  wn109: `Correcciones y ajustes para la temporada de mercadillos.

Nuevo desde la 1.0.8:
• Depósitos: el depósito de un vaso o una taza es un artículo más y se devuelve con un toque.
• La versión gratuita avisa con tiempo antes del límite diario.
• ¿Sin cobertura en el puesto? Puede terminar la cuenta abierta y recibe una sola vez una reserva de 10 pagos.`,
  desc: (store) => `La caja para puestos, mercadillos navideños, ferias, barras y fiestas de asociaciones. Escriba su menú y empiece a cobrar en dos minutos: sin registro, sin cuenta y sin internet.

Tapkasa calcula y anota sus ventas, pero no procesa pagos. Por eso no bloquea ni verifica nada y no cobra comisiones por los pagos. El efectivo va a su caja y la tarjeta pasa por su propio datáfono.

Un segundo móvil muestra los pedidos numerados y los lee en voz alta. El depósito de vasos y tazas se anota con un toque. Gratis: 10 pagos al día. Para todo un mercado, pruebe Tapkasa Pro gratis durante 14 días.

UNA VENTA EN TRES TOQUES
• Cada artículo es una tarjeta de color. El equipo la reconoce antes de leer el nombre.
• Un toque añade el artículo a la cuenta; mantener pulsado quita una unidad.
• «+ Otro importe» para lo que no está en el menú.
• ¿Se ha equivocado? Un toque deshace la última cuenta.

EFECTIVO Y TARJETA
• En efectivo, teclee lo que entrega el cliente y Tapkasa muestra el cambio.
• Con tarjeta, cobra en su propio datáfono y solo confirma el importe.

DEPÓSITOS
• El depósito de un vaso reutilizable o de una taza es una tarjeta como las demás; la devolución es una tarjeta con precio negativo.
• La devolución se descuenta de la cuenta. Una cuenta solo con devoluciones no cuenta para el límite diario ni entra en la cola de pedidos.
• El resumen muestra por separado los depósitos cobrados y los devueltos a clientes.

PEDIDOS Y BARRA
• Cada cuenta pagada se convierte en un pedido numerado.
• Un segundo móvil o una tableta pasa al modo Barra: los pedidos aparecen solos, se marcan los artículos y «Entregado» cierra el pedido.
• La barra puede leer los pedidos nuevos en voz alta.
• Dos iPhone o dos móviles Android (Android 13 o posterior) se enlazan también sin internet. Un iPhone y un Android necesitan internet para enlazarse.

RESUMEN Y CIERRE
• Ingresos totales, efectivo y tarjeta, unidades vendidas por artículo.
• Resumen de ventas en PDF de cualquier periodo, con sus datos y, si procede, el desglose del IVA.
• Varios eventos a la vez; el cierre guarda el evento en el archivo.
• 9 idiomas y 33 monedas.

SUS DATOS SON SUYOS
• Todo se queda en el dispositivo. Sin cuentas, sin analítica, sin publicidad.
• La copia de seguridad se guarda gratis en un archivo y se restaura cuando quiera, también en un móvil nuevo.
• Si se cae la cobertura, sigue vendiendo.

GRATIS Y PRO
Gratis: la caja completa en un dispositivo, 10 cuentas pagadas al día. La app avisa con tiempo antes de llegar al límite. Si en ese momento no tiene cobertura, puede terminar la cuenta abierta y recibe una sola vez una reserva de 10 pagos.
Tapkasa Pro (suscripción): cobros ilimitados y enlace con un segundo dispositivo. Basta una suscripción por puesto; la barra se conecta gratis. Los nuevos suscriptores tienen 14 días de prueba gratis. Se factura a través de ${store} y se cancela cuando quiera en los ajustes de su cuenta.

LO QUE TAPKASA NO ES
• No procesa pagos ni es un datáfono.
• No es un sistema de facturación certificado (Verifactu, TicketBAI). Úsela donde la normativa lo permita: asociaciones, fiestas escolares y benéficas, registro interno.
• No lleva inventario ni contabilidad.

${LINKS}`,
};
