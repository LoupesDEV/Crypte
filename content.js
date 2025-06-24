(function () {
  const domain = window.location.hostname;

  chrome.runtime.sendMessage({ type: "GET_CREDENTIALS", domain }, response => {
    if (response && response.creds) {
      injectPopup(response.creds);
    }
  });

  function injectPopup(creds) {
    if (document.getElementById("crypte-popup")) return;

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