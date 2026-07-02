const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

(async () => {
  const chromeExecutable = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const officialUserDataDir = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data';
  const tempUserDataDir = path.join(__dirname, 'chrome-temp-profile');

  console.log('--- Preparando Perfil Temporário com Cookies do Usuário ---');
  try {
    // Cria pastas necessárias
    if (!fs.existsSync(tempUserDataDir)) {
      fs.mkdirSync(tempUserDataDir, { recursive: true });
    }
    const tempDefaultDir = path.join(tempUserDataDir, 'Default');
    if (!fs.existsSync(tempDefaultDir)) {
      fs.mkdirSync(tempDefaultDir, { recursive: true });
    }
    const tempNetworkDir = path.join(tempDefaultDir, 'Network');
    if (!fs.existsSync(tempNetworkDir)) {
      fs.mkdirSync(tempNetworkDir, { recursive: true });
    }

    // Copia Local State da raiz (essencial para decodificação DPAPI)
    fs.copyFileSync(
      path.join(officialUserDataDir, 'Local State'),
      path.join(tempUserDataDir, 'Local State')
    );
    console.log('✓ Local State copiado.');

    // Copia o arquivo Cookies já destravado (Cookies_test)
    const srcCookies = path.join(__dirname, 'Cookies_test');
    if (fs.existsSync(srcCookies)) {
      fs.copyFileSync(srcCookies, path.join(tempNetworkDir, 'Cookies'));
      console.log('✓ Arquivo Cookies copiado para a pasta de rede temporária.');
    } else {
      throw new Error('Arquivo Cookies_test não encontrado! Execute a cópia primeiro.');
    }

    // Copia a pasta Local Storage para manter estados de login locais se houver
    const officialLocalStorageDir = path.join(officialUserDataDir, 'Default', 'Local Storage');
    const tempLocalStorageDir = path.join(tempDefaultDir, 'Local Storage');
    if (fs.existsSync(officialLocalStorageDir)) {
      if (!fs.existsSync(tempLocalStorageDir)) {
        fs.mkdirSync(tempLocalStorageDir, { recursive: true });
      }
      try {
        execSync(`xcopy "${officialLocalStorageDir}" "${tempLocalStorageDir}" /E /I /H /Y /Q`);
        console.log('✓ Local Storage copiado.');
      } catch (e) {
        console.log('Aviso ao copiar Local Storage:', e.message);
      }
    }
  } catch (err) {
    console.error('Erro na preparação do perfil temporário:', err.message);
    process.exit(1);
  }

  console.log('Iniciando Puppeteer...');
  const browser = await puppeteer.launch({
    executablePath: chromeExecutable,
    userDataDir: tempUserDataDir,
    headless: true,
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

    console.log('Aguardando 12 segundos para carregar o token...');
    await new Promise(r => setTimeout(r, 12000));

    // Print para diagnóstico de sucesso
    const screenshotPath = path.join(__dirname, 'explorer_success_screen.png');
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
      await browser.close();
      cleanupTemp(tempUserDataDir);
      return;
    }

    // Extrai o token do DOM
    const token = await page.evaluate(() => {
      // Procura por inputs que comecem com EAA
      const inputs = Array.from(document.querySelectorAll('input'));
      for (const input of inputs) {
        if (input.value && input.value.startsWith('EAA')) {
          return input.value;
        }
      }
      // Procura em outros elementos do DOM
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
      console.log('Token não encontrado no DOM nem no localStorage.');
    }
  } catch (error) {
    console.error('Erro durante execução do Puppeteer:', error);
  } finally {
    await browser.close();
    cleanupTemp(tempUserDataDir);
  }
})();

function cleanupTemp(dir) {
  console.log('Limpando diretório temporário de perfil...');
  try {
    execSync(`rmdir /S /Q "${dir}"`);
    console.log('Pasta temporária limpa com sucesso.');
  } catch (e) {
    console.log('Aviso ao deletar pasta temporária:', e.message);
  }
}
