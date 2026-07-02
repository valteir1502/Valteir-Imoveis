const token = require('./token.json').token;
const ADSET_ID = '120245174402130720'; // Ad Set do Edificio Time

async function main() {
  console.log(`--- Buscando anúncios associados ao Ad Set ${ADSET_ID} ---`);
  
  // Pegar os anúncios do Ad Set
  const adsUrl = `https://graph.facebook.com/v17.0/${ADSET_ID}/ads?fields=name,creative{id,name,object_story_spec,video_id,image_hash,body,title}&access_token=${token}`;
  const adsRes = await fetch(adsUrl);
  const adsData = await adsRes.json();
  
  console.log('Anúncios Encontrados:', JSON.stringify(adsData, null, 2));
}

main().catch(err => console.error(err));
