const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  console.log('Tentando conectar ao Chrome na porta 9222...');
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://localhost:9222'
    });

    console.log('Conectado com sucesso! Abrindo nova aba...');
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    console.log('Navegando para o Graph Explorer...');
    await page.goto('https://developers.facebook.com/tools/explorer/', { waitUntil: 'networkidle2', timeout: 60000 });

    console.log('Aguardando 10 segundos para carregar o token...');
    await new Promise(r => setTimeout(r, 10000));

    // Salva print da tela para vermos o estado visual
    const screenshotPath = path.join(__dirname, 'explorer_remote_screen.png');
    await page.screenshot({ path: screenshotPath });
    console.log(`Print da tela salvo em: ${screenshotPath}`);

    // Extrai o token do localStorage
    const localStorageToken = await page.evaluate(() => {
      try {
        return window.localStorage.getItem('GraphExplorer:accessToken') || '';
      } catch (e) {
        return '';
      }
    });

    if (localStorageToken && localStorageToken.startsWith('EAA')) {
      console.log('Token encontrado no localStorage!');
      fs.writeFileSync(path.join(__dirname, 'token.json'), JSON.stringify({ token: localStorageToken.trim() }, null, 2));
      console.log('Token completo salvo com sucesso no arquivo token.json!');
      await page.close();
      await browser.disconnect();
      return;
    }

    // Extrai o token do DOM
    const token = await page.evaluate(() => {
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
      console.log('Token encontrado no DOM!');
      fs.writeFileSync(path.join(__dirname, 'token.json'), JSON.stringify({ token: token.trim() }, null, 2));
      console.log('Token completo salvo com sucesso no arquivo token.json!');
    } else {
      console.log('Token não encontrado no DOM nem no localStorage do Chrome conectado.');
    }

    await page.close();
    await browser.disconnect();
  } catch (error) {
    console.error('Erro ao conectar ou executar no Chrome remoto:', error.message);
  }
})();
