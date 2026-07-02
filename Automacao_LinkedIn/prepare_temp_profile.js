const fs = require('fs');
const path = require('path');

const officialUserDataDir = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data';
const tempUserDataDir = path.join(__dirname, 'chrome-temp-profile');

console.log('--- Preparando Perfil Temporário para Nova Instância do Chrome ---');
try {
  if (!fs.existsSync(tempUserDataDir)) {
    fs.mkdirSync(tempUserDataDir, { recursive: true });
  }
  const tempDefaultDir = path.join(tempUserDataDir, 'Default');
  if (!fs.existsSync(tempDefaultDir)) {
    fs.mkdirSync(tempDefaultDir, { recursive: true });
  }
  const tempNetworkDir = path.join(tempDefaultDir, 'Network');
  if (!fs.existsSync(tempNetworkDir)) {
    fs.mkdirSync(tempNetworkDir, { recursive: true });
  }

  // Copia Local State
  fs.copyFileSync(
    path.join(officialUserDataDir, 'Local State'),
    path.join(tempUserDataDir, 'Local State')
  );
  console.log('✓ Local State copiado.');

  // Copia Cookies_test (já destravado anteriormente)
  const srcCookies = path.join(__dirname, 'Cookies_test');
  if (fs.existsSync(srcCookies)) {
    fs.copyFileSync(srcCookies, path.join(tempNetworkDir, 'Cookies'));
    console.log('✓ Cookies copiados.');
  } else {
    throw new Error('Cookies_test não encontrado! Rode o copy_test.js primeiro.');
  }
  
  console.log('Perfil temporário preparado com sucesso!');
} catch (e) {
  console.error('Erro ao preparar perfil:', e.message);
}
