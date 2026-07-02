const token = require('./token.json').token;
const AD_SET_ID = '120247080465980720';

async function main() {
  console.log(`--- Verificando Anúncios no Ad Set ${AD_SET_ID} ---`);
  
  const url = `https://graph.facebook.com/v17.0/${AD_SET_ID}/ads?fields=id,name,status,effective_status,creative{id,name}&access_token=${token}`;
  const res = await fetch(url);
  const data = await res.json();
  
  if (data.error) {
    console.error('Erro na API do Facebook:', data.error);
    return;
  }

  if (!data.data || data.data.length === 0) {
    console.log('Nenhum anúncio encontrado neste conjunto ainda.');
    return;
  }

  console.log(`Encontrado(s) ${data.data.length} anúncio(s):`);
  for (const ad of data.data) {
    console.log('--------------------------------------------------');
    console.log('ID do Anúncio:', ad.id);
    console.log('Nome do Anúncio:', ad.name);
    console.log('Status Configurado:', ad.status);
    console.log('Status Efetivo (Veiculação):', ad.effective_status);
    if (ad.creative) {
      console.log('ID do Criativo Associado:', ad.creative.id);
      console.log('Nome do Criativo:', ad.creative.name);
    }
  }
}

main().catch(err => console.error(err));
