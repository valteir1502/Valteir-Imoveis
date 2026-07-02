const token = require('./token.json').token;

const CREATIVE_ID = '1867337303916386';
const IMAGE_HASH = '89398f975b8114fa5d9660cf37f5c065';

async function main() {
  console.log('--- Tentando Atualizar Criativo Existente ---');
  
  const body = new URLSearchParams();
  body.append('access_token', token);
  body.append('image_hash', IMAGE_HASH);
  // Também vamos tentar definir o link_data ou apenas o image_hash
  
  const url = `https://graph.facebook.com/v17.0/${CREATIVE_ID}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  const data = await res.json();
  console.log('Resultado da Atualização do Criativo:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
