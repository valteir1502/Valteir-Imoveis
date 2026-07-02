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
  console.log('--- Verificando Criativo 1867337303916386 ---');
  const creative = await api('1867337303916386', {
    fields: 'name,title,body,object_story_id,object_id,instagram_actor_id,thumbnail_url'
  });
  console.log('Criativo:', JSON.stringify(creative, null, 2));
}

main();
