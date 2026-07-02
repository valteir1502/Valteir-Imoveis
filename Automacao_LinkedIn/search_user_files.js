const fs = require('fs');
const path = require('path');

const baseDir = 'c:\\Users\\User\\Desktop\\Negocios Imobiliários\\Valteir PROJETOS';

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    if (f === 'node_modules' || f === 'chrome-temp-profile' || f === 'chrome-data' || f === '.git') {
      return;
    }
    
    let stats = fs.statSync(dirPath);
    if (stats.isDirectory()) {
      walkDir(dirPath, callback);
    } else {
      callback(dirPath);
    }
  });
}

async function main() {
  if (!fs.existsSync(baseDir)) {
    console.error('Diretório de projetos não encontrado.');
    return;
  }

  console.log('Pesquisando tokens nos arquivos do usuário...');
  let foundTokens = new Set();

  walkDir(baseDir, (filePath) => {
    // Apenas arquivos de texto comuns
    if (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.zip') || filePath.endsWith('.exe')) {
      return;
    }
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const matches = content.match(/EAA[A-Za-z0-9]+/g);
      if (matches) {
        for (const token of matches) {
          if (token.length > 120) {
            foundTokens.add(JSON.stringify({ file: filePath, token: token.trim() }));
          }
        }
      }
    } catch (e) {
      // Ignorar erros de leitura
    }
  });

  console.log(`\nBusca concluída. Encontrados ${foundTokens.size} registros de tokens:`);
  Array.from(foundTokens).forEach((itemStr, index) => {
    const item = JSON.parse(itemStr);
    console.log(`\n[#${index + 1}] Arquivo: ${item.file}`);
    console.log(`Token: ${item.token}`);
    console.log(`Comprimento: ${item.token.length} caracteres`);
  });
}

main();
