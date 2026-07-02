const token = require('./token.json').token;

async function api(path, params = {}) {
  const query = new URLSearchParams({
    access_token: token,
    ...params
  }).toString();
  const url = `https://graph.facebook.com/v17.0/${path}?${query}`;
  const res = await fetch(url);
  return res.json();
}

async function main() {
  console.log('--- Verificando Anúncio do Edifício Time 120245174402110720 ---');
  const ad = await api('120245174402110720', {
    fields: 'creative'
  });
  console.log('Criativo ID do Time Garetti:', ad.creative.id);

  console.log('\n--- Verificando Estrutura Interna do Criativo ---');
  const creative = await api(ad.creative.id, {
    fields: 'name,title,body,object_story_spec,call_to_action_type,link_url,image_hash,asset_feed_spec'
  });
  console.log('Criativo Completo:', JSON.stringify(creative, null, 2));
}

main();
