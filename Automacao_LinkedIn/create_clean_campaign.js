const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const PAGE_ID = '102441765221079';

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
  console.log('--- Criando Nova Campanha para o Condomínio Village Provence ---');

  // 1. Criar Campanha
  const campaignParams = {
    name: '[ATIVO] Village Provence - Residência R$1.46M - Vídeo Alcides',
    objective: 'OUTCOME_ENGAGEMENT',
    status: 'ACTIVE',
    special_ad_categories: [],
    is_adset_budget_sharing_enabled: false
  };

  const campaignData = await apiPost(`${AD_ACCOUNT_ID}/campaigns`, campaignParams);
  if (campaignData.error) {
    throw new Error(`Erro ao criar Campanha: ${JSON.stringify(campaignData.error)}`);
  }

  const campaignId = campaignData.id;
  console.log('Campanha Criada com ID:', campaignId);

  // 2. Definir Targeting
  const targeting = {
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
    publisher_platforms: ['facebook', 'instagram'],
    targeting_automation: {
      advantage_audience: 0
    }
  };

  // 3. Criar Ad Set (Conjunto de Anúncios)
  const adsetParams = {
    name: 'SJRP - Village Provence - Alto Padrão',
    campaign_id: campaignId,
    status: 'ACTIVE',
    daily_budget: 2000, // R$ 20.00 por dia (em centavos de real)
    billing_event: 'IMPRESSIONS',
    optimization_goal: 'CONVERSATIONS',
    destination_type: 'WHATSAPP',
    bid_strategy: 'LOWEST_COST_WITHOUT_CAP', // Força menor custo no Ad Set
    targeting: targeting,
    promoted_object: {
      page_id: PAGE_ID,
      whats_app_business_phone_number_id: '136466944934245'
    }
  };

  const adsetData = await apiPost(`${AD_ACCOUNT_ID}/adsets`, adsetParams);
  if (adsetData.error) {
    throw new Error(`Erro ao criar Ad Set: ${JSON.stringify(adsetData.error)}`);
  }

  console.log('Ad Set Criado com ID:', adsetData.id);
  console.log('\n--- Campanha e Ad Set Criados e Configurados com Sucesso! ---');
}

main().catch(err => console.error(err));
