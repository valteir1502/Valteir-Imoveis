const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Matando processos chrome.exe...');
  try {
    execSync('taskkill /IM chrome.exe /F');
  } catch (e) {
    console.log('Nenhum processo chrome.exe ativo ou erro ao matar:', e.message);
  }

  console.log('Aguardando 3 segundos para liberação de handles pelo SO...');
  await new Promise(r => setTimeout(r, 3000));

  const src = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies';
  const dest = path.join(__dirname, 'Cookies_test');

  console.log(`Tentando copiar de ${src} para ${dest}...`);
  try {
    fs.copyFileSync(src, dest);
    console.log('SUCESSO! Arquivo Cookies copiado com sucesso.');
    const stats = fs.statSync(dest);
    console.log(`Tamanho do arquivo copiado: ${stats.size} bytes`);
  } catch (e) {
    console.error('FALHA na cópia dos cookies:', e.message);
  }
}

main();
