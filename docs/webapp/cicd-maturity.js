const catalogStatus = document.querySelector('#catalogStatus');
const summaryStats = document.querySelector('#summaryStats');
const maturityDimensions = document.querySelector('#maturityDimensions');
const agentSuggestions = document.querySelector('#agentSuggestions');
const recordCount = document.querySelector('#recordCount');
const recordsTable = document.querySelector('#recordsTable');

init();

async function init() {
  try {
    const response = await fetch('./jenkins-build-catalog.json');
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    renderCatalog(await response.json());
  } catch (error) {
    catalogStatus.textContent = `Unable to load mocked Jenkins catalog. Run this demo from a static web server. ${error.message}`;
  }
}

function renderCatalog(catalog) {
  const records = catalog.buildRecords || [];
  const metrics = calculateMetrics(records);
  catalogStatus.innerHTML = `<strong>${escapeHtml(catalog.summary.company)}</strong><br>${escapeHtml(catalog.summary.source)}`;
  renderSummary(metrics, catalog.summary);
  renderDimensions(metrics, catalog.maturityDimensions || []);
  renderSuggestions(metrics);
  renderCharts(records);
  renderRecords(records, metrics);
}

function calculateMetrics(records) {
  const count = records.length || 1;
  const successes = records.filter((record) => record.status === 'success').length;
  const failures = records.filter((record) => record.status === 'failed').length;
  const deployable = records.filter((record) => record.deployableArtifact).length;
  const scans = records.filter((record) => record.securityScan).length;
  const sboms = records.filter((record) => record.sbomGenerated).length;
  const signed = records.filter((record) => record.artifactSigned).length;
  const pipelineAsCode = records.filter((record) => record.maturitySignals?.pipelineAsCode).length;
  const qualityGate = records.filter((record) => record.maturitySignals?.qualityGate).length;
  const traceLinked = records.filter((record) => record.maturitySignals?.changeTraceLinked).length;
  const progressive = records.filter((record) => record.maturitySignals?.progressiveDeliveryReady).length;
  const avgDuration = average(records, 'durationMinutes');
  const avgQueue = average(records, 'queueMinutes');
  const avgLeadTime = average(records, 'leadTimeMinutes');
  const avgFlakeRate = average(records, 'flakeRatePercent');
  return {
    count,
    successRate: pct(successes, count),
    failureRate: pct(failures, count),
    deployableRate: pct(deployable, count),
    scanRate: pct(scans, count),
    sbomRate: pct(sboms, count),
    signedRate: pct(signed, count),
    pipelineAsCodeRate: pct(pipelineAsCode, count),
    qualityGateRate: pct(qualityGate, count),
    traceRate: pct(traceLinked, count),
    progressiveRate: pct(progressive, count),
    avgDuration,
    avgQueue,
    avgLeadTime,
    avgFlakeRate,
  };
}

function renderSummary(metrics, summary) {
  summaryStats.innerHTML = [
    stat(summary.recordCount, 'Daily builds'),
    stat(`${metrics.successRate}%`, 'Success rate'),
    stat(`${metrics.avgQueue}m`, 'Avg queue time'),
    stat(`${metrics.deployableRate}%`, 'Deployable artifacts'),
    stat(`${metrics.scanRate}%`, 'Security scanned'),
    stat(`${metrics.sbomRate}%`, 'SBOM coverage'),
  ].join('');
}

function renderDimensions(metrics, dimensions) {
  const scores = {
    pipeline_as_code: metrics.pipelineAsCodeRate,
    build_health: Math.max(0, Math.round(metrics.successRate - metrics.avgFlakeRate - metrics.avgQueue / 3)),
    quality_security: Math.round((metrics.qualityGateRate + metrics.scanRate + metrics.sbomRate + metrics.signedRate) / 4),
    flow_efficiency: Math.max(0, Math.round((metrics.deployableRate + metrics.progressiveRate + Math.max(0, 100 - metrics.avgLeadTime / 4)) / 3)),
    agentic_readiness: Math.round((metrics.traceRate + metrics.pipelineAsCodeRate + metrics.qualityGateRate) / 3),
  };
  maturityDimensions.innerHTML = dimensions.map((dimension) => {
    const score = scores[dimension.id] ?? 0;
    return `<article class="dimension-card">
      <div class="score-ring ${scoreClass(score)}">${score}</div>
      <div><h3>${escapeHtml(dimension.label)}</h3><p>${escapeHtml(dimension.description)}</p><p><strong>${maturityLabel(score)}</strong></p></div>
    </article>`;
  }).join('');
}

function renderSuggestions(metrics) {
  const suggestions = [
    ['Build intelligence agent', `Summarize failed and unstable Jenkins runs, cluster failures by team and language, and create daily modernization briefs. Prioritize the ${metrics.failureRate}% failure rate and ${metrics.avgFlakeRate}% average flake rate.`],
    ['Pipeline-as-code migration copilot', `Detect non-standard jobs, generate Jenkinsfile/shared-library pull requests, and require human approval before changing build logic. Current pipeline-as-code signal is ${metrics.pipelineAsCodeRate}%.`],
    ['Quality gate assistant', `Recommend missing test, coverage, SAST, SBOM, and signing controls before repositories enter factory automation. Security scan coverage is ${metrics.scanRate}% and artifact signing is ${metrics.signedRate}%.`],
    ['Flow and queue optimizer', `Find overloaded agents, long queues, and slow jobs, then suggest ephemeral runners or caching changes. Average queue time is ${metrics.avgQueue} minutes.`],
    ['Release readiness agent', `Promote only trace-linked, scanned, signed, deployable artifacts into progressive delivery experiments. Current progressive-delivery readiness is ${metrics.progressiveRate}%.`],
  ];
  agentSuggestions.innerHTML = suggestions.map(([title, body]) => `<article class="suggestion"><h3>${title}</h3><p>${body}</p></article>`).join('');
}

function renderCharts(records) {
  renderBarChart('#teamChart', countBy(records, 'team'));
  renderBarChart('#languageChart', countBy(records, 'language'));
  renderBarChart('#statusChart', countBy(records, 'status'));
  renderBarChart('#agentChart', countBy(records, 'agentLabel'));
}

function renderRecords(records) {
  const risky = [...records].sort((a, b) => (b.queueMinutes + b.durationMinutes + b.failedTests * 3) - (a.queueMinutes + a.durationMinutes + a.failedTests * 3)).slice(0, 12);
  recordCount.textContent = `${records.length} total records`;
  recordsTable.innerHTML = `<thead><tr><th>Build</th><th>Team</th><th>Job</th><th>Status</th><th>Duration</th><th>Queue</th><th>Signals</th></tr></thead><tbody>${risky.map((record) => `<tr>
    <td>${escapeHtml(record.buildId)}</td><td>${escapeHtml(record.team)}</td><td>${escapeHtml(record.jobName)}</td>
    <td><span class="badge ${record.status === 'success' ? 'good' : 'risk'}">${escapeHtml(record.status)}</span></td>
    <td>${record.durationMinutes}m</td><td>${record.queueMinutes}m</td>
    <td>${signalBadges(record)}</td>
  </tr>`).join('')}</tbody>`;
}

function renderBarChart(selector, counts) {
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  const max = Math.max(...entries.map(([, value]) => value), 1);
  document.querySelector(selector).innerHTML = entries.map(([label, value]) => `<div class="bar-row"><span>${escapeHtml(label)}</span><div class="bar-track"><div class="bar-fill" style="width:${(value / max) * 100}%"></div></div><strong>${value}</strong></div>`).join('');
}

function signalBadges(record) {
  return [record.securityScan && 'scan', record.sbomGenerated && 'sbom', record.artifactSigned && 'signed', record.deployableArtifact && 'deployable'].filter(Boolean).map((signal) => `<span class="badge">${signal}</span>`).join(' ');
}

function countBy(records, key) { return records.reduce((acc, record) => ({ ...acc, [record[key]]: (acc[record[key]] || 0) + 1 }), {}); }
function average(records, key) { return Math.round(records.reduce((sum, record) => sum + (Number(record[key]) || 0), 0) / (records.length || 1)); }
function pct(part, total) { return Math.round((part / (total || 1)) * 100); }
function stat(value, label) { return `<div class="stat"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`; }
function scoreClass(score) { return score >= 75 ? 'good' : score >= 50 ? 'warn' : 'risk'; }
function maturityLabel(score) { return score >= 75 ? 'Scaling practice' : score >= 50 ? 'Standardizing practice' : 'Modernization opportunity'; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char])); }
