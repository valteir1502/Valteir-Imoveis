const fs = require('fs');
const path = require('path');
const token = require('./token.json').token;

const AD_ACCOUNT_ID = 'act_317759256861786';
const VIDEO_PATH = 'C:/Users/User/Desktop/Negocios Imobiliários/Condomínio Village Provence/Alcides/Video/Alcides - Provence(1).mp4';
const CHUNK_SIZE = 10 * 1024 * 1024; // 10 MB por parte

async function apiPost(params) {
  const formData = new FormData();
  for (const [key, val] of Object.entries(params)) {
    if (val instanceof Blob) {
      formData.append(key, val, 'chunk.mp4');
    } else {
      formData.append(key, val);
    }
  }

  const url = `https://graph.facebook.com/v17.0/${AD_ACCOUNT_ID}/advideos`;
  const res = await fetch(url, {
    method: 'POST',
    body: formData
  });

  const data = await res.json();
  if (data.error) {
    throw new Error(`Erro na API do Facebook: ${JSON.stringify(data.error)}`);
  }
  return data;
}

async function main() {
  console.log('--- Iniciando Upload Resumível de Vídeo ---');
  
  if (!fs.existsSync(VIDEO_PATH)) {
    throw new Error(`Arquivo não encontrado em: ${VIDEO_PATH}`);
  }

  const fileStats = fs.statSync(VIDEO_PATH);
  const fileSize = fileStats.size;
  console.log(`Tamanho do vídeo: ${(fileSize / (1024 * 1024)).toFixed(2)} MB (${fileSize} bytes)`);

  // 1. FASE DE INICIALIZAÇÃO
  console.log('\n[Fase 1] Inicializando sessão de upload...');
  const initResult = await apiPost({
    access_token: token,
    upload_phase: 'start',
    file_size: fileSize.toString()
  });

  const sessionId = initResult.upload_session_id;
  const videoId = initResult.video_id;
  console.log(`Sessão iniciada com ID: ${sessionId}`);
  console.log(`ID do Vídeo alocado: ${videoId}`);

  // 2. FASE DE TRANSFERÊNCIA (CHUNKS)
  console.log('\n[Fase 2] Transferindo vídeo em partes de 10MB...');
  const fd = fs.openSync(VIDEO_PATH, 'r');
  let startOffset = 0;

  while (startOffset < fileSize) {
    const buffer = Buffer.alloc(CHUNK_SIZE);
    const bytesRead = fs.readSync(fd, buffer, 0, CHUNK_SIZE, startOffset);
    const chunkBuffer = buffer.subarray(0, bytesRead);
    
    console.log(`Enviando parte: offset ${startOffset} a ${startOffset + bytesRead} ...`);
    
    const blob = new Blob([chunkBuffer], { type: 'video/mp4' });
    const transferResult = await apiPost({
      access_token: token,
      upload_phase: 'transfer',
      upload_session_id: sessionId,
      start_offset: startOffset.toString(),
      video_file_chunk: blob
    });

    // Validar se o offset avançou corretamente
    const nextOffset = parseInt(transferResult.start_offset);
    const endOffset = parseInt(transferResult.end_offset);
    console.log(`Confirmado offset avançado de ${nextOffset} para ${endOffset}`);
    
    startOffset = endOffset;
  }
  fs.closeSync(fd);
  console.log('Todos os chunks foram enviados com sucesso!');

  // 3. FASE DE FINALIZAÇÃO
  console.log('\n[Fase 3] Finalizando sessão de upload...');
  const finishResult = await apiPost({
    access_token: token,
    upload_phase: 'finish',
    upload_session_id: sessionId
  });

  console.log('Resultado da Finalização:', finishResult);
  console.log(`\n--- UPLOAD CONCLUÍDO COM SUCESSO! ---`);
  console.log(`ID DO VÍDEO DO ALCIDES: ${videoId}`);
  
  // Salvar o ID do vídeo para uso posterior
  fs.writeFileSync(path.join(__dirname, 'video_id.json'), JSON.stringify({ video_id: videoId }, null, 2));
}

main().catch(err => {
  console.error('\nErro no Upload do Vídeo:', err.message);
  process.exit(1);
});
