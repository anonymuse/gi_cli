const sampleMarkdown = `# Medical Records Processor

A healthcare operations company with mixed repository maturity, CI conventions, and modernization readiness.

## Repositories

### custom-report
- Language: Node
- Runtime: 20
- Package manager: npm
- Build system: npm scripts
- CI/CD: GitHub Actions
- Evidence: package.json includes Vite build and Vitest scripts; package-lock.json is present.

### risk-api
- Language: Python
- Runtime: 3.11
- Package manager: poetry
- Build system: pyproject
- CI/CD: GitHub Actions
- Evidence: pyproject.toml has pytest hints; poetry.lock is present.

### billing-batch
- Language: Java
- Runtime: 17
- Package manager: maven
- Build system: maven
- CI/CD: Jenkins
- Evidence: pom.xml declares Java 17; Jenkinsfile runs mvn test.

### legacy-ops-tool
- Language: Unknown
- Runtime: Unknown
- Package manager: Unknown
- Build system: legacy shell script
- CI/CD: Manual checklist
- Evidence: README.txt references manual releases; build.sh has no structured metadata.
`;

const blueprintByLanguage = {
  node: 'Node.js Service CI Blueprint',
  python: 'Python Service CI Blueprint',
  java: 'JVM Service CI Blueprint',
  unknown: 'Legacy Repository Assessment Blueprint',
};

const repoDetails = {
  'custom-report': {
    title: 'Custom Report',
    description: 'Generates medical-record summary reports for care coordinators. The repository is ready for agentic acceleration because it has reproducible package metadata, automated tests, and a modern Node build path.',
    enhancement: 'Create a LangGraph report QA workflow that drafts synthetic report fixtures, runs Vitest, validates accessibility of rendered report components, and opens a pull request with evidence attached.',
    pseudocode: `workflow CustomReportQA:
  changedFiles = git.diff()
  if changedFiles.include("report templates"):
    fixtures = agent.generateSyntheticRecords(schema="HIPAA-safe")
    run("npm test -- --runInBand", fixtures)
    eval("report_completeness", threshold=0.95)
    agent.openPullRequest(summary, evidence)`
  },
  'risk-api': {
    title: 'Risk API',
    description: 'Scores patient and operational risk through a Python API. Strong Python project metadata and pytest signals make it a good candidate for an agent-assisted API safety and regression workflow.',
    enhancement: 'Add a custom risk-contract agent that proposes endpoint changes, generates pytest coverage for edge cases, and runs an eval suite that checks calibration drift and response-contract compatibility.',
    pseudocode: `agent RiskContractAgent:
  spec = load_openapi()
  tests = create_pytest_cases(spec, edgeCases=["missing data", "high acuity"])
  run("poetry run pytest")
  eval("risk_score_calibration", goldenSet="clinical-risk-fixtures")
  block_merge_if(contract_breaks or drift > 0.02)`
  },
  'billing-batch': {
    title: 'Billing Batch',
    description: 'Runs scheduled billing reconciliation and claim-preparation jobs. The Maven and Jenkins foundation supports a controlled agentic workflow for batch-job refactors and test generation.',
    enhancement: 'Build a LangChain modernization chain that reads failing Jenkins stages, proposes narrow Java changes, generates Maven tests for billing edge cases, and routes high-risk claim changes for human review.',
    pseudocode: `chain BillingBatchFixer:
  logs = jenkins.getLastFailedBuild()
  hypothesis = agent.explainFailure(logs)
  patch = agent.proposeJavaPatch(scope="billing reconciliation")
  run("mvn test")
  if touchesClaimRules(patch): requestHumanApproval()
  else createPullRequest(patch, testEvidence)`
  },
  'legacy-ops-tool': {
    title: 'Legacy Ops Tool',
    description: 'Contains manual release scripts and sparse metadata, so it should be stabilized before broad automation. The best next step is to let agents inventory behavior while humans keep release authority.',
    enhancement: 'Use an agentic remediation workflow that maps shell-script behavior, adds characterization tests, extracts configuration into typed manifests, and only then proposes CI jobs that replace checklist steps.',
    pseudocode: `workflow LegacyOpsRemediation:
  scripts = agent.inventoryShellScripts()
  behaviorMap = agent.traceInputsOutputs(scripts)
  tests = agent.writeCharacterizationTests(behaviorMap)
  run("./build.sh --dry-run")
  createBacklog(items=["typed config", "CI wrapper", "release guardrails"])
  requireHumanReviewFor(allPatches)`
  },
};

const markdownInput = document.querySelector('#markdownInput');
const fileInput = document.querySelector('#fileInput');
const results = document.querySelector('#results');
const detailRoot = document.querySelector('#repoDetail');
const activeMarkdownStorageKey = 'factoryFitProfiler.activeMarkdown';

if (document.querySelector('#loadSample')) {
  document.querySelector('#loadSample').addEventListener('click', () => {
    markdownInput.value = sampleMarkdown;
    renderProfile(sampleMarkdown);
  });

  document.querySelector('#analyze').addEventListener('click', () => renderProfile(markdownInput.value));

  fileInput.addEventListener('change', async (event) => {
    const [file] = event.target.files;
    if (!file) return;
    markdownInput.value = await file.text();
    renderProfile(markdownInput.value);
  });

  markdownInput.value = getActiveMarkdown();
  renderProfile(markdownInput.value);
}

if (detailRoot) renderRepoDetail();

function parseCompany(markdown) {
  const lines = markdown.split(/\r?\n/);
  const companyName = (lines.find((line) => line.startsWith('# ')) || '# Untitled Company').replace(/^#\s+/, '').trim();
  const repos = [];
  let current = null;

  for (const line of lines) {
    const repoMatch = line.match(/^###\s+(.+)/);
    if (repoMatch) {
      current = { name: repoMatch[1].trim(), facts: {}, evidence: [] };
      repos.push(current);
      continue;
    }
    if (!current) continue;
    const factMatch = line.match(/^-\s*([^:]+):\s*(.+)$/);
    if (!factMatch) continue;
    const key = factMatch[1].trim().toLowerCase();
    const value = factMatch[2].trim();
    if (key === 'evidence') current.evidence.push(value);
    else current.facts[key] = value;
  }
  return { companyName, repos };
}

function classify(repo) {
  const language = normalize(repo.facts.language || 'unknown');
  const ci = repo.facts['ci/cd'] || repo.facts.ci || 'No CI/CD signal';
  const buildSystem = repo.facts['build system'] || 'unknown';
  const blueprint = blueprintByLanguage[language] || blueprintByLanguage.unknown;
  const readySignals = [language !== 'unknown', buildSystem !== 'unknown', !/manual|none|no ci/i.test(ci), repo.evidence.length > 0];
  const score = Math.round((readySignals.filter(Boolean).length / readySignals.length) * 100);
  const lane = score >= 75 ? 'Factory-ready' : score >= 50 ? 'Retrofit first' : 'Assess before automation';
  return { language, ci, buildSystem, blueprint, score, lane };
}

function normalize(value) {
  const normalized = String(value).toLowerCase();
  if (normalized.includes('node') || normalized.includes('javascript') || normalized.includes('typescript')) return 'node';
  if (normalized.includes('python')) return 'python';
  if (normalized.includes('java')) return 'java';
  return 'unknown';
}

function renderProfile(markdown) {
  persistActiveMarkdown(markdown);
  const company = parseCompany(markdown);
  if (!company.repos.length) {
    results.innerHTML = '<div class="empty">Add markdown with <code>### repository-name</code> sections and facts like <code>- Language: Python</code>.</div>';
    return;
  }

  const profiled = company.repos.map((repo) => ({ ...repo, profile: classify(repo) }));
  const factoryReady = profiled.filter((repo) => repo.profile.lane === 'Factory-ready').length;
  const retrofit = profiled.filter((repo) => repo.profile.lane === 'Retrofit first').length;
  const assess = profiled.length - factoryReady - retrofit;

  results.innerHTML = `
    <h2>${escapeHtml(company.companyName)}</h2>
    <div class="stats" aria-label="Profile summary">
      <div class="stat"><strong>${profiled.length}</strong><span>Repositories</span></div>
      <div class="stat"><strong>${factoryReady}</strong><span>Factory-ready</span></div>
      <div class="stat"><strong>${retrofit}</strong><span>Retrofit first</span></div>
      <div class="stat"><strong>${assess}</strong><span>Assess first</span></div>
    </div>
    <div class="path">Assess → Onboard → Retrofit → Automate → Govern → Scale</div>
    <div class="repo-list">
      ${profiled.map(renderRepo).join('')}
    </div>`;
}

function renderRepo(repo) {
  const { profile } = repo;
  const badgeClass = profile.score >= 75 ? 'good' : profile.score >= 50 ? 'warn' : 'risk';
  const detail = getRepoDetail(repo.name);
  const enhancementLabel = profile.score === 50 ? 'Maturity enhancement recommendation' : 'Agentic enhancement';
  return `<a class="repo-link" href="./repo.html?repo=${encodeURIComponent(repo.name)}" aria-label="Open ${escapeHtml(detail.title)} details"><article class="repo">
    <h3>${escapeHtml(detail.title)} <span class="badge ${badgeClass}">${profile.score}% ready</span></h3>
    <div class="meta">
      <span class="badge">${escapeHtml(profile.language)}</span>
      <span class="badge">${escapeHtml(profile.buildSystem)}</span>
      <span class="badge">${escapeHtml(profile.ci)}</span>
    </div>
    <p><strong>Recommended lane:</strong> ${escapeHtml(profile.lane)}</p>
    <p><strong>Recommended Lang blueprint:</strong> ${escapeHtml(profile.blueprint)}</p>
    <p><strong>Evidence:</strong> ${escapeHtml(repo.evidence.join(' ') || 'No explicit evidence supplied.')}</p>
    <p><strong>${enhancementLabel}:</strong> ${escapeHtml(detail.enhancement)}</p>
  </article></a>`;
}

function renderRepoDetail() {
  const repoName = new URLSearchParams(window.location.search).get('repo');
  const company = parseCompany(getActiveMarkdown());
  const repo = company.repos.find((item) => item.name === repoName) || company.repos[0];

  if (!repo) {
    detailRoot.innerHTML = `<section class="panel detail-card">
      <a class="back-link" href="./index.html">← Back to company profile</a>
      <div class="empty">No repository sections were found in the active markdown profile.</div>
    </section>`;
    return;
  }

  const profile = classify(repo);
  const detail = getRepoDetail(repo.name);
  const badgeClass = profile.score >= 75 ? 'good' : profile.score >= 50 ? 'warn' : 'risk';
  detailRoot.innerHTML = `<section class="panel detail-card">
    <a class="back-link" href="./index.html">← Back to company profile</a>
    <h2>${escapeHtml(detail.title)}</h2>
    <span class="badge ${badgeClass}">${profile.score}% ready</span>
    <p class="lede small">${escapeHtml(detail.description)}</p>
    <div class="detail-grid">
      <div><h3>Company</h3><p>${escapeHtml(company.companyName)}</p></div>
      <div><h3>Recommended lane</h3><p>${escapeHtml(profile.lane)}</p></div>
      <div><h3>Recommended Lang blueprint</h3><p>${escapeHtml(profile.blueprint)}</p></div>
      <div><h3>Evidence</h3><p>${escapeHtml(repo.evidence.join(' ') || 'No explicit evidence supplied.')}</p></div>
      <div><h3>${profile.score === 50 ? 'Maturity enhancement recommendation' : 'Agentic enhancement'}</h3><p>${escapeHtml(detail.enhancement)}</p></div>
    </div>
    <h3>Pseudocode snippet</h3>
    <pre><code>${escapeHtml(detail.pseudocode)}</code></pre>
  </section>`;
}

function persistActiveMarkdown(markdown) {
  try {
    window.sessionStorage.setItem(activeMarkdownStorageKey, markdown);
  } catch (error) {
    // The detail page can still fall back to the bundled sample if storage is unavailable.
  }
}

function getActiveMarkdown() {
  try {
    return window.sessionStorage.getItem(activeMarkdownStorageKey) || sampleMarkdown;
  } catch (error) {
    return sampleMarkdown;
  }
}

function getRepoDetail(repoName) {
  return repoDetails[repoName] || { title: repoName, description: 'Repository detail.', enhancement: 'Create an agentic workflow tailored to the repository maturity signals.', pseudocode: 'agent.run()' };
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
}
