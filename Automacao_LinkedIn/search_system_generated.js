const fs = require('fs');
const path = require('path');

const baseDir = 'C:\\Users\\User\\.gemini\\antigravity\\brain\\c57af89f-aef6-43b4-9484-2fa0cf2b9815\\.system_generated';

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    if (isDirectory) {
      walkDir(dirPath, callback);
    } else {
      callback(dirPath);
    }
  });
}

async function main() {
  if (!fs.existsSync(baseDir)) {
    console.error('Diretório .system_generated não encontrado.');
    return;
  }

  console.log('Pesquisando tokens do Facebook em .system_generated...');
  let foundTokens = new Set();

  walkDir(baseDir, (filePath) => {
    // Ignora arquivos binários como png
    if (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.zip')) {
      return;
    }
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const matches = content.match(/EAA[A-Za-z0-9]+/g);
      if (matches) {
        for (const token of matches) {
          if (token.length > 120) {
            foundTokens.add(JSON.stringify({ file: path.basename(filePath), token: token.trim() }));
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
