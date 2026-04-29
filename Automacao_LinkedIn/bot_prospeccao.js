const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Caminhos dos arquivos
const historicoPath = path.join(__dirname, 'relatorio_prospeccao.json');
const leadsPath = path.join(__dirname, 'leads_db.json');

function carregarJSON(caminho) {
    if (fs.existsSync(caminho)) {
        try {
            return JSON.parse(fs.readFileSync(caminho, 'utf-8'));
        } catch (e) {
            return [];
        }
    }
    return [];
}

function salvarJSON(caminho, dados) {
    fs.writeFileSync(caminho, JSON.stringify(dados, null, 2), 'utf-8');
}

function registrarNoHistorico(url, status, detalhes = '') {
    const historico = carregarJSON(historicoPath);
    historico.push({
        data: new Date().toLocaleString('pt-BR'),
        url: url,
        status: status,
        detalhes: detalhes
    });
    salvarJSON(historicoPath, historico);
}

function salvarLead(lead) {
    const leads = carregarJSON(leadsPath);
    // Evitar duplicados
    const index = leads.findIndex(l => l.url === lead.url);
    if (index !== -1) {
        leads[index] = { ...leads[index], ...lead };
    } else {
        leads.push(lead);
    }
    salvarJSON(leadsPath, leads);
}

function gerarMensagem(nome, cargo) {
    const primeirNome = nome.split(' ')[0];
    const cargoFmt = cargo.split('at')[0].trim(); // Pega o cargo antes da empresa se houver
    
    return `Olá ${primeirNome}! Tudo bem?

Acompanho sua trajetória como ${cargoFmt} e gostaria de conectar. Atuo com assessoria estratégica para o mercado imobiliário de alto padrão aqui em São José do Rio Preto.

Meu trabalho foca na curadoria de oportunidades exclusivas em condomínios como o Quinta do Golfe e os Damhas, muitas vezes com acessos 'off-market' que não chegam ao grande público.

Acredito que compartilhar networking e tendências do mercado local seja valioso para ambos. Um abraço, Valteir.`;
}

(async () => {
    // CAMINHO DO SEU NAVEGADOR
    const chromeExecutable = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    
    // USANDO PASTA LOCAL PARA PERFIL (Evita travas no Chrome do usuário)
    const userDataDir = path.join(__dirname, 'chrome-data');

    const browser = await puppeteer.launch({
        executablePath: chromeExecutable,
        userDataDir: userDataDir,
        headless: false,
        args: [
            '--profile-directory=Default',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-notifications',
            '--disable-features=Translate'
        ]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    const alvosPath = path.join(__dirname, 'lista_alvos.txt');
    if (!fs.existsSync(alvosPath)) {
        console.error('Arquivo lista_alvos.txt não encontrado!');
        await browser.close();
        return;
    }

    const alvos = fs.readFileSync(alvosPath, 'utf-8').split('\n').map(l => l.trim()).filter(l => l.startsWith('http'));
    const historico = carregarJSON(historicoPath);

    console.log(`Iniciando prospecção inteligente para ${alvos.length} perfis...`);
    
    // ESTABILIZAR SESSÃO (Acessa o feed primeiro)
    console.log('Estabilizando sessão no LinkedIn...');
    await page.goto('https://www.linkedin.com', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await new Promise(r => setTimeout(r, 10000));

    // Função auxiliar para pausa
    const wait = (ms) => new Promise(r => setTimeout(r, ms));

    for (let url of alvos) {
        // Verificar se já foi enviado com sucesso anteriormente
        if (historico.some(h => h.url === url && h.status === 'Sucesso')) {
            console.log(`--- Ignorando (já enviado): ${url} ---`);
            continue;
        }

        try {
            const partesUrl = url.split('/in/')[1].split('-');
            const nomeSemCidade = partesUrl.slice(0, 2).join(' ');
            const nomeBusca = nomeSemCidade; // Busca ampla para garantir visibilidade
            const primeiroNome = partesUrl[0];
            console.log(`--- Iniciando Busca Humana por: ${nomeBusca} ---`);
            
            const seletorBusca = 'input[placeholder="Pesquisar"], input[aria-label="Pesquisar"]';
            
            if (!await page.$(seletorBusca)) {
                await page.goto('https://www.linkedin.com', { waitUntil: 'domcontentloaded' });
                await wait(5000);
            }

            await page.waitForSelector(seletorBusca, { timeout: 15000 });
            await page.click(seletorBusca);
            await wait(1000);
            
            await page.keyboard.down('Control');
            await page.keyboard.press('A');
            await page.keyboard.up('Control');
            await page.keyboard.press('Backspace');
            
            await page.keyboard.type(nomeBusca, { delay: 120 });
            await page.keyboard.press('Enter');
            await wait(10000); // Aguarda resultados carregarem 100%
            
            // Lógica de Raio-X: Mira Laser por URL (Flexível e Infalível)
            const linkEncontrado = await page.evaluate((urlAlvo) => {
                const links = Array.from(document.querySelectorAll('a'));
                const handleAlvo = urlAlvo.split('/in/')[1]?.split('/')[0]?.split('?')[0].replace(/\/$/, "");
                
                // Busca link que contenha o handle único do perfil
                const alvo = links.find(l => {
                    const href = l.href.toLowerCase();
                    return href.includes(`/in/${handleAlvo.toLowerCase()}`) && !href.includes('/search/');
                });
                
                if (alvo) {
                    return { texto: alvo.innerText.trim(), href: alvo.href };
                }
                return null;
            }, url);

            if (linkEncontrado) {
                console.log(`Alvo Confirmado via URL: ${linkEncontrado.texto} (${linkEncontrado.href})`);
                await page.goto(linkEncontrado.href, { waitUntil: 'domcontentloaded' });
                var clicou = true;
            } else {
                console.log('URL exata não detectada. Buscando por correspondência de Nome...');
                const linkNome = await page.evaluate((nome) => {
                    const links = Array.from(document.querySelectorAll('a'));
                    const alvo = links.find(l => {
                        const txt = l.innerText.toLowerCase();
                        return txt.includes(nome.toLowerCase()) && l.href.includes('/in/') && !l.href.includes('/search/');
                    });
                    return alvo ? { texto: alvo.innerText.trim(), href: alvo.href } : null;
                }, nomeSemCidade);

                if (linkNome) {
                    console.log(`Alvo Identificado por Nome: ${linkNome.texto} (${linkNome.href})`);
                    await page.goto(linkNome.href, { waitUntil: 'domcontentloaded' });
                    var clicou = true;
                } else {
                    var clicou = false; 
                }
            }

            if (!clicou) {
                console.log('Tentando clique via seletor de emergência...');
                const clicou2 = await page.evaluate(() => {
                    const el = document.querySelector('.entity-result__title-text a, .app-aware-link');
                    if (el && el.href.includes('/in/')) { el.click(); return true; }
                    return false;
                });
                if (!clicou2) throw new Error('Perfil real não localizado na busca');
            }
            
            await wait(15000);
            await page.evaluate(() => window.scrollBy(0, 400));
            await wait(2000);
            await page.waitForFunction(() => {
                const h1 = document.querySelector('h1');
                const h2 = document.querySelector('h2');
                return (h1 && h1.innerText.length > 2) || (h2 && h2.innerText.length > 2);
            }, { timeout: 25000 });

            // EXTRAIR DADOS DO PERFIL (Versão Infalível com Filtro de Sistema)
            const perfil = await page.evaluate(() => {
                const titulo = document.title;
                let nomeRaw = titulo.split('|')[0].trim();
                
                // Se o título for genérico, tenta pegar o H1/H2 real da página
                if (nomeRaw.includes('Colega') || nomeRaw.includes('Notificações') || nomeRaw.includes('LinkedIn') || nomeRaw.length < 3) {
                    const h1 = document.querySelector('h1');
                    const h2 = document.querySelector('h2');
                    if (h1) nomeRaw = h1.innerText.split('\n')[0].trim();
                    else if (h2) nomeRaw = h2.innerText.split('\n')[0].trim();
                }

                // Captura Localização (Apenas no cabeçalho do perfil)
                const header = document.querySelector('.pv-text-details__left-panel') || document.querySelector('main section');
                const locElement = header ? (header.querySelector('.text-body-small.inline.t-black--light.break-words') || 
                                            header.querySelector('.pv-text-details__left-panel.mt2 span')) : null;
                
                const localizacao = locElement ? locElement.innerText.trim() : 'Não informada';

                const nomeLimpio = nomeRaw.replace(/\(.*\)/g, '').replace(/[^\p{L}\s]/gu, '').trim();
                
                return { nome: nomeLimpio, localizacao };
            });

            // Se der "Não informada", tenta uma última vez após 3 segundos
            if (perfil.localizacao === 'Não informada') {
                await wait(3000);
                perfil.localizacao = await page.evaluate(() => {
                    const loc = document.querySelector('.text-body-small.inline.t-black--light.break-words') || 
                                 document.querySelector('.pv-text-details__left-panel.mt2 span') ||
                                 document.querySelector('main section .text-body-small');
                    return loc ? loc.innerText.trim() : 'Não informada';
                });
            }

            const cidadesPermitidas = ['São José do Rio Preto', 'Mirassol', 'Bady Bassitt', 'Guapiaçu', 'Olímpia', 'SJRP', 'São Paulo e Região', 'São Paulo, Brasil'];
            const ehDaRegiao = cidadesPermitidas.some(c => perfil.localizacao.includes(c));

            // LÓGICA DE EXECUÇÃO GARANTIDA: Se está na lista de alvos, não pulamos por erro de GPS
            if (!ehDaRegiao && perfil.localizacao !== 'Não informada') {
                console.log(`Lead fora da região alvo: ${perfil.localizacao}. Pulando...`);
                await wait(2000);
                continue;
            } else if (perfil.localizacao === 'Não informada') {
                console.log(`Aviso: Localização não detectada, mas prosseguindo por ser alvo da lista de elite.🎯`);
            }

            console.log(`Perfil identificado na região: ${perfil.nome} (${perfil.localizacao})`);

            const perfilCompleto = await page.evaluate(() => {
                const main = document.querySelector('main');
                const allP = Array.from((main || document).querySelectorAll('p, div, span'));
                const cargoEle = allP.find(p => {
                    const txt = p.innerText.trim();
                    return txt.length > 10 && 
                           txt.length < 150 && 
                           !txt.includes('Pular para') && 
                           !txt.includes('Início') && 
                           !txt.includes('conexo') && 
                           !txt.includes('Dados de contato') &&
                           p.offsetParent !== null;
                });

                return {
                    cargo: cargoEle ? cargoEle.innerText.split('\n')[0].trim() : 'Empresário/Diretor'
                };
            });

            // Atualiza dados estratégicos
            perfil.cargo = perfilCompleto.cargo;

            console.log(`Perfil identificado estrategicamente: ${perfil.nome} (${perfil.cargo})`);
            salvarLead({ ...perfil, url, data_captura: new Date().toLocaleDateString('pt-BR'), status: 'Acessado' });

            const mensagemPersonalizada = gerarMensagem(perfil.nome, perfil.cargo);

            // 1. PRIORIDADE: BOTÃO "ENVIAR MENSAGEM" (Qualquer Cor/Estilo)
            const logicaBotaoMsg = await page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                
                // Busca por texto (Independente de ser azul ou branco)
                const alvo = buttons.find(b => {
                    const txt = b.innerText.toLowerCase();
                    return (txt.includes('enviar mensagem') || txt.trim() === 'mensagem') && 
                           b.offsetParent !== null;
                });
                
                if (alvo) {
                    alvo.click();
                    return true;
                }
                
                // Plano B: Pelo ícone de aviãozinho (conforme print do usuário)
                const btnIcone = buttons.find(b => 
                    b.querySelector('svg[data-test-icon="send-privately-small"]') ||
                    b.querySelector('li-icon[type="send-privately"]')
                );
                if (btnIcone) {
                    btnIcone.click();
                    return true;
                }
                
                return false;
            });

            if (logicaBotaoMsg) {
                console.log('Botão de mensagem acionado! Aguardando modal (8s)...');
                await wait(8000); // Mais tempo para o modal carregar

                // Tirar print do modal para diagnóstico
                const timestamp = Date.now();
                const debugModal = path.join(__dirname, `debug_modal_${timestamp}.png`);
                const debugHTML = path.join(__dirname, `debug_modal_${timestamp}.html`);
                await page.screenshot({ path: debugModal });
                fs.writeFileSync(debugHTML, await page.content());
                console.log(`Diagnóstico do modal salvo (PNG/HTML)!`);

                // Detectar se há iframes (comum em modais de mensagem)
                const iframeCount = await page.evaluate(() => document.querySelectorAll('iframe').length);
                if (iframeCount > 0) console.log(`Atenção: ${iframeCount} iframes detectados no modal.`);

                // PREENCHER INMAIL (Abordagem de Raio-X: Busca em Iframe e Main)
                const preencherCampos = async (msg, nome) => {
                    const frames = page.frames();
                    let preenchido = false;

                    for (const frame of frames) {
                        try {
                            const sucesso = await frame.evaluate((m, n) => {
                                // 1. Tentar achar Assunto
                                const campoAssunto = document.querySelector('input[name="subject"], .msg-form__subject, input[placeholder*="Assunto"]');
                                if (campoAssunto && !campoAssunto.value) {
                                    campoAssunto.value = `Networking — ${n}`;
                                    campoAssunto.dispatchEvent(new Event('input', { bubbles: true }));
                                }

                                // 2. Tentar achar Corpo
                                const corpo = document.querySelector('.msg-form__contenteditable, div[contenteditable="true"], .ql-editor, textarea[name="message"]');
                                if (corpo) {
                                    corpo.focus();
                                    if (corpo.tagName === 'DIV') {
                                        corpo.innerHTML = `<p>${m.replace(/\n/g, '<br>')}</p>`;
                                    } else {
                                        corpo.value = m;
                                    }
                                    corpo.dispatchEvent(new Event('input', { bubbles: true }));
                                    corpo.dispatchEvent(new Event('change', { bubbles: true }));
                                    return true;
                                }
                                return false;
                            }, msg, nome);
                            
                            if (sucesso) {
                                preenchido = true;
                                break;
                            }
                        } catch (e) { /* ignora erros de cross-origin */ }
                    }
                    return preenchido;
                };

                const sucessoInMail = await preencherCampos(mensagemPersonalizada, perfil.nome);

                if (sucessoInMail) {
                    console.log('✓ InMail preenchido com sucesso (Raio-X)!');
                    registrarNoHistorico(perfil.nome, url, 'Sucesso', 'InMail preenchido');
                    
                    // CLIQUE FINAL EM ENVIAR (MODO 100% AUTOMÁTICO)
                    console.log('Finalizando: Enviando mensagem agora...');
                    // CLIQUE FINAL EM ENVIAR (MODO 100% AUTOMÁTICO)
                    console.log('Finalizando: Enviando apresentação...');
                    await page.evaluate(() => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        const btn = buttons.find(b => 
                            b.innerText.toLowerCase().trim() === 'enviar' || 
                            b.innerText.toLowerCase().trim() === 'send' ||
                            b.classList.contains('msg-form__send-button') ||
                            b.getAttribute('type') === 'submit' ||
                            b.querySelector('svg[data-test-icon="send-privately-small"]') ||
                            b.querySelector('li-icon[type="send-privately"]')
                        );
                        if (btn) {
                            btn.click();
                            return true;
                        }
                        return false;
                    });
                    
                    await wait(3000); // Espera o disparo ser concluído
                } else {
                    console.log('! Falha técnica ao preencher os campos do InMail.');
                }
                continue;
            }

            // 2. SEGUNDA OPÇÃO: CONECTAR (SE NÃO ESTIVER PENDENTE)
            const btnConectar = await page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const b = buttons.find(b => b.innerText.includes('Conectar') || b.innerText.includes('Connect'));
                if (b && !b.innerText.includes('Pendente')) return true;
                return false;
            });

            if (btnConectar) {
                console.log('Tentando pedido de conexão...');
                await page.evaluate(() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    buttons.find(b => b.innerText.includes('Conectar') || b.innerText.includes('Connect')).click();
                });
                await wait(2000);

                const addNotaBtn = await page.evaluate(() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    return buttons.find(b => b.innerText.includes('Adicionar uma nota') || b.innerText.includes('Add a note'));
                });

                if (addNotaBtn) {
                    await page.evaluate(() => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        buttons.find(b => b.innerText.includes('Adicionar uma nota') || b.innerText.includes('Add a note')).click();
                    });
                    await wait(1000);
                    await page.keyboard.type(mensagemPersonalizada, { delay: 40 });
                    await wait(1000);
                    await page.evaluate(() => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        buttons.find(b => b.innerText.includes('Enviar') || b.innerText.includes('Send')).click();
                    });
                    console.log('Convite com nota enviado!');
                    registrarNoHistorico(url, 'Sucesso', 'Conexão com nota');
                    continue;
                }
            }

            console.log('Perfil ignorado: Nenhuma opção de contato imediata ou convite já pendente.');
            registrarNoHistorico(url, 'Aviso', 'Pendente ou sem botões de contato');

        } catch (err) {
            console.error(`Erro ao processar ${url}:`, err.message);
            registrarNoHistorico(url, 'Erro', err.message);
        }
    }

    console.log('Prospecção finalizada!');
    await browser.close();
})();
