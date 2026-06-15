# Contoso

Contoso is a synthetic portfolio-company demo profile for live Factory Fit Profiler walkthroughs. It is designed to be downloaded from the repository and uploaded into the static web demo as a richer markdown data set with realistic engineering signals, modernization constraints, and agentic SDLC opportunities.

## Demo Scenario

- Industry: Multi-channel equipment services and field operations
- Operating model: Acquisition-led platform with shared corporate technology and semi-autonomous business-unit engineering teams
- Demo goal: Show how a mixed repository estate can be triaged into factory-ready, retrofit-first, and assessment-first lanes without needing live DevOps integrations
- Executive question: Which teams can safely adopt agentic coding workflows now, and which teams need platform remediation first?

## Company Signals

- Engineering teams: 7 product squads, 2 platform squads, 1 data enablement squad
- Primary delivery platforms: GitHub Enterprise, Azure DevOps, Jenkins, ServiceNow change calendar
- Regulated workflows: Customer billing, technician safety checks, parts warranty adjudication
- Shared standards target: Reproducible builds, automated tests, policy-as-code checks, and evidence-backed pull requests

## Repositories

### customer-mobile-app
- Business capability: Technician and customer self-service mobile experience
- Owner: Digital Experience squad
- Language: TypeScript / React Native
- Runtime: Node 20
- Package manager: pnpm
- Build system: Expo Application Services with npm scripts
- CI/CD: GitHub Actions
- Test signal: Jest unit tests, Detox smoke tests, and accessibility linting
- Deployment target: iOS, Android, and staged internal distribution
- Data sensitivity: Customer contact data and appointment notes
- Agentic candidate: High
- Suggested agent workflow: Generate mobile regression tests from changed screens, run accessibility checks, and prepare release notes with linked evidence.
- Evidence: package.json declares test, lint, and build scripts; pnpm-lock.yaml is present.
- Evidence: .github/workflows/mobile-ci.yml runs lint, Jest, and Expo preview builds on pull requests.

### pricing-api
- Business capability: Contract pricing, discount eligibility, and quote calculation
- Owner: Revenue Systems squad
- Language: Python
- Runtime: 3.11
- Package manager: poetry
- Build system: pyproject
- CI/CD: GitHub Actions
- Test signal: pytest, contract tests, and OpenAPI schema validation
- Deployment target: Containerized service on Kubernetes
- Data sensitivity: Customer pricing terms and margin rules
- Agentic candidate: High with policy gates
- Suggested agent workflow: Propose narrow pricing-rule changes, generate pytest parameter coverage, validate OpenAPI compatibility, and require human approval for margin-impacting logic.
- Evidence: pyproject.toml declares Python 3.11, pytest configuration, ruff, and mypy.
- Evidence: openapi.yaml and poetry.lock are present; GitHub Actions publishes test artifacts.

### parts-fulfillment-worker
- Business capability: Warehouse inventory reservation and parts shipment orchestration
- Owner: Supply Chain Automation squad
- Language: Java
- Runtime: 17
- Package manager: maven
- Build system: maven
- CI/CD: Jenkins
- Test signal: JUnit integration tests and Testcontainers smoke tests
- Deployment target: Kubernetes CronJob and message-driven workers
- Data sensitivity: Supplier identifiers, inventory locations, and shipment status
- Agentic candidate: Medium
- Suggested agent workflow: Read failed Jenkins stages, draft bounded Java fixes, add JUnit coverage for inventory edge cases, and route message-schema changes to platform review.
- Evidence: pom.xml declares Maven compiler release 17 and JUnit dependencies.
- Evidence: Jenkinsfile runs mvn verify and archives Surefire reports, but deployment promotion remains manually approved.

### data-quality-dashboard
- Business capability: Executive visibility into customer, billing, and work-order data quality
- Owner: Data Enablement squad
- Language: Node / TypeScript
- Runtime: 20
- Package manager: npm
- Build system: npm scripts
- CI/CD: Azure DevOps Pipelines
- Test signal: Vitest component tests and SQL snapshot checks
- Deployment target: Static dashboard hosted behind SSO
- Data sensitivity: Aggregated operational metrics with drill-down links
- Agentic candidate: Medium
- Suggested agent workflow: Generate missing data-quality checks from metric definitions, run Vitest, compare SQL snapshots, and attach dashboard screenshots to pull requests.
- Evidence: package.json includes build, test, and lint scripts; package-lock.json is present.
- Evidence: azure-pipelines.yml runs npm ci, npm test, and npm run build but lacks reusable governance templates.

### warranty-rules-engine
- Business capability: Warranty eligibility, exception routing, and claim adjudication
- Owner: Warranty Modernization squad
- Language: C# / .NET
- Runtime: .NET 8
- Package manager: NuGet
- Build system: dotnet
- CI/CD: Azure DevOps Pipelines
- Test signal: xUnit tests and golden claim scenarios
- Deployment target: Azure App Service
- Data sensitivity: Claim history, customer equipment records, and exception rationale
- Agentic candidate: Medium with domain review
- Suggested agent workflow: Generate golden-scenario tests for changed warranty rules, explain decision-table diffs, and require domain-owner approval before merge.
- Evidence: Contoso.Warranty.sln and global.json pin the .NET SDK; tests are present under tests/Contoso.Warranty.Tests.
- Evidence: azure-pipelines.yml runs dotnet test but does not yet publish structured decision evidence.

### erp-nightly-sync
- Business capability: Nightly ERP synchronization for customers, invoices, and parts masters
- Owner: Enterprise Applications squad
- Language: Unknown
- Runtime: Unknown
- Package manager: Unknown
- Build system: legacy shell script
- CI/CD: Manual checklist
- Test signal: Production reconciliation spreadsheet and manual smoke check
- Deployment target: On-premises scheduler
- Data sensitivity: Customer master data, invoice records, and financial reconciliation outputs
- Agentic candidate: Low until characterized
- Suggested agent workflow: Inventory shell scripts, map inputs and outputs, create characterization tests around sample extracts, and keep humans in control of production scheduling.
- Evidence: README.txt documents a manual release window and rollback contact list.
- Evidence: sync.sh and transform.awk are present, but no lockfile, test harness, or CI configuration exists.

## Readiness Narrative

- Factory-ready candidates: customer-mobile-app and pricing-api already have modern runtimes, reproducible dependencies, automated tests, and pull-request CI evidence.
- Retrofit-first candidates: parts-fulfillment-worker, data-quality-dashboard, and warranty-rules-engine have enough structure for targeted agent assistance but need governance templates, richer evidence capture, or domain-review gates.
- Assess-first candidates: erp-nightly-sync should be characterized before automation because it has unknown runtime assumptions, manual release controls, and financial-data blast radius.

## Suggested Demo Flow

1. Download this markdown file from the repository.
2. Open the static Factory Fit Profiler company profile demo.
3. Use the upload control to load this file into the browser-only analyzer.
4. Highlight how repository facts, repeated evidence lines, and operating notes produce a more credible readiness conversation.
5. Use the recommendations to discuss where agentic coding can start immediately versus where modernization prerequisites are required.

## Operating Notes

- Treat the profile as synthetic demo data; do not map it to a real Contoso tenant or production environment.
- The markdown intentionally includes more fields than the browser parser requires so presenters can narrate business context, ownership, data sensitivity, and governance considerations.
- Repeated Evidence lines are supported by the profile parser and make the resulting repository cards more compelling during live uploads.
- Unknown language, runtime, package-manager, and CI/CD signals are intentional because they demonstrate the assessment lane for legacy repositories.
