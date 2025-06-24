document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("lockForm");
  const msg = document.getElementById("msg");
  const title = document.getElementById("title");

  chrome.storage.local.get("masterHash", data => {
    if (!data.masterHash) {
      title.textContent = "Créer mot de passe maître";
    }
  });

  form.addEventListener("submit", e => {
    e.preventDefault();
    const pass = document.getElementById("master").value;
    const hash = CryptoJS.SHA256(pass).toString();

    chrome.storage.local.get("masterHash", data => {
      if (!data.masterHash) {
        chrome.storage.local.set({ masterHash: hash }, () => {
          chrome.runtime.sendMessage({ type: "UNLOCK", key: pass });
          window.location.href = "popup/popup.html";
        });
      } else if (data.masterHash === hash) {
        chrome.runtime.sendMessage({ type: "UNLOCK", key: pass });
        window.location.href = "popup/popup.html";
      } else {
        msg.textContent = "Mot de passe incorrect.";
      }
    });
  });
});