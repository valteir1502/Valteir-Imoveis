const token = require('./token.json').token;

async function api(path, params = {}) {
  const query = new URLSearchParams({
    access_token: token,
    ...params
  }).toString();
  const url = `https://graph.facebook.com/v17.0/${path}?${query}`;
  const res = await fetch(url);
  const data = await res.json();
  if (data.error) {
    throw new Error(`Erro na API (${path}): ${JSON.stringify(data.error)}`);
  }
  return data;
}

async function main() {
  console.log('=== CAMPANHAS ATIVAS NO META ADS ===\n');
  try {
    const accountsData = await api('me/adaccounts', { fields: 'name,id' });
    
    for (const acc of accountsData.data) {
      const campaigns = await api(`${acc.id}/campaigns`, {
        fields: 'name,id,status,objective',
        effective_status: '["ACTIVE"]'
      });

      if (campaigns.data && campaigns.data.length > 0) {
        console.log(`CONTA: ${acc.name} (${acc.id})`);
        console.log(`--------------------------------------------------`);
        
        for (const camp of campaigns.data) {
          console.log(`CAMPANHA ATIVA: ${camp.name} (ID: ${camp.id}) - Objetivo: ${camp.objective}`);
          
          const adSets = await api(`${camp.id}/adsets`, {
            fields: 'name,id,status,targeting,daily_budget,lifetime_budget',
            effective_status: '["ACTIVE"]'
          });

          if (adSets.data) {
            for (const adset of adSets.data) {
              console.log(`  └─ ADSET ATIVO: ${adset.name} (ID: ${adset.id})`);
              console.log(`     Orçamento: ${adset.daily_budget ? 'R$ ' + (adset.daily_budget/100).toFixed(2) + '/dia' : 'Vitalício: ' + adset.lifetime_budget}`);
              console.log(`     Geolocalização e Segmentação:`, JSON.stringify(adset.targeting.geo_locations || adset.targeting, null, 2));

              const ads = await api(`${adset.id}/ads`, {
                fields: 'name,id,status,creative{name,id,body,title}',
                effective_status: '["ACTIVE"]'
              });

              if (ads.data) {
                for (const ad of ads.data) {
                  console.log(`        └─ ANÚNCIO ATIVO: ${ad.name} (ID: ${ad.id})`);
                  if (ad.creative) {
                    console.log(`           Título: "${ad.creative.title || 'Sem título'}"`);
                    console.log(`           Texto: "${ad.creative.body ? ad.creative.body.substring(0, 150) + '...' : 'Sem texto'}"`);
                  }
                }
              }
            }
          }
          console.log('');
        }
        console.log('==================================================\n');
      }
    }
  } catch (err) {
    console.error('Erro:', err.message);
  }
}

main();
