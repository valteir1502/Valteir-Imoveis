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
  console.log('--- Verificando Ad Set 120245591905240720 ---');
  const adset = await api('120245591905240720', {
    fields: 'name,status,effective_status,targeting,campaign{name,status}'
  });
  console.log('Ad Set:', JSON.stringify(adset, null, 2));

  console.log('\n--- Verificando Anúncio 120245591905220720 ---');
  const ad = await api('120245591905220720', {
    fields: 'name,status,effective_status,creative'
  });
  console.log('Anúncio:', JSON.stringify(ad, null, 2));
}

main();
