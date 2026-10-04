const money = new Intl.NumberFormat("en-UG", { maximumFractionDigits: 0 });
const number = new Intl.NumberFormat("en-UG");
const pageSize = 12;
let data;
let rows = [];
let filtered = [];
let page = 0;

const ui = {
    period: document.querySelector("#periodFilter"),
    channel: document.querySelector("#channelFilter"),
    store: document.querySelector("#storeFilter"),
    district: document.querySelector("#districtFilter"),
    category: document.querySelector("#categoryFilter"),
    sales: document.querySelector("#salesKpi"),
    customers: document.querySelector("#customersKpi"),
    transactions: document.querySelector("#transactionsKpi"),
    returns: document.querySelector("#returnsKpi"),
    returnNote: document.querySelector("#returnsNote"),
    table: document.querySelector("#transactionRows"),
    dialog: document.querySelector("#detailDialog"),
};

const ugx = value => `UGX ${money.format(Math.round(value || 0))}`;
const compactUgx = value => {
    const millions = value / 1_000_000;
    return millions >= 1000 ? `UGX ${(millions / 1000).toFixed(1)}B` : `UGX ${millions.toFixed(1)}M`;
};
const pct = value => `${(value || 0).toFixed(1)}%`;
const monthLabel = value => new Intl.DateTimeFormat("en", { month: "short", year: "2-digit", timeZone: "UTC" }).format(new Date(`${value}-01T00:00:00Z`));
const safe = value => String(value ?? "").replace(/[&<>"']/g, character => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);

async function loadDashboard() {
    try {
        const response = await fetch("./data/srg-demo.json", { cache: "no-store" });
        if (!response.ok) throw new Error(`Data request returned ${response.status}`);
        data = await response.json();
        rows = data.transactions.map(record => ({
            date: record[0], customer: record[1], product: record[2], store: record[3],
            storeName: record[4], channel: record[5], quantity: record[6], amount: record[7],
            district: record[8], category: record[9],
        }));
        populateFilters();
        bindControls();
        renderQuality();
        render();
    } catch (error) {
        document.querySelector(".demo-notice p").textContent = `Dashboard data could not load: ${error.message}. Serve this folder over HTTP and regenerate the demo data.`;
        document.querySelector("#transactionRows").innerHTML = '<tr><td colspan="7" class="error-state">No dashboard data loaded.</td></tr>';
    }
}

function populateFilters() {
    const distinct = (key, label = value => value) => [...new Set(rows.map(row => row[key]))].sort().map(value => `<option value="${safe(value)}">${safe(label(value))}</option>`).join("");
    const months = [...new Set(rows.map(row => row.date.slice(0, 7)))].sort();
    ui.period.insertAdjacentHTML("beforeend", months.map(month => `<option value="${month}">${monthLabel(month)}</option>`).join(""));
    ui.channel.insertAdjacentHTML("beforeend", distinct("channel"));
    const stores = [...new Map(rows.filter(row => row.store.startsWith("ST")).map(row => [row.store, row.storeName])).entries()].sort((a, b) => a[1].localeCompare(b[1]));
    ui.store.insertAdjacentHTML("beforeend", stores.map(([id, name]) => `<option value="${safe(id)}">${safe(name)}</option>`).join(""));
    ui.district.insertAdjacentHTML("beforeend", distinct("district"));
    ui.category.insertAdjacentHTML("beforeend", distinct("category"));
    document.querySelector("#periodLabel").textContent = data.period;
}

function bindControls() {
    [ui.period, ui.channel, ui.store, ui.district, ui.category].forEach(control => control.addEventListener("change", () => { page = 0; render(); }));
    document.querySelector("#resetFilters").addEventListener("click", () => {
        [ui.period, ui.channel, ui.store, ui.district, ui.category].forEach(control => { control.value = "all"; });
        page = 0;
        render();
    });
    document.querySelector("#prevPage").addEventListener("click", () => { page = Math.max(0, page - 1); renderTable(); });
    document.querySelector("#nextPage").addEventListener("click", () => { page = Math.min(Math.ceil(filtered.length / pageSize) - 1, page + 1); renderTable(); });
    document.querySelector("#downloadButton").addEventListener("click", downloadView);
    document.querySelector("#closeDialog").addEventListener("click", () => ui.dialog.close());
    window.addEventListener("resize", drawTrend, { passive: true });
}

function applyFilters() {
    return rows.filter(row =>
        (ui.period.value === "all" || row.date.startsWith(ui.period.value)) &&
        (ui.channel.value === "all" || row.channel === ui.channel.value) &&
        (ui.store.value === "all" || row.store === ui.store.value) &&
        (ui.district.value === "all" || row.district === ui.district.value) &&
        (ui.category.value === "all" || row.category === ui.category.value)
    );
}

function render() {
    filtered = applyFilters();
    const netSales = filtered.reduce((sum, row) => sum + row.amount, 0);
    const activeCustomers = new Set(filtered.map(row => row.customer)).size;
    const returnLines = filtered.filter(row => row.quantity < 0).length;
    ui.sales.textContent = compactUgx(netSales);
    ui.customers.textContent = number.format(activeCustomers);
    ui.transactions.textContent = number.format(filtered.length);
    ui.returns.textContent = pct(filtered.length ? returnLines / filtered.length * 100 : 0);
    ui.returnNote.textContent = `${number.format(returnLines)} negative-quantity lines`;
    const selectedMonth = ui.period.value === "all" ? "Jan–Jun 2025" : monthLabel(ui.period.value);
    document.querySelector("#headingPeriod").textContent = selectedMonth;
    document.querySelector("#trendCaption").textContent = `${number.format(filtered.length)} transaction lines · all sales converted to UGX`;
    renderTrend();
    renderBars("categoryChart", aggregate(filtered, "category"), "category");
    renderStores(filtered);
    renderTable();
}

function aggregate(sourceRows, key) {
    const totals = new Map();
    sourceRows.forEach(row => totals.set(row[key], (totals.get(row[key]) || 0) + row.amount));
    return [...totals].sort((a, b) => b[1] - a[1]);
}

function renderTrend() {
    const totals = new Map();
    filtered.forEach(row => {
        const month = row.date.slice(0, 7);
        totals.set(month, (totals.get(month) || 0) + row.amount);
    });
    const values = [...totals].sort((a, b) => a[0].localeCompare(b[0]));
    drawTrend(values);
}

function drawTrend(values) {
    if (!Array.isArray(values)) {
        const totals = new Map();
        filtered.forEach(row => {
            const month = row.date.slice(0, 7);
            totals.set(month, (totals.get(month) || 0) + row.amount);
        });
        values = [...totals].sort((a, b) => a[0].localeCompare(b[0]));
    }
    const canvas = document.querySelector("#trendChart");
    const bounds = canvas.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.round(bounds.width * ratio);
    canvas.height = Math.round(bounds.height * ratio);
    const context = canvas.getContext("2d");
    context.scale(ratio, ratio);
    const width = bounds.width;
    const height = bounds.height;
    const pad = { left: 48, right: 14, top: 12, bottom: 29 };
    const plotWidth = width - pad.left - pad.right;
    const plotHeight = height - pad.top - pad.bottom;
    const maximum = Math.max(1, ...values.map(item => item[1])) * 1.12;
    context.clearRect(0, 0, width, height);
    context.font = '9px "DM Mono", Consolas, monospace';
    context.textBaseline = "middle";
    for (let tick = 0; tick <= 4; tick++) {
        const y = pad.top + plotHeight * tick / 4;
        context.strokeStyle = "#e9eee8";
        context.beginPath();
        context.moveTo(pad.left, y);
        context.lineTo(width - pad.right, y);
        context.stroke();
        context.fillStyle = "#89958e";
        context.textAlign = "right";
        context.fillText((maximum * (1 - tick / 4) / 1_000_000).toFixed(0), pad.left - 8, y);
    }
    if (!values.length) {
        context.fillStyle = "#77857d";
        context.textAlign = "center";
        context.fillText("No data for these filters", width / 2, height / 2);
        return;
    }
    const points = values.map((item, index) => ({
        x: values.length === 1 ? pad.left + plotWidth / 2 : pad.left + plotWidth * index / (values.length - 1),
        y: pad.top + plotHeight * (1 - item[1] / maximum), month: item[0], value: item[1],
    }));
    const gradient = context.createLinearGradient(0, pad.top, 0, pad.top + plotHeight);
    gradient.addColorStop(0, "rgba(231, 121, 91, .22)");
    gradient.addColorStop(1, "rgba(231, 121, 91, 0)");
    context.beginPath();
    context.moveTo(points[0].x, pad.top + plotHeight);
    points.forEach(point => context.lineTo(point.x, point.y));
    context.lineTo(points.at(-1).x, pad.top + plotHeight);
    context.closePath();
    context.fillStyle = gradient;
    context.fill();
    context.beginPath();
    points.forEach((point, index) => index ? context.lineTo(point.x, point.y) : context.moveTo(point.x, point.y));
    context.strokeStyle = "#d96e52";
    context.lineWidth = 2.5;
    context.lineJoin = "round";
    context.stroke();
    points.forEach(point => {
        context.beginPath();
        context.arc(point.x, point.y, 3.3, 0, Math.PI * 2);
        context.fillStyle = "#fff";
        context.fill();
        context.strokeStyle = "#d96e52";
        context.lineWidth = 2;
        context.stroke();
        context.fillStyle = "#7c8982";
        context.textAlign = "center";
        context.fillText(monthLabel(point.month), point.x, height - 11);
    });
    canvas.title = points.map(point => `${monthLabel(point.month)}: ${ugx(point.value)}`).join("\n");
}

function renderBars(containerId, entries, label) {
    const container = document.getElementById(containerId);
    if (!entries.length) {
        container.innerHTML = '<p class="loading-state">No records match these filters.</p>';
        return;
    }
    const top = entries.slice(0, 6);
    const max = Math.max(...top.map(entry => entry[1]), 1);
    container.innerHTML = top.map(([name, value]) => `
    <div class="bar-row" title="${safe(name)}: ${ugx(value)}">
      <span class="bar-label">${safe(name)}</span>
      <span class="bar-track"><span class="bar-fill" style="display:block;width:${Math.max(2, value / max * 100)}%"></span></span>
      <span class="bar-value">${compactUgx(value)}</span>
    </div>`).join("");
}

function renderStores(sourceRows) {
    const entries = aggregate(sourceRows.filter(row => row.store.startsWith("ST")), "store").slice(0, 8);
    const container = document.querySelector("#storeChart");
    const max = Math.max(1, ...entries.map(entry => entry[1]));
    if (!entries.length) {
        container.innerHTML = '<p class="loading-state">No physical-store sales match these filters.</p>';
        return;
    }
    container.innerHTML = entries.map(([store, value]) => {
        const info = rows.find(row => row.store === store);
        const selected = ui.store.value === store;
        return `<button type="button" class="store-item${selected ? " selected" : ""}" data-store="${safe(store)}" title="Filter to ${safe(info?.storeName || store)}">
      <span class="store-name">${safe(info?.storeName || store)}</span><span class="store-value">${compactUgx(value)}</span>
      <span class="store-track"><span class="store-fill" style="display:block;width:${Math.max(2, value / max * 100)}%"></span></span></button>`;
    }).join("");
    container.querySelectorAll(".store-item").forEach(button => button.addEventListener("click", () => {
        ui.store.value = button.dataset.store;
        page = 0;
        render();
    }));
}

function renderQuality() {
    const customer = data.quality.customerBefore;
    const customerAfter = data.quality.customerAfter;
    const product = data.quality.productBefore;
    const productAfter = data.quality.productAfter;
    const values = [
        { label: "Customer duplicate rows", before: customer.duplicate_rows_pct, after: customerAfter.duplicate_rows_pct, suffix: "%", better: "lower" },
        { label: "Product duplicate SKUs", before: product.duplicate_skus_pct, after: productAfter.duplicate_skus_pct, suffix: "%", better: "lower" },
        { label: "Customer format consistency", before: customer.consistency_pct, after: customerAfter.consistency_pct, suffix: "%", better: "higher" },
    ];
    document.querySelector("#qualityMetrics").innerHTML = values.map(item => {
        const width = item.better === "lower" ? 100 - item.after : item.after;
        return `<div class="quality-row"><span class="quality-name">${item.label}</span><span class="quality-value">${item.before}${item.suffix} → ${item.after}${item.suffix}</span><span class="quality-track"><span class="quality-fill" style="display:block;width:${Math.min(100, Math.max(2, width))}%"></span></span></div>`;
    }).join("");
}

function renderTable() {
    const pageCount = Math.max(1, Math.ceil(filtered.length / pageSize));
    page = Math.min(page, pageCount - 1);
    const visible = filtered.slice(page * pageSize, (page + 1) * pageSize);
    document.querySelector("#rowCount").textContent = `${number.format(filtered.length)} records`;
    document.querySelector("#pageLabel").textContent = filtered.length ? `Showing ${number.format(page * pageSize + 1)}–${number.format(Math.min((page + 1) * pageSize, filtered.length))} of ${number.format(filtered.length)}` : "Showing 0 records";
    document.querySelector("#prevPage").disabled = page === 0;
    document.querySelector("#nextPage").disabled = page >= pageCount - 1;
    ui.table.innerHTML = visible.map((row, index) => `
    <tr data-row="${page * pageSize + index}" tabindex="0" aria-label="Open transaction ${safe(row.customer)}">
      <td>${safe(row.date)}</td><td class="cell-id">${safe(row.customer)}</td>
      <td>${safe(row.storeName)} <span class="muted">· ${safe(row.district)}</span></td>
      <td>${safe(row.channel)}</td><td>${safe(row.category)}</td>
      <td class="${row.quantity < 0 ? "qty-return" : ""}">${number.format(row.quantity)}</td>
      <td class="cell-amount">${money.format(Math.round(row.amount))}</td>
    </tr>`).join("") || '<tr><td colspan="7" class="loading-state">No transactions match these filters.</td></tr>';
    ui.table.querySelectorAll("tr[data-row]").forEach(tr => {
        tr.addEventListener("click", () => showDetail(filtered[Number(tr.dataset.row)]));
        tr.addEventListener("keydown", event => { if (event.key === "Enter") showDetail(filtered[Number(tr.dataset.row)]); });
    });
}

function showDetail(row) {
    document.querySelector("#detailTitle").textContent = row.customer;
    const values = [
        ["Transaction date", row.date], ["Product", row.product], ["Store", row.storeName],
        ["District", row.district], ["Channel", row.channel], ["Category", row.category],
        ["Quantity", number.format(row.quantity)], ["Net sales", ugx(row.amount)],
    ];
    const details = document.querySelector("#detailList");
    details.replaceChildren(...values.flatMap(([key, value]) => {
        const term = document.createElement("dt");
        const description = document.createElement("dd");
        term.textContent = key;
        description.textContent = value;
        return [term, description];
    }));
    ui.dialog.showModal();
}

function downloadView() {
    const header = ["date", "customer_id", "product_id", "store_id", "store_name", "channel", "quantity", "amount_ugx", "district", "category"];
    const body = filtered.map(row => [row.date, row.customer, row.product, row.store, row.storeName, row.channel, row.quantity, row.amount, row.district, row.category]);
    const csv = [header, ...body].map(record => record.map(value => `"${String(value).replaceAll('"', '""')}"`).join(",")).join("\r\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "srg_demo_filtered_transactions.csv";
    link.click();
    URL.revokeObjectURL(url);
}

loadDashboard();
