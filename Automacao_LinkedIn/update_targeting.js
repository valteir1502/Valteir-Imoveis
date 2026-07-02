const token = require('./token.json').token;

const ADSET_PROVENCE_ID = '120247080465980720'; // Ad Set da campanha Village Provence ativa
const ADSET_TIME_ID = '120245174402130720';     // Ad Set da campanha Edifício Time ativa

// Segmentação para o Village Provence (Venda R$ 1.46M)
// Foco em pessoas buscando ativamente imóveis na região E qualificadas financeiramente
const targetingProvence = {
  age_min: 30,
  age_max: 65,
  geo_locations: {
    cities: [
      {
        country: 'BR',
        distance_unit: 'kilometer',
        key: '269661',
        radius: 40 // Raio de 40km para cobrir Rio Preto e cidades vizinhas
      }
    ],
    location_types: ['home', 'recent']
  },
  // AND condição:
  // Grupo 1: Ativamente buscando imóveis (Portais imobiliários e categorias residenciais)
  // AND
  // Grupo 2: Alto poder aquisitivo ou luxo
  flexible_spec: [
    {
      interests: [
        { id: '6788101567252', name: 'Property listings and web portals' }, // Substituto oficial do ZAP e Imovelweb
        { id: '6003077334693', name: 'Condomínio fechado (imóveis)' },
        { id: '6003693537583', name: 'Propriedade de imóveis (imóveis)' },
        { id: '6849417269780', name: 'Imóveis residenciais (imóveis)' }
      ]
    },
    {
      interests: [
        { id: '6007828099136', name: 'Bens de luxo (varejo)' },
        { id: '6003375842396', name: 'Luxo' }
      ],
      behaviors: [
        { id: '6046096201583', name: 'People who prefer high-value goods in Brazil' }
      ]
    }
  ],
  targeting_automation: {
    advantage_audience: 0
  }
};

// Segmentação para o Edifício Time (Locação)
// Foco em pessoas buscando apartamentos e condomínios na região de Rio Preto
const targetingTime = {
  age_min: 25,
  age_max: 55,
  geo_locations: {
    cities: [
      {
        country: 'BR',
        distance_unit: 'kilometer',
        key: '269661',
        radius: 40 // Ampliado para 40km
      }
    ],
    location_types: ['home', 'recent']
  },
  flexible_spec: [
    {
      interests: [
        { id: '6788101567252', name: 'Property listings and web portals' }, // Substituto do ZAP e Imovelweb
        { id: '6003435139283', name: 'Condomínio (imóveis)' },
        { id: '6003077334693', name: 'Condomínio fechado (imóveis)' },
        { id: '6003693537583', name: 'Propriedade de imóveis (imóveis)' }
      ]
    }
  ],
  targeting_automation: {
    advantage_audience: 0
  }
};

async function updateAdSet(adSetId, targeting, name) {
  console.log(`--- Atualizando segmentação do Ad Set: ${name} (ID: ${adSetId}) ---`);
  
  const body = new URLSearchParams();
  body.append('access_token', token);
  body.append('targeting', JSON.stringify(targeting));

  const url = `https://graph.facebook.com/v17.0/${adSetId}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  const data = await res.json();
  if (data.error) {
    console.error(`Erro ao atualizar ${name}:`, JSON.stringify(data.error, null, 2));
  } else {
    console.log(`✓ Ad Set ${name} atualizado com sucesso! Resultado:`, data);
  }
}

async function main() {
  await updateAdSet(ADSET_PROVENCE_ID, targetingProvence, 'Village Provence');
  console.log('\n');
  await updateAdSet(ADSET_TIME_ID, targetingTime, 'Edifício Time');
}

main().catch(err => console.error(err));
