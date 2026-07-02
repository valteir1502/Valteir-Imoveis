const token = require('./token.json').token;
const CAMPAIGN_ID = '120245591905230720';

async function main() {
  console.log(`--- Deletando Campanha ${CAMPAIGN_ID} ---`);
  
  const url = `https://graph.facebook.com/v17.0/${CAMPAIGN_ID}?access_token=${token}`;
  const res = await fetch(url, {
    method: 'DELETE'
  });

  const data = await res.json();
  console.log('Resultado da Exclusão:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
