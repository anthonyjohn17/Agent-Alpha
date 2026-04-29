const state = {
  selectedRunId: null,
  autoRefreshHandle: null,
  modelsByProvider: {},
};

async function apiGet(path) {
  const res = await fetch(path);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

async function apiPost(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

function statusClass(status) {
  return `status status-${status || "queued"}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function markdownToHtml(markdown) {
  const lines = String(markdown || "").split("\n");
  const html = [];
  let inList = false;

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (!line.trim()) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      continue;
    }
    if (line.startsWith("### ")) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<h4>${escapeHtml(line.slice(4))}</h4>`);
      continue;
    }
    if (line.startsWith("## ")) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<h3>${escapeHtml(line.slice(3))}</h3>`);
      continue;
    }
    if (line.startsWith("# ")) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<h2>${escapeHtml(line.slice(2))}</h2>`);
      continue;
    }
    if (line.startsWith("- ")) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${escapeHtml(line.slice(2))}</li>`);
      continue;
    }
    if (inList) {
      html.push("</ul>");
      inList = false;
    }
    html.push(`<p>${escapeHtml(line)}</p>`);
  }
  if (inList) html.push("</ul>");
  return html.join("");
}

async function loadHealth() {
  const pill = document.getElementById("health-pill");
  try {
    await apiGet("/api/health");
    pill.textContent = "Service healthy";
  } catch {
    pill.textContent = "Service unavailable";
  }
}

async function loadProvidersAndSettings() {
  const [{ providers }, { settings }, { models_by_provider }] = await Promise.all([
    apiGet("/api/providers"),
    apiGet("/api/settings"),
    apiGet("/api/models"),
  ]);
  state.modelsByProvider = models_by_provider || {};

  const providerSelect = document.getElementById("provider");
  const settingsProviderSelect = document.getElementById("s-provider");
  providerSelect.innerHTML = "";
  settingsProviderSelect.innerHTML = "";
  providers.forEach((provider) => {
    const opt = document.createElement("option");
    opt.value = provider;
    opt.textContent = provider;
    providerSelect.appendChild(opt);

    const optSettings = document.createElement("option");
    optSettings.value = provider;
    optSettings.textContent = provider;
    settingsProviderSelect.appendChild(optSettings);
  });

  providerSelect.value = settings.defaults.provider;
  settingsProviderSelect.value = settings.defaults.provider;
  populateModelDropdowns("provider", "deep-model", "quick-model", settings.defaults.deep_model, settings.defaults.quick_model);
  populateModelDropdowns(
    "s-provider",
    "s-deep-model",
    "s-quick-model",
    settings.defaults.deep_model,
    settings.defaults.quick_model
  );

  document.getElementById("debate-rounds").value = settings.defaults.debate_rounds;
  document.getElementById("checkpoint").checked = settings.defaults.checkpoint;

  document.getElementById("s-debate-rounds").value = settings.defaults.debate_rounds;
  document.getElementById("s-checkpoint").checked = settings.defaults.checkpoint;

  document.getElementById("k-openai").value = settings.api_keys.OPENAI_API_KEY || "";
  document.getElementById("k-anthropic").value = settings.api_keys.ANTHROPIC_API_KEY || "";
  document.getElementById("k-google").value = settings.api_keys.GOOGLE_API_KEY || "";
  document.getElementById("k-azure").value = settings.api_keys.AZURE_OPENAI_API_KEY || "";

  wireProviderModelSync();
}

function populateModelDropdowns(providerSelectId, deepModelId, quickModelId, deepModelValue, quickModelValue) {
  const provider = document.getElementById(providerSelectId).value;
  const modelOptions = state.modelsByProvider[provider] || [];
  const deepSelect = document.getElementById(deepModelId);
  const quickSelect = document.getElementById(quickModelId);
  deepSelect.innerHTML = "";
  quickSelect.innerHTML = "";

  modelOptions.forEach((model) => {
    const deepOpt = document.createElement("option");
    deepOpt.value = model;
    deepOpt.textContent = model;
    deepSelect.appendChild(deepOpt);

    const quickOpt = document.createElement("option");
    quickOpt.value = model;
    quickOpt.textContent = model;
    quickSelect.appendChild(quickOpt);
  });

  if (modelOptions.includes(deepModelValue)) {
    deepSelect.value = deepModelValue;
  } else if (modelOptions.length) {
    deepSelect.value = modelOptions[0];
  }
  if (modelOptions.includes(quickModelValue)) {
    quickSelect.value = quickModelValue;
  } else if (modelOptions.length > 1) {
    quickSelect.value = modelOptions[1];
  } else if (modelOptions.length) {
    quickSelect.value = modelOptions[0];
  }
}

function wireProviderModelSync() {
  const runProvider = document.getElementById("provider");
  const settingsProvider = document.getElementById("s-provider");

  runProvider.onchange = () => {
    populateModelDropdowns("provider", "deep-model", "quick-model");
  };
  settingsProvider.onchange = () => {
    populateModelDropdowns("s-provider", "s-deep-model", "s-quick-model");
  };
}

function setActiveTab(tab) {
  const runsBtn = document.getElementById("tab-runs");
  const settingsBtn = document.getElementById("tab-settings");
  const runsContent = document.getElementById("runs-tab-content");
  const settingsContent = document.getElementById("settings-tab-content");

  if (tab === "settings") {
    settingsBtn.classList.add("active");
    runsBtn.classList.remove("active");
    settingsContent.classList.remove("hidden");
    runsContent.classList.add("hidden");
    return;
  }

  runsBtn.classList.add("active");
  settingsBtn.classList.remove("active");
  runsContent.classList.remove("hidden");
  settingsContent.classList.add("hidden");
}

function renderRuns(runs) {
  const root = document.getElementById("runs-list");
  root.innerHTML = "";
  const totalRuns = document.getElementById("metric-total-runs");
  const activeRuns = document.getElementById("metric-active-runs");
  totalRuns.textContent = String(runs.length);
  activeRuns.textContent = String(runs.filter((run) => run.status === "running" || run.status === "queued").length);

  if (!runs.length) {
    root.innerHTML = '<div class="run-item">No runs yet.</div>';
    return;
  }

  runs.forEach((run) => {
    const div = document.createElement("div");
    div.className = "run-item";
    const logs = (run.logs || []).slice(-10).join("\n");
    const tickers = run.args && run.args.tickers ? run.args.tickers.join(", ") : "";
    div.innerHTML = `
      <div class="run-head">
        <strong>${run.id}</strong>
        <span class="${statusClass(run.status)}">${run.status}</span>
      </div>
      <div class="message">${run.command}</div>
      <div class="message">Tickers: ${tickers}</div>
      <div class="logs">${logs || "(no logs yet)"}</div>
    `;
    root.appendChild(div);
  });
}

async function loadRuns() {
  try {
    const { runs } = await apiGet("/api/runs");
    renderRuns(runs);
  } catch (err) {
    document.getElementById("runs-list").innerHTML = `<div class="run-item">${err.message}</div>`;
  }
}

function renderReports(reports) {
  const root = document.getElementById("reports-list");
  root.innerHTML = "";

  if (!reports.length) {
    root.innerHTML = '<div class="report-item">No reports found yet.</div>';
    return;
  }

  reports.forEach((report) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "report-item";
    btn.textContent = `${report.date} · ${report.ticker} · ${report.final_rating}`;
    btn.addEventListener("click", async () => {
      await loadReport(report.date, report.ticker);
    });
    root.appendChild(btn);
  });
}

async function loadReports() {
  try {
    const { reports } = await apiGet("/api/reports");
    renderReports(reports);
  } catch (err) {
    document.getElementById("reports-list").innerHTML = `<div class="report-item">${err.message}</div>`;
  }
}

async function loadReport(date, ticker) {
  const title = document.getElementById("report-title");
  const content = document.getElementById("report-content");
  try {
    const payload = await apiGet(`/api/report?date=${encodeURIComponent(date)}&ticker=${encodeURIComponent(ticker)}`);
    title.textContent = `${payload.date} · ${payload.ticker}`;
    content.innerHTML = markdownToHtml(payload.report);
  } catch (err) {
    title.textContent = "Failed to load report";
    content.textContent = err.message;
  }
}

function bindForms() {
  const runsTabBtn = document.getElementById("tab-runs");
  const settingsTabBtn = document.getElementById("tab-settings");
  runsTabBtn.addEventListener("click", () => setActiveTab("runs"));
  settingsTabBtn.addEventListener("click", () => setActiveTab("settings"));

  const runForm = document.getElementById("run-form");
  runForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("run-message");
    message.textContent = "Launching run...";
    try {
      await apiPost("/api/run", {
        tickers: document.getElementById("tickers").value,
        date: document.getElementById("date").value,
        provider: document.getElementById("provider").value,
        deep_model: document.getElementById("deep-model").value,
        quick_model: document.getElementById("quick-model").value,
        debate_rounds: Number(document.getElementById("debate-rounds").value),
        checkpoint: document.getElementById("checkpoint").checked,
      });
      message.textContent = "Run started.";
      await loadRuns();
    } catch (err) {
      message.textContent = err.message;
    }
  });

  const settingsForm = document.getElementById("settings-form");
  settingsForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("settings-message");
    message.textContent = "Saving settings...";
    try {
      await apiPost("/api/settings", {
        defaults: {
          provider: document.getElementById("s-provider").value,
          deep_model: document.getElementById("s-deep-model").value,
          quick_model: document.getElementById("s-quick-model").value,
          debate_rounds: Number(document.getElementById("s-debate-rounds").value),
          checkpoint: document.getElementById("s-checkpoint").checked,
        },
        api_keys: {
          OPENAI_API_KEY: document.getElementById("k-openai").value,
          ANTHROPIC_API_KEY: document.getElementById("k-anthropic").value,
          GOOGLE_API_KEY: document.getElementById("k-google").value,
          AZURE_OPENAI_API_KEY: document.getElementById("k-azure").value,
        },
      });
      message.textContent = "Settings saved.";
      await loadProvidersAndSettings();
    } catch (err) {
      message.textContent = err.message;
    }
  });
}

async function boot() {
  setActiveTab("runs");
  bindForms();
  await loadHealth();
  await loadProvidersAndSettings();
  await loadRuns();
  await loadReports();

  state.autoRefreshHandle = window.setInterval(async () => {
    await loadRuns();
    await loadReports();
  }, 2000);
}

boot();
