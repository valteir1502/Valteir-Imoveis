const fs = require('fs');
const path = require('path');
const readline = require('readline');

async function main() {
  const logFilePath = 'C:\\Users\\User\\.gemini\\antigravity\\brain\\c57af89f-aef6-43b4-9484-2fa0cf2b9815\\.system_generated\\logs\\transcript.jsonl';
  
  if (!fs.existsSync(logFilePath)) {
    console.error('Arquivo transcript.jsonl não encontrado.');
    return;
  }

  const fileStream = fs.createReadStream(logFilePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  console.log('Pesquisando chamadas de ferramenta de navegador dos passos anteriores (1 a 700)...');
  for await (const line of rl) {
    try {
      const obj = JSON.parse(line);
      if (obj.step_index < 730 && obj.tool_calls) {
        for (const tc of obj.tool_calls) {
          if (tc.name.includes('browser') || tc.name.includes('subagent') || tc.name.includes('mcp')) {
            console.log(`\n--- Passo ${obj.step_index} (${obj.type}) ---`);
            console.log(`Ferramenta: ${tc.name}`);
            console.log(`Argumentos:`, JSON.stringify(tc.args, null, 2));
          }
        }
      }
    } catch (e) {
      // Ignorar erros de parse ou linhas parciais
    }
  }
}

main();
