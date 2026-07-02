const token = require('./token.json').token;
const CAMPAIGNS = ['120247078949660720', '120247080422180720'];

async function main() {
  console.log('--- Limpando Campanhas Vazias/Temporárias ---');
  for (const id of CAMPAIGNS) {
    const url = `https://graph.facebook.com/v17.0/${id}?access_token=${token}`;
    const res = await fetch(url, { method: 'DELETE' });
    const data = await res.json();
    console.log(`Deleção da campanha ${id}:`, data.success ? 'SUCESSO' : 'FALHA');
  }
}

main().catch(err => console.error(err));
