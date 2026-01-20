async function api(path, opts) {
  const res = await fetch(path, Object.assign({ headers: { "content-type": "application/json" } }, opts || {}));
  const ct = res.headers.get("content-type") || "";
  const body = ct.includes("application/json") ? await res.json() : await res.text();
  if (!res.ok) {
    const msg = typeof body === "string" ? body : (body.detail || JSON.stringify(body));
    throw new Error(msg);
  }
  return body;
}

function setTab(name) {
  document.querySelectorAll(".tab").forEach(b => b.classList.toggle("active", b.dataset.tab === name));
  document.querySelectorAll(".panel").forEach(p => p.classList.toggle("show", p.id === name));
}

let currentReceiptFile = null;
let receiptsIndex = [];

function renderReceiptList(items) {
  const list = document.getElementById("receiptList");
  list.innerHTML = "";
  items.forEach(it => {
    const div = document.createElement("div");
    div.className = "item";
    const decision = it.decision || "";
    const code = it.refusal_code || "";
    const rid = it.receipt_id || it.file;
    div.innerHTML = `<strong>${decision} ${code ? "· " + code : ""}</strong><span>${it.timestamp_utc || ""} · ${rid}</span>`;
    div.onclick = async () => {
      currentReceiptFile = it.file;
      const data = await api(`/api/receipts/${encodeURIComponent(it.file)}`);
      document.getElementById("receiptJson").textContent = JSON.stringify(data.receipt, null, 2);
    };
    list.appendChild(div);
  });
}

function applyFilter() {
  const q = (document.getElementById("filterText").value || "").toLowerCase().trim();
  if (!q) return renderReceiptList(receiptsIndex);
  const filtered = receiptsIndex.filter(it => JSON.stringify(it).toLowerCase().includes(q));
  renderReceiptList(filtered);
}

async function loadStatus() {
  const s = await api("/api/status");
  document.getElementById("statusJson").textContent = JSON.stringify(s, null, 2);

  const pill = document.getElementById("readonlyPill");
  pill.textContent = s.read_only ? "READ_ONLY" : "EDIT_ENABLED";
  pill.style.borderColor = s.read_only ? "#2a3040" : "#3a6ff7";
}

async function loadPolicy() {
  const p = await api("/api/policy");
  document.getElementById("policyEditor").value = JSON.stringify(p.policy, null, 2);
  document.getElementById("policyMeta").textContent =
    `${p.path} · hash ${p.policy_hash.slice(0,12)}… · valid ${p.valid} · read_only ${p.read_only}`;
  document.getElementById("policyValidation").textContent = p.valid ? "OK" : (p.validation_errors || []).join("\n");

  const btnApply = document.getElementById("btnApplyPolicy");
  btnApply.disabled = p.read_only;
}

async function validatePolicy() {
  const raw = document.getElementById("policyEditor").value;
  let obj;
  try { obj = JSON.parse(raw); } catch (e) { throw new Error("Invalid JSON in editor"); }
  const v = await api("/api/policy/validate", { method: "POST", body: JSON.stringify({ policy: obj }) });
  document.getElementById("policyValidation").textContent = v.valid ? "OK" : (v.validation_errors || []).join("\n");
  return { obj, v };
}

async function applyPolicy() {
  const { obj, v } = await validatePolicy();
  if (!v.valid) throw new Error("Policy failed validation; cannot apply.");
  const r = await api("/api/policy", { method: "PUT", body: JSON.stringify({ policy: obj }) });
  await loadPolicy();
  await loadStatus();
  return r;
}

async function loadReceipts() {
  const r = await api("/api/receipts");
  receiptsIndex = r.items || [];
  renderReceiptList(receiptsIndex);
  document.getElementById("receiptJson").textContent = "";
  currentReceiptFile = null;
}

function wireUI() {
  document.querySelectorAll(".tab").forEach(b => {
    b.onclick = () => setTab(b.dataset.tab);
  });

  document.getElementById("btnReloadStatus").onclick = () => loadStatus().catch(alert);
  document.getElementById("btnReloadPolicy").onclick = () => loadPolicy().catch(alert);
  document.getElementById("btnValidatePolicy").onclick = () => validatePolicy().catch(alert);
  document.getElementById("btnApplyPolicy").onclick = () => applyPolicy().catch(alert);
  document.getElementById("btnReloadReceipts").onclick = () => loadReceipts().catch(alert);

  document.getElementById("filterText").oninput = () => applyFilter();

  document.getElementById("btnDownloadReceipt").onclick = () => {
    if (!currentReceiptFile) return alert("Select a receipt first.");
    window.location.href = `/api/receipts/${encodeURIComponent(currentReceiptFile)}/download`;
  };
}

(async function main() {
  wireUI();
  await loadStatus().catch(() => {});
  await loadPolicy().catch(() => {});
  await loadReceipts().catch(() => {});
})();
