const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const chromeExecutable = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const tempUserDataDir = path.join(__dirname, 'chrome-temp-profile');

  console.log('Iniciando Puppeteer com perfil clonado...');
  const browser = await puppeteer.launch({
    executablePath: chromeExecutable,
    userDataDir: tempUserDataDir,
    headless: false, // modo gráfico para suportar DPAPI e interações
    args: [
      '--profile-directory=Default',
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    console.log('Navegando para o Graph Explorer...');
    await page.goto('https://developers.facebook.com/tools/explorer/', { waitUntil: 'networkidle2', timeout: 60000 });

    console.log('Aguardando 10 segundos para carregar...');
    await new Promise(r => setTimeout(r, 10000));

    // Salva print inicial
    await page.screenshot({ path: path.join(__dirname, 'auto_login_step1.png') });

    // Verifica se a tela de login do Facebook está aparecendo
    const needsLogin = await page.evaluate(() => {
      return document.body.innerText.includes('Continuar com o Facebook') || 
             document.body.innerText.includes('Entrar no Meta for Developers') ||
             !!document.querySelector('button, a, div[role="button"]') && 
             (document.body.innerText.includes('Log In') || document.body.innerText.includes('Entrar'));
    });

    if (needsLogin) {
      console.log('Tela de login detectada. Tentando clicar no botão de login...');
      
      // Procura por botões ou links que contenham "Continuar com o Facebook" ou "Log In"
      const clicked = await page.evaluate(() => {
        const elements = Array.from(document.querySelectorAll('button, a, div[role="button"], span'));
        for (const el of elements) {
          const text = el.innerText || el.textContent || '';
          if (text.includes('Continuar com o Facebook') || text.includes('Log In') || text.includes('Entrar com o Facebook')) {
            el.click();
            return true;
          }
        }
        return false;
      });

      if (clicked) {
        console.log('✓ Botão de login clicado! Aguardando 12 segundos para autenticação...');
        await new Promise(r => setTimeout(r, 12000));
        await page.screenshot({ path: path.join(__dirname, 'auto_login_step2.png') });
      } else {
        console.log('✗ Não foi possível encontrar o botão de login automaticamente.');
      }
    }

    // Procura o botão de gerar token
    const generated = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, div[role="button"]'));
      for (const btn of buttons) {
        const text = btn.innerText || btn.textContent || '';
        if (text.includes('Generate Access Token') || text.includes('Gerar token de acesso')) {
          btn.click();
          return true;
        }
      }
      return false;
    });

    if (generated) {
      console.log('✓ Botão "Generate Access Token" clicado! Aguardando 10 segundos...');
      await new Promise(r => setTimeout(r, 10000));
      await page.screenshot({ path: path.join(__dirname, 'auto_login_step3.png') });
    }

    // Extrai o token
    const token = await page.evaluate(() => {
      // 1. Tenta pegar do localStorage do Graph Explorer
      try {
        const lsToken = window.localStorage.getItem('GraphExplorer:accessToken');
        if (lsToken && lsToken.startsWith('EAA')) return lsToken;
      } catch (e) {}

      // 2. Tenta pegar do DOM
      const inputs = Array.from(document.querySelectorAll('input'));
      for (const input of inputs) {
        if (input.value && input.value.startsWith('EAA')) {
          return input.value;
        }
      }
      const divs = Array.from(document.querySelectorAll('div, span, textarea'));
      for (const div of divs) {
        const text = div.innerText || div.textContent || div.value || '';
        if (text.startsWith('EAA') && text.length > 100) {
          return text.trim();
        }
      }
      return null;
    });

    if (token) {
      console.log('✓ Novo token de acesso gerado e capturado com sucesso!');
      fs.writeFileSync(path.join(__dirname, 'token.json'), JSON.stringify({ token: token.trim() }, null, 2));
      console.log('Salvo no token.json.');
    } else {
      console.log('✗ Não foi possível extrair o token nesta tentativa.');
    }

  } catch (err) {
    console.error('Erro durante execução do auto-login:', err.message);
  } finally {
    await browser.close();
    console.log('Navegador fechado.');
  }
})();
