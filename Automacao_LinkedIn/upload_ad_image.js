const fs = require('fs');
const path = require('path');
const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const IMAGE_URL = 'https://cdn3.praedium.com.br/1700g8BocjY0sIkrqD1/8815023963369/m3moxym2odnhmjyymdi0oduw_md.jpg';

async function main() {
  console.log('--- Fazendo download da foto da fachada ---');
  const tempPath = path.join(__dirname, 'fachada_damha.jpg');
  
  const response = await fetch(IMAGE_URL);
  const buffer = await response.arrayBuffer();
  fs.writeFileSync(tempPath, Buffer.from(buffer));
  console.log('Imagem salva em:', tempPath);

  console.log('--- Fazendo upload para o Meta Ads ---');
  
  // Como fetch nativo do Node 18+ suporta FormData e File/Blob:
  const blob = new Blob([fs.readFileSync(tempPath)], { type: 'image/jpeg' });
  const formData = new FormData();
  formData.append('filename', blob, 'fachada_damha.jpg');
  formData.append('access_token', token);

  const uploadUrl = `https://graph.facebook.com/v17.0/${AD_ACCOUNT_ID}/adimages`;
  const uploadRes = await fetch(uploadUrl, {
    method: 'POST',
    body: formData
  });

  const data = await uploadRes.json();
  console.log('Resultado do Upload:', JSON.stringify(data, null, 2));
}

main().catch(err => console.error(err));
