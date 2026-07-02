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
  console.log('--- Verificando problemas do Anúncio 120245591905220720 ---');
  const adIssues = await api('120245591905220720', {
    fields: 'recommendations,ad_review_feedback,issues_info'
  });
  console.log('Problemas/Feedback:', JSON.stringify(adIssues, null, 2));
}

main();
