// fetch nativo é usado

const tokens = [
  // Token 1
  'EAAXrwZCwdGUsBRv7bMnqFZAecoWdVSRoZA80E9KZBvF2zgIlCR40kXn4YpM2mDOKWZAev2MYiDKgGdJpjMD6IlQas4X3nls8BROJ04OE8NpCADBDGC64VaonNpIkMOZAQJZBpZAg5oj5AZBJZBMbQadKRQ945xYGxxuoNOsCXIN3RGGVANZBjt1kKamA4GYFHYqzZCSt8KaLWshWwgtJQQxJgnZA616aqos4M9eL6pvvmBkYU5Z',
  // Token 2
  'EAAXrwZCwdGUsBRaG1cTtScjZAmebM5fbSDv8HoDEXo9CEsZBPUsJ8p4clCOiEbPpEx0gTP08Fb3ZCBJwUU389TXqPw6FoSK6zdr24nXtYgCZABhNurauxuRoOmLNrAmO3l8XiZB1d4USAoZCSX0dNC9Woc95y1Gcpt8yI9pLRAkcZByGZAyaWvu7aZCRxBD6dNiHian89ZB4MKUCkzBpmWIKye2cZC6t09SUThG5PmiLAoZAcVZ',
  // Token 3
  'EAAXrwZCwdGUsBRZAiZB5fZB2EMxjv7BhlPzerbJt9yftmvdZAaVTtZADnLuSYSVOfj2GzgOPZCAVQRFrTp1ZBAPXvhr4Sa6e19fMVZCZAqnNfZBUAo4E5pLvBo7oDqUk5VWIyADZBZAUGOZCOJ0VDZAajE9gH0sTdZAtaymvifeAZAYi3nKmZAOdxzdLp1mqRMWsPtzxw8p9fDLCkQrw7Lop0GibdynJkzySJhZAJUlZB1ZCVto',
  // Token 4
  'EAAXrwZCwdGUsBRXQ3yPYRmZBq08XcaVo5trZBZA4fE2trWphIZCx3YZCVlGzFMIRpdfZCKA1zq6PnkBgNFvVZCSpRNlq3R6nnIp1XBi53WbrEfZADZCZAEyZAkJ3istGJY2oSCnpV3pUIR7sgMDIsU54m0jjKGCHNEdn0tiqeB7gJv9ZAZB5dEcmfHoqnOfxtfcWNfjzLovQEozshDCKzRwhuV5bjxsLoasLMrgJ8pAJaU3i3Vq',
  // Token 5
  'EAAXrwZCwdGUsBRWMXfWsqI1UB7UgfyafgykrOyZBwJMs1L7gllGxjjTeNGmchXKIjVdnwYhuKHvwNAeJfy2p30dLttwLEoa3Kl5Hn7bEiLnr5a9l077vqujtzg3W1nrS9sVMVPmpBohyjwc5yDJUWH0Rj4j4K21K4C4mbLViWZAN321ZCE4SG6wwZBVcLceFlrnpUalnAyNw9lDNA4uUZAyk1RetSqTE7MWEnA0ZBqPXbDmXuDq',
  // Token 6 (O que deu erro de criptografia)
  'EAAXrwZCwdGUsBRvUMeAAiWF1sVrDtCrxSZB4BtyZCTZBLprScUp7ZABMIEYJiMZbSNlEIIpO3nQoYZAANll8k1ZC8ZCLUO1EJ4625nL0MGja1WK7B2of55PckQQ7aDhelt5Leou6HssOH6uJYg6C0s6ubj6sq1udwTLYvuZCWQbE2wPtL7BYvPNZC7ATEHRueQgMuZA0HTMv9O0frUCkyaAcZCi74z9SjH9XmnyZADXSeHBNWEylipolKzlgZDZD'
];

async function testToken(token, index) {
  const url = `https://graph.facebook.com/v17.0/me?fields=name,id&access_token=${token}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.id) {
      console.log(`[+] Token #${index + 1} VÁLIDO! Nome: ${data.name}, ID: ${data.id}`);
      return { index, token, valid: true, data };
    } else {
      console.log(`[-] Token #${index + 1} INVÁLIDO. Erro: ${JSON.stringify(data.error)}`);
      return { index, token, valid: false };
    }
  } catch (err) {
    console.log(`[!] Token #${index + 1} FALHOU na requisição: ${err.message}`);
    return { index, token, valid: false };
  }
}

async function main() {
  console.log('--- Testando todos os 6 tokens com a Graph API ---');
  
  // No node moderno, fetch é global, senão usa node-fetch se disponível
  if (typeof fetch === 'undefined') {
    global.fetch = require('node-fetch');
  }

  for (let i = 0; i < tokens.length; i++) {
    await testToken(tokens[i], i);
  }
}

main();
