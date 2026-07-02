const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const PAGE_ID = '102441765221079';
const INSTAGRAM_USER_ID = '17841401831627959';
const ADSET_ID = '120245591905240720';
const IMAGE_HASH = '89398f975b8114fa5d9660cf37f5c065';

const messageText = `🏛️ Já pensou em morar na Residência Neoclássica mais imponente do Damha I?

Uma verdadeira obra-prima da arquitetura que redefine o conceito de luxo e sofisticação em São José do Rio Preto.

✨ Diferenciais Exclusivos:
📐 800m² de área construída em terreno de 900m²
🛏️ 6 suítes master completas com closet (4 com hidromassagem)
🏊 Piscina com raia de natação integrada à área de lazer
🧖 Sauna úmida e academia privativa
🎬 Cinema particular climatizado
🍷 Adega climatizada premium
🛗 Elevador privativo interno
☀️ Energia fotovoltaica e automação completa

Localização nobre no Parque Residencial Damha I. Avaliação de permutas e propostas à vista.

💬 Quer agendar uma apresentação privativa deste imóvel? Toque no botão abaixo para conversar diretamente comigo no WhatsApp!

Valteir de Oliveira | CRECI 214072-F`;

async function main() {
  console.log('--- Criando Ad Creative para a Mansão Damha I ---');
  
  const objectStorySpec = {
    page_id: PAGE_ID,
    instagram_user_id: INSTAGRAM_USER_ID,
    link_data: {
      call_to_action: {
        type: 'WHATSAPP_MESSAGE',
        value: {
          app_destination: 'WHATSAPP',
          link: 'https://api.whatsapp.com/send'
        }
      },
      image_hash: IMAGE_HASH,
      link: 'https://api.whatsapp.com/send',
      message: messageText,
      name: 'Residência Neoclássica - Damha I',
      caption: 'valteir.com.br'
    }
  };

  const creativeBody = new URLSearchParams();
  creativeBody.append('access_token', token);
  creativeBody.append('name', 'Criativo Mansão Damha I - Imagem Direta');
  creativeBody.append('object_story_spec', JSON.stringify(objectStorySpec));

  const creativeRes = await fetch(`https://graph.facebook.com/v17.0/${AD_ACCOUNT_ID}/adcreatives`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: creativeBody.toString()
  });

  const creativeData = await creativeRes.json();
  if (creativeData.error) {
    throw new Error(`Erro ao criar Criativo: ${JSON.stringify(creativeData.error)}`);
  }

  const creativeId = creativeData.id;
  console.log('Ad Creative criado com ID:', creativeId);

  console.log('\n--- Criando Anúncio (Ad) associado ao Ad Set ---');
  
  const adBody = new URLSearchParams();
  adBody.append('access_token', token);
  adBody.append('name', '[ATIVO] Mansão Neoclássica Damha I R$8.9M');
  adBody.append('adset_id', ADSET_ID);
  adBody.append('creative', JSON.stringify({ creative_id: creativeId }));
  adBody.append('status', 'ACTIVE');

  const adRes = await fetch(`https://graph.facebook.com/v17.0/${AD_ACCOUNT_ID}/ads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: adBody.toString()
  });

  const adData = await adRes.json();
  if (adData.error) {
    throw new Error(`Erro ao criar Anúncio: ${JSON.stringify(adData.error)}`);
  }

  console.log('Anúncio criado com sucesso! ID:', adData.id);
  console.log('--- Processo finalizado com sucesso! ---');
}

main().catch(err => console.error(err));
