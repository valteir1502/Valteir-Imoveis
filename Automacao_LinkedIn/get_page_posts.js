const token = require('./token.json').token;
const PAGE_ID = '102441765221079';

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
  console.log('--- Buscando posts da Página ---');
  const feed = await api(`${PAGE_ID}/published_posts`, {
    fields: 'id,message,created_time,permalink_url'
  });
  
  if (feed.error) {
    console.error('Erro:', feed.error);
    return;
  }

  console.log(`Encontrados ${feed.data.length} posts:`);
  for (const post of feed.data) {
    console.log('--------------------------------------------------');
    console.log('ID:', post.id);
    console.log('Criado em:', post.created_time);
    console.log('Mensagem:', post.message ? post.message.substring(0, 100) + '...' : 'Sem texto');
    console.log('Link:', post.permalink_url);
  }
}

main();
