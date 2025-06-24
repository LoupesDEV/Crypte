document.addEventListener("DOMContentLoaded", () => {
  const domainInput = document.getElementById("domain");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const listDiv = document.getElementById("list");

  let masterKey = null;

  chrome.runtime.sendMessage({ type: "REQUEST_KEY" }, res => {
    masterKey = res.key;
    refresh();
  });

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

      Object.entries(data).forEach(([domain, encrypted]) => {
        if (domain === "masterHash") return;

        const div = document.createElement("div");
        div.className = "entry";

        try {
          const decrypted = JSON.parse(
            CryptoJS.AES.decrypt(encrypted, masterKey).toString(CryptoJS.enc.Utf8)
          );

          div.innerHTML = `
            <strong>${domain}</strong><br>
            👤 ${decrypted.username}
            <button class="copy-btn" data-copy="${decrypted.username}">⎘</button><br>
            🔑 <span class="masked">••••••••</span>
            <button class="reveal-btn" data-pw="${decrypted.password}">👁</button>
            <button class="copy-btn" data-copy="${decrypted.password}">⎘</button>
            <button class="edit-btn" data-domain="${domain}" data-user="${decrypted.username}" data-pw="${decrypted.password}">✎</button>
            <button class="delete-btn" data-domain="${domain}">❌</button>
          `;
          listDiv.appendChild(div);

        } catch (e) {
          div.textContent = `${domain} — 🔒 (verrouillé)`;
          listDiv.appendChild(div);
        }
      });

      listDiv.querySelectorAll(".reveal-btn").forEach(btn => {
        btn.onclick = () => {
          const span = btn.previousElementSibling;
          span.textContent = span.textContent === "••••••••" ? btn.dataset.pw : "••••••••";
        };
      });

      listDiv.querySelectorAll(".copy-btn").forEach(btn => {
        btn.onclick = () => {
          navigator.clipboard.writeText(btn.dataset.copy);
        };
      });

      listDiv.querySelectorAll(".delete-btn").forEach(btn => {
        btn.onclick = () => {
          const domain = btn.dataset.domain;
          chrome.storage.local.remove(domain, refresh);
        };
      });

      listDiv.querySelectorAll(".edit-btn").forEach(btn => {
        btn.onclick = () => {
          domainInput.value = btn.dataset.domain;
          usernameInput.value = btn.dataset.user;
          passwordInput.value = btn.dataset.pw;
        };
      });
    });
  }
});