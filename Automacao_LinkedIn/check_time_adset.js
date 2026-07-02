const token = require('./token.json').token;
const ADSET_ID = '120245174402130720'; // Ad Set do Edificio Time

async function main() {
  console.log(`--- Buscando detalhes do Ad Set funcional ${ADSET_ID} ---`);
  const url = `https://graph.facebook.com/v17.0/${ADSET_ID}?fields=name,billing_event,optimization_goal,bid_strategy,bid_amount,destination_type,promoted_object&access_token=${token}`;
  const res = await fetch(url);
  const data = await res.json();
  console.log('Detalhes do Ad Set:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
