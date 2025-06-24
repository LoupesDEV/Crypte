let isUnlocked = false;
let masterKey = null;
let timeout = null;

function lockExtension() {
  isUnlocked = false;
  masterKey = null;
}

function unlockWithTimeout(key) {
  isUnlocked = true;
  masterKey = key;
  if (timeout) clearTimeout(timeout);
  timeout = setTimeout(() => {
    lockExtension();
  }, 2 * 60 * 1000);
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "REQUEST_KEY") {
    return sendResponse({ key: masterKey });
  }
});


chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "UNLOCK") {
    unlockWithTimeout(msg.key);
    sendResponse({ ok: true });
  }

  if (msg.type === "GET_CREDENTIALS") {
    if (!isUnlocked) return sendResponse({ creds: null });
    const domain = msg.domain;
    chrome.storage.local.get([domain], data => {
      const encrypted = data[domain];
      if (!encrypted) return sendResponse({ creds: null });
      const decrypted = JSON.parse(
        CryptoJS.AES.decrypt(encrypted, masterKey).toString(CryptoJS.enc.Utf8)
      );
      sendResponse({ creds: decrypted });
    });
    return true;
  }

  if (msg.type === "SET_CREDENTIALS") {
    if (!isUnlocked) return sendResponse({ success: false });
    const { domain, creds } = msg;
    const encrypted = CryptoJS.AES.encrypt(JSON.stringify(creds), masterKey).toString();
    chrome.storage.local.set({ [domain]: encrypted }, () => {
      sendResponse({ success: true });
    });
    return true;
  }
});