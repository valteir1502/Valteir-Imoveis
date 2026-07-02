const fs = require('fs');
const path = require('path');
const readline = require('readline');

async function main() {
  const logFilePath = 'C:\\Users\\User\\.gemini\\antigravity\\brain\\c57af89f-aef6-43b4-9484-2fa0cf2b9815\\.system_generated\\logs\\transcript.jsonl';
  
  if (!fs.existsSync(logFilePath)) {
    console.error('Arquivo transcript.jsonl não encontrado no caminho esperado.');
    return;
  }

  console.log('Buscando tokens no log do sistema...');
  const fileStream = fs.createReadStream(logFilePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let foundTokens = new Set();

  for await (const line of rl) {
    // Procura por strings que começam com EAA e têm caracteres típicos de token
    const matches = line.match(/EAA[A-Za-z0-9]+/g);
    if (matches) {
      for (const token of matches) {
        if (token.length > 150) { // Tokens reais são longos
          foundTokens.add(token);
        }
      }
    }
  }

  console.log(`Busca concluída. Encontrados ${foundTokens.size} tokens únicos:`);
  Array.from(foundTokens).forEach((token, index) => {
    console.log(`\nToken #${index + 1}:`);
    console.log(token);
    console.log(`Comprimento: ${token.length} caracteres`);
  });
}

main();
