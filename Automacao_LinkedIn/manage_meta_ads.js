const fs = require('fs');
const path = require('path');
const token = require('./token.json').token;

let logContent = '';
function log(msg) {
  console.log(msg);
  logContent += msg + '\n';
}

async function api(path, params = {}) {
  const query = new URLSearchParams({
    access_token: token,
    ...params
  }).toString();
  const url = `https://graph.facebook.com/v17.0/${path}?${query}`;
  const res = await fetch(url);
  const data = await res.json();
  if (data.error) {
    throw new Error(`Erro na API (${path}): ${JSON.stringify(data.error)}`);
  }
  return data;
}

async function main() {
  log('# Relatório de Auditoria Completa do Meta Ads\n');
  log(`Gerado em: ${new Date().toISOString()}\n`);
  
  try {
    log('## 1. Contas de Anúncios');
    const accountsData = await api('me/adaccounts', { fields: 'name,id,account_status,currency' });
    
    if (!accountsData.data || accountsData.data.length === 0) {
      log('Nenhuma conta de anúncios encontrada.');
      return;
    }

    log(`Encontradas ${accountsData.data.length} contas:\n`);
    for (const acc of accountsData.data) {
      log(`### CONTA: **${acc.name}** (ID: \`${acc.id}\`) [Status: ${acc.account_status}]`);
      
      try {
        // Listar Campanhas da conta
        const campaigns = await api(`${acc.id}/campaigns`, {
          fields: 'name,id,status,objective,buying_type',
          effective_status: '["ACTIVE", "PAUSED"]'
        });

        if (!campaigns.data || campaigns.data.length === 0) {
          log('  *Nenhuma campanha encontrada nesta conta.*\n');
          continue;
        }

        log(`  *Total de campanhas:* ${campaigns.data.length}\n`);
        for (const camp of campaigns.data) {
          log(`  #### CAMPANHA: **${camp.name}** (ID: \`${camp.id}\`)`);
          log(`  - **Status:** \`${camp.status}\``);
          log(`  - **Objetivo:** \`${camp.objective}\``);
          
          // Listar Ad Sets para a campanha
          const adSets = await api(`${camp.id}/adsets`, {
            fields: 'name,id,status,targeting,daily_budget,lifetime_budget,billing_event,optimization_goal'
          });

          if (adSets.data && adSets.data.length > 0) {
            log(`  - *Conjuntos de Anúncios:*`);
            for (const adset of adSets.data) {
              log(`    * **ADSET:** \`${adset.name}\` (ID: \`${adset.id}\`)`);
              log(`      - Status: \`${adset.status}\``);
              log(`      - Orçamento: ${adset.daily_budget ? 'R$ ' + (adset.daily_budget/100).toFixed(2) + '/dia' : 'Vitalício: ' + adset.lifetime_budget}`);
              log(`      - Otimização: \`${adset.optimization_goal}\` | Cobrança: \`${adset.billing_event}\``);
              log(`      - Segmentação Atual:`);
              log(`\`\`\`json\n${JSON.stringify(adset.targeting, null, 2)}\n\`\`\``);

              // Listar Anúncios para o Ad Set
              const ads = await api(`${adset.id}/ads`, {
                fields: 'name,id,status,creative{name,id,body,title}'
              });

              if (ads.data && ads.data.length > 0) {
                log(`      - *Anúncios:*`);
                for (const ad of ads.data) {
                  log(`        * **Anúncio:** \`${ad.name}\` (ID: \`${ad.id}\`) [Status: \`${ad.status}\`]`);
                  if (ad.creative) {
                    log(`          - Título: *${ad.creative.title || 'Sem título'}*`);
                    log(`          - Texto: _${ad.creative.body || 'Sem texto'}_`);
                  }
                }
              } else {
                log(`      - *Nenhum anúncio.*`);
              }
            }
          } else {
            log(`  - *Nenhum Ad Set.*`);
          }
          log('\n  ---');
        }
      } catch (e) {
        log(`  *Erro ao ler campanhas desta conta:* ${e.message}\n`);
      }
      log('\n==================================================\n');
    }

    // Salva o relatório no disco
    fs.writeFileSync(path.join(__dirname, '..', 'campanhas_auditoria.md'), logContent, 'utf8');
    console.log('\nRelatório geral salvo com sucesso em campanhas_auditoria.md');

  } catch (err) {
    log(`Erro geral: ${err.message}`);
  }
}

main();
