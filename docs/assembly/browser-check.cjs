// Shared browser-check infrastructure; each suite owns its scenarios and assertions.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');

const htmlPath = path.resolve('docs/assembly.html');
const htmlURL = pathToFileURL(htmlPath).href;

async function withBrowser(check) {
  const {firefox} = require(process.env.PLAYWRIGHT_MODULE || '/tmp/kanpo-review-browser/node_modules/playwright');
  const browser = await firefox.launch({
    headless: true,
    executablePath: process.env.FIREFOX_PATH || '/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox',
  });
  try {
    return await check(browser);
  } finally {
    await browser.close();
  }
}

function monitorPage(page, {consoleErrors = false, requestsAsErrors = false} = {}) {
  const errors = [], requests = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    const url = request.url();
    if (!/^https?:/.test(url)) return;
    if (requestsAsErrors) errors.push('Unexpected request: ' + url);
    else requests.push(url);
  });
  if (consoleErrors) {
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
    });
  }
  return {errors, requests};
}

function htmlHash() {
  return crypto.createHash('sha256').update(fs.readFileSync(htmlPath)).digest('hex');
}

function writeReport(file, report) {
  const json = JSON.stringify(report, null, 2);
  fs.writeFileSync(file, json + '\n');
  console.log(json);
}

module.exports = {withBrowser, monitorPage, htmlURL, htmlHash, writeReport};
