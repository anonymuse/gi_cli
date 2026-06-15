const sampleMarkdown = `# Synthetic Portfolio Company

A portfolio company with mixed repository maturity, CI conventions, and modernization readiness.

## Repositories

### customer-portal
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

### legacy-ops-tools
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

const markdownInput = document.querySelector('#markdownInput');
const fileInput = document.querySelector('#fileInput');
const results = document.querySelector('#results');

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
  return `<article class="repo">
    <h3>${escapeHtml(repo.name)} <span class="badge ${badgeClass}">${profile.score}% ready</span></h3>
    <div class="meta">
      <span class="badge">${escapeHtml(profile.language)}</span>
      <span class="badge">${escapeHtml(profile.buildSystem)}</span>
      <span class="badge">${escapeHtml(profile.ci)}</span>
    </div>
    <p><strong>Recommended lane:</strong> ${escapeHtml(profile.lane)}</p>
    <p><strong>Blueprint:</strong> ${escapeHtml(profile.blueprint)}</p>
    <p><strong>Evidence:</strong> ${escapeHtml(repo.evidence.join(' ') || 'No explicit evidence supplied.')}</p>
  </article>`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
}

markdownInput.value = sampleMarkdown;
renderProfile(sampleMarkdown);
