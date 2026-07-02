const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const officialUserDataDir = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data';
const tempUserDataDir = path.join(__dirname, 'chrome-temp-profile');

function copyFileSafe(src, dest) {
  try {
    if (fs.existsSync(src)) {
      const parentDir = path.dirname(dest);
      if (!fs.existsSync(parentDir)) {
        fs.mkdirSync(parentDir, { recursive: true });
      }
      fs.copyFileSync(src, dest);
      console.log(`✓ Copiado: ${path.basename(src)}`);
    } else {
      console.log(`- Não encontrado: ${path.basename(src)}`);
    }
  } catch (e) {
    console.log(`✗ Erro ao copiar ${path.basename(src)}:`, e.message);
  }
}

async function main() {
  console.log('--- Clonando Perfil do Chrome do Usuário de Forma Completa ---');
  
  // Limpa diretório temporário anterior
  if (fs.existsSync(tempUserDataDir)) {
    try {
      execSync(`rmdir /S /Q "${tempUserDataDir}"`);
      console.log('✓ Perfil temporário anterior removido.');
    } catch (e) {
      console.log('Aviso ao limpar pasta temporária anterior:', e.message);
    }
  }

  // Cria novas pastas
  const tempDefaultDir = path.join(tempUserDataDir, 'Default');
  fs.mkdirSync(tempDefaultDir, { recursive: true });

  // 1. Copia Local State
  copyFileSafe(
    path.join(officialUserDataDir, 'Local State'),
    path.join(tempUserDataDir, 'Local State')
  );

  // 2. Copia Cookies (usamos a nossa cópia destravada Cookies_test se a original falhar)
  const officialCookies = path.join(officialUserDataDir, 'Default', 'Network', 'Cookies');
  const tempCookies = path.join(tempDefaultDir, 'Network', 'Cookies');
  
  try {
    copyFileSafe(officialCookies, tempCookies);
  } catch (e) {
    console.log('Falha ao copiar Cookies oficial diretamente, tentando usar Cookies_test...');
    copyFileSafe(path.join(__dirname, 'Cookies_test'), tempCookies);
  }

  // 3. Copia Preferences
  copyFileSafe(
    path.join(officialUserDataDir, 'Default', 'Preferences'),
    path.join(tempDefaultDir, 'Preferences')
  );

  // 4. Copia Secure Preferences
  copyFileSafe(
    path.join(officialUserDataDir, 'Default', 'Secure Preferences'),
    path.join(tempDefaultDir, 'Secure Preferences')
  );

  // 5. Copia Local Storage (contém tokens e estados persistidos do DOM)
  const officialLocalStorage = path.join(officialUserDataDir, 'Default', 'Local Storage');
  const tempLocalStorage = path.join(tempDefaultDir, 'Local Storage');
  if (fs.existsSync(officialLocalStorage)) {
    try {
      fs.mkdirSync(tempLocalStorage, { recursive: true });
      execSync(`xcopy "${officialLocalStorage}" "${tempLocalStorage}" /E /I /H /Y /Q`);
      console.log('✓ Pasta Local Storage copiada.');
    } catch (e) {
      console.log('Aviso ao copiar Local Storage:', e.message);
    }
  }

  console.log('Clonagem concluída!');
}

main();
