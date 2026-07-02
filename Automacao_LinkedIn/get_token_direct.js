const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const chromeExecutable = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const officialUserDataDir = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data';

  console.log('Iniciando Puppeteer diretamente com o perfil oficial do Chrome do usuário...');
  try {
    const browser = await puppeteer.launch({
      executablePath: chromeExecutable,
      userDataDir: officialUserDataDir,
      headless: true,
      args: [
        '--profile-directory=Default',
        '--no-sandbox',
        '--disable-setuid-sandbox'
      ]
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    console.log('Navegando para o Graph Explorer...');
    await page.goto('https://developers.facebook.com/tools/explorer/', { waitUntil: 'networkidle2', timeout: 60000 });

    console.log('Aguardando 12 segundos para carregar...');
    await new Promise(r => setTimeout(r, 12000));

    // Print para diagnóstico
    const screenshotPath = path.join(__dirname, 'explorer_screen_direct.png');
    await page.screenshot({ path: screenshotPath });
    console.log(`Print da tela salvo em: ${screenshotPath}`);

    // Tenta extrair o token do localStorage
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
      await browser.close();
      return;
    }

    // Tenta extrair o token via DOM
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
      console.log('Token não encontrado no DOM nem no localStorage do perfil oficial.');
    }

    await browser.close();
  } catch (error) {
    console.error('Erro ao abrir perfil oficial diretamente:', error);
  }
})();
