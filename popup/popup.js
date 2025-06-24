document.addEventListener("DOMContentLoaded", () => {
  const domainInput = document.getElementById("domain");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const listDiv = document.getElementById("list");

  refresh();

  document.getElementById("saveForm").addEventListener("submit", e => {
    e.preventDefault();

    const domain = domainInput.value.trim();
    const creds = { username: usernameInput.value, password: passwordInput.value };

    chrome.runtime.sendMessage({ type: "SET_CREDENTIALS", domain, creds }, () => {
      domainInput.value = usernameInput.value = passwordInput.value = "";
      refresh();
    });
  });

  function refresh() {
    chrome.storage.local.get(null, data => {
      listDiv.innerHTML = "";
      Object.entries(data).forEach(([domain, creds]) => {
        const div = document.createElement("div");
        div.textContent = `${domain} — ${creds.username}`;
        listDiv.appendChild(div);
      });
    });
  }
});