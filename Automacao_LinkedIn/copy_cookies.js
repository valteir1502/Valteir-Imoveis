const fs = require('fs');
const path = require('path');

const src = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies';
const dest = path.join(__dirname, 'Cookies_copy');

try {
  // Abre o arquivo de origem no modo de leitura ('r')
  const readStream = fs.createReadStream(src, { flags: 'r' });
  const writeStream = fs.createWriteStream(dest);

  readStream.on('error', (err) => {
    console.error('Erro ao ler Cookies de origem:', err.message);
  });

  writeStream.on('error', (err) => {
    console.error('Erro ao gravar Cookies de destino:', err.message);
  });

  writeStream.on('finish', () => {
    console.log('Arquivo Cookies copiado com sucesso via stream de leitura!');
  });

  readStream.pipe(writeStream);
} catch (e) {
  console.error('Falha geral na cópia dos cookies:', e.message);
}
