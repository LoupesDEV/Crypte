(function () {
  const domain = window.location.hostname;

  chrome.runtime.sendMessage({ type: "GET_CREDENTIALS", domain }, response => {
    if (response && response.creds) {
      injectPopup(response.creds);
    }
  });

  function injectPopup(creds) {
    if (document.getElementById("crypte-popup")) return;

    const style = document.createElement("style");
    style.textContent = `
      #crypte-popup {
        position: fixed;
        top: 12px;
        right: 12px;
        z-index: 999999;
        background: #1e1e2f;
        color: #f4f4f4;
        padding: 14px;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
        font-family: 'Segoe UI', sans-serif;
        max-width: 260px;
        backdrop-filter: blur(4px);
      }

      #crypte-popup h3 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #c2113a;
        font-size: 16px;
      }

      #crypte-popup code {
        display: block;
        background: #2c2c3e;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 13px;
        margin-bottom: 6px;
        user-select: all;
        color: #ffffff;
      }

      #crypte-popup button {
        width: 100%;
        padding: 6px;
        background: #c2113a;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        cursor: pointer;
        margin-top: 8px;
        transition: background 0.2s;
      }

      #crypte-popup button:hover {
        background: #a10e2f;
      }
    `;
    document.head.appendChild(style);

    const box = document.createElement("div");
    box.id = "crypte-popup";
    box.innerHTML = `
      <h3>Crypte</h3>
      <code>${creds.username}</code>
      <code>${creds.password}</code>
      <button id="crypte-close">Fermer</button>
    `;
    box.querySelector("#crypte-close").onclick = () => box.remove();
    document.body.appendChild(box);
  }
})();