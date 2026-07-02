const fs = require('fs');
const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const IMAGE_PATH = 'C:/Users/User/Desktop/Negocios Imobiliários/Condomínio Village Provence/Alcides/Fotos/20260420_114342.jpg';

async function main() {
  console.log('--- Fazendo Upload da Miniatura ---');
  
  if (!fs.existsSync(IMAGE_PATH)) {
    throw new Error(`Imagem não encontrada em: ${IMAGE_PATH}`);
  }

  const formData = new FormData();
  formData.append('access_token', token);
  
  // Ler arquivo local e convertê-lo em Blob
  const fileBuffer = fs.readFileSync(IMAGE_PATH);
  const blob = new Blob([fileBuffer], { type: 'image/jpeg' });
  formData.append('filename', blob, 'thumbnail.jpg');

  const url = `https://graph.facebook.com/v17.0/${AD_ACCOUNT_ID}/adimages`;
  const res = await fetch(url, {
    method: 'POST',
    body: formData
  });

  const data = await res.json();
  if (data.error) {
    throw new Error(`Erro no Upload da Imagem: ${JSON.stringify(data.error)}`);
  }

  console.log('Imagem carregada com sucesso!');
  console.log('Resultado da API:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
