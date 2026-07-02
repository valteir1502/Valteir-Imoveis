const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const AD_SET_ID = '120247080465980720';
const PAGE_ID = '102441765221079';
const VIDEO_ID = '2261589607711329';

const messageText = `🏛️ Conforto, tecnologia e sofisticação no Condomínio Village Provence!

Apresento esta linda casa térrea projetada para oferecer a melhor experiência de moradia para você e sua família na Zona Sul de São José do Rio Preto - SP.

✨ Detalhes da Residência:
📐 264m² de terreno | 173m² de construção primorosa
🛏️ 3 Suítes climatizadas (suíte master com um closet deslumbrante em vidro reflecta)
🖥️ Escritório privativo completo com móveis planejados
🍽️ Espaço gourmet amplo com ilha central e churrasqueira (equipado com depurador, forno, micro-ondas e cooktop)
🏊 Piscina aquecida e revestida em cerâmica
🤖 Casa totalmente integrada com automação inteligente (Alexa)
☀️ Climatização completa em todos os ambientes

📍 Condomínio com infraestrutura completa de lazer e segurança 24h (piscinas, campo de futebol, quadras, academia e salão de festas).

💰 Valor de Venda: R$ 1.460.000,00
(Condomínio: R$ 358,18 | IPTU: R$ 124,11)

💬 Venha conhecer de perto todos os detalhes deste imóvel exclusivo! Clique no botão abaixo para agendar sua visita pelo WhatsApp.

Valteir de Oliveira | CRECI 214072-F`;

async function apiPost(path, params = {}) {
  const body = new URLSearchParams();
  body.append('access_token', token);
  for (const [key, val] of Object.entries(params)) {
    if (typeof val === 'object') {
      body.append(key, JSON.stringify(val));
    } else {
      body.append(key, val);
    }
  }

  const url = `https://graph.facebook.com/v17.0/${path}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  return res.json();
}

async function main() {
  console.log('--- Criando Ad Creative (Vídeo) ---');

  const creativeParams = {
    name: 'Criativo Vídeo - Village Provence Alcides',
    object_story_spec: {
      page_id: PAGE_ID,
      instagram_user_id: '17841401831627959',
      video_data: {
        video_id: VIDEO_ID,
        message: messageText,
        title: 'Converse conosco',
        image_hash: '109fcf25dc93322fde089fe0bdf15dbb',
        call_to_action: {
          type: 'WHATSAPP_MESSAGE',
          value: {
            app_destination: 'WHATSAPP',
            link: 'https://api.whatsapp.com/send'
          }
        }
      }
    }
  };

  const creativeData = await apiPost(`${AD_ACCOUNT_ID}/adcreatives`, creativeParams);
  if (creativeData.error) {
    console.error('Erro ao criar Criativo:', JSON.stringify(creativeData.error));
    // Tentar sem Call To Action se der erro de app em desenvolvimento
    if (creativeData.error.error_subcode === 1885183) {
      console.log('Tentando criar criativo simplificado sem Call To Action de mensagens...');
      const fallbackParams = {
        name: 'Criativo Vídeo - Village Provence (Simplificado)',
        object_story_spec: {
          page_id: PAGE_ID,
          video_data: {
            video_id: VIDEO_ID,
            message: messageText,
            image_hash: '109fcf25dc93322fde089fe0bdf15dbb'
          }
        }
      };
      const fallbackData = await apiPost(`${AD_ACCOUNT_ID}/adcreatives`, fallbackParams);
      if (fallbackData.error) {
        throw new Error(`Erro no criativo fallback: ${JSON.stringify(fallbackData.error)}`);
      }
      await createAd(fallbackData.id);
    } else {
      throw new Error(`Erro inesperado no criativo: ${JSON.stringify(creativeData.error)}`);
    }
  } else {
    console.log('Criativo Criado com ID:', creativeData.id);
    await createAd(creativeData.id);
  }
}

async function createAd(creativeId) {
  console.log('--- Criando Anúncio (Ad) ---');
  const adParams = {
    name: 'Anúncio de Vídeo - Casa R$1.46M',
    adset_id: AD_SET_ID,
    creative: {
      creative_id: creativeId
    },
    status: 'ACTIVE'
  };

  const adData = await apiPost(`${AD_ACCOUNT_ID}/ads`, adParams);
  if (adData.error) {
    throw new Error(`Erro ao criar Anúncio: ${JSON.stringify(adData.error)}`);
  }

  console.log('Anúncio Criado e Ativado com ID:', adData.id);
}

main().catch(err => console.error(err));
