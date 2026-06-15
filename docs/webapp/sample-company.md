# Apex Components

A private-equity portfolio company that manufactures industrial control parts and runs a mixed software estate inherited through acquisitions.

## Repositories

### customer-portal
- Language: Node
- Runtime: 20
- Package manager: npm
- Build system: npm scripts
- CI/CD: GitHub Actions
- Evidence: package.json includes Vite build and Vitest test scripts; package-lock.json is present.

### risk-api
- Language: Python
- Runtime: 3.11
- Package manager: poetry
- Build system: pyproject
- CI/CD: GitHub Actions
- Evidence: pyproject.toml declares Python 3.11 and pytest configuration; poetry.lock is present.

### billing-batch
- Language: Java
- Runtime: 17
- Package manager: maven
- Build system: maven
- CI/CD: Jenkins
- Evidence: pom.xml declares Maven compiler release 17; Jenkinsfile runs mvn test.

### legacy-ops-tools
- Language: Unknown
- Runtime: Unknown
- Package manager: Unknown
- Build system: legacy shell script
- CI/CD: Manual checklist
- Evidence: README.txt references manual releases; build.sh is present without structured metadata.

## Operating Notes

- The portal and API are closest to factory-ready because they already expose build and test signals.
- Billing batch needs Jenkins-to-blueprint mapping before full standardization.
- Legacy operations tooling should enter a human-reviewed assessment lane before automation.
