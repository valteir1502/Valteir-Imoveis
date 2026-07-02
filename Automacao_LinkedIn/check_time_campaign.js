const token = require('./token.json').token;
const ADSET_ID = '120245174402130720';

async function main() {
  console.log(`--- Buscando campanha associada ao Ad Set ${ADSET_ID} ---`);
  
  // Primeiro, pegamos o campaign_id do Ad Set
  const adsetUrl = `https://graph.facebook.com/v17.0/${ADSET_ID}?fields=campaign&access_token=${token}`;
  const adsetRes = await fetch(adsetUrl);
  const adsetData = await adsetRes.json();
  
  const campaignId = adsetData.campaign.id;
  console.log('ID da Campanha associada:', campaignId);

  // Agora inspecionamos a campanha
  const campaignUrl = `https://graph.facebook.com/v17.0/${campaignId}?fields=name,objective,bid_strategy,daily_budget,buying_type,special_ad_categories&access_token=${token}`;
  const campaignRes = await fetch(campaignUrl);
  const campaignData = await campaignRes.json();
  console.log('Detalhes da Campanha:', JSON.stringify(campaignData, null, 2));
}

main().catch(err => console.error(err));
