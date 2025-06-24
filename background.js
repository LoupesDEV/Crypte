chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  switch (msg.type) {
    case "GET_CREDENTIALS": {
      const domain = msg.domain;
      chrome.storage.local.get([domain], data => {
        sendResponse({ creds: data[domain] || null });
      });
      return true;
    }
    case "SET_CREDENTIALS": {
      const { domain, creds } = msg;
      chrome.storage.local.set({ [domain]: creds }, () => {
        sendResponse({ success: true });
      });
      return true;
    }
  }
});