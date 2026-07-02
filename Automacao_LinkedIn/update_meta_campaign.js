const token = require('./token.json').token;

async function updateNode(id, fields = {}) {
  const body = new URLSearchParams();
  body.append('access_token', token);
  for (const [key, val] of Object.entries(fields)) {
    if (typeof val === 'object') {
      body.append(key, JSON.stringify(val));
    } else {
      body.append(key, val);
    }
  }

  const url = `https://graph.facebook.com/v17.0/${id}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: body.toString()
  });

  const data = await res.json();
  if (data.error) {
    throw new Error(`Erro ao atualizar nó ${id}: ${JSON.stringify(data.error)}`);
  }
  return data;
}

async function main() {
  console.log('--- Iniciando Atualização do Meta Ads ---');
  
  const campaignId = '120245591905230720';
  const adSetId = '120245591905240720';

  try {
    // 1. Atualizar Nome da Campanha
    console.log(`Atualizando nome da campanha ${campaignId}...`);
    const campaignResult = await updateNode(campaignId, {
      name: '[ATIVO] Damha I - Residência Neoclássica R$8.9M - WhatsApp'
    });
    console.log('Resultado da Campanha:', campaignResult);

    // 2. Definir a Segmentação Técnica do Público de Luxo Local (Sem exclusões devido a restrições da API)
    const newTargeting = {
      age_max: 65,
      age_min: 30,
      genders: [1, 2],
      geo_locations: {
        cities: [
          {
            country: 'BR',
            distance_unit: 'kilometer',
            key: '269661',
            name: 'São José do Rio Prêto',
            radius: 25,
            region: 'São Paulo (state)',
            region_id: '460'
          }
        ],
        location_types: ['home', 'recent']
      },
      flexible_spec: [
        {
          interests: [
            { id: '6003077334693', name: 'Condomínio fechado (imóveis)' },
            { id: '6003375842396', name: 'Luxo' },
            { id: '6003388314512', name: 'Investimento (negócios e finanças)' },
            { id: '6003446239080', name: 'Investimento imobiliário (investimento)' },
            { id: '6003578086487', name: 'Imóveis (indústria)' },
            { id: '6003693537583', name: 'Propriedade de imóveis (imóveis)' },
            { id: '6007828099136', name: 'Bens de luxo (varejo)' }
          ],
          behaviors: [
            { id: '6022788483583', name: 'Frequent international travelers' },
            { id: '6046096201583', name: 'People who prefer high-value goods in Brazil' }
          ]
        }
      ],
      publisher_platforms: ['facebook', 'instagram']
    };

    // 3. Atualizar Ad Set (Nome e Segmentação)
    console.log(`\nAtualizando nome e segmentação do Ad Set ${adSetId}...`);
    const adSetResult = await updateNode(adSetId, {
      name: 'SJRP - Damha I - Alto Padrão & Luxo',
      targeting: newTargeting
    });
    console.log('Resultado do Ad Set:', adSetResult);

    console.log('\n--- Atualização Concluída com Sucesso! ---');

  } catch (err) {
    console.error('\nErro durante a atualização:', err.message);
  }
}

main();
