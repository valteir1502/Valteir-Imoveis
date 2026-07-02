const token = require('./token.json').token;

async function main() {
  console.log('--- Buscando Contas de Páginas (Tokens) ---');
  const url = `https://graph.facebook.com/v17.0/me/accounts?access_token=${token}`;
  const res = await fetch(url);
  const data = await res.json();
  
  if (data.error) {
    console.error('Erro:', data.error);
    return;
  }

  console.log('Páginas encontradas:');
  for (const page of data.data) {
    console.log('--------------------------------------------------');
    console.log('Nome:', page.name);
    console.log('ID:', page.id);
    console.log('Category:', page.category);
    console.log('Page Token:', page.access_token);
  }
}

main();
