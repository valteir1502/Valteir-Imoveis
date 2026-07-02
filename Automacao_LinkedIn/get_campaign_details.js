const token = require('./token.json').token;
const CAMPAIGN_ID = '120241780606290103'; // ID da Campanha Damha 5

async function main() {
  console.log(`--- Buscando detalhes da campanha ${CAMPAIGN_ID} ---`);
  const url = `https://graph.facebook.com/v17.0/${CAMPAIGN_ID}?fields=name,objective,special_ad_categories,status&access_token=${token}`;
  const res = await fetch(url);
  const data = await res.json();
  console.log('Detalhes da Campanha:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
