# Security Policy and Supply-Chain Audit

This document outlines the security practices, dependency management, and vulnerability assessment for the refactored Microservice System, as mandated by the **final.pdf** examination guidelines.

---

## 1. Supply-Chain Integrity & Dependency Pinning

To mitigate supply-chain attacks (such as dependency hijacking or breaking upstream changes), all third-party production and testing dependencies are strictly pinned to exact versions. 

The following primary packages have been vetted and locked in `requirements.txt`:
* **PyJWT==2.8.0**: Handles secure JSON Web Token generation and validation for the authentication microservice.
* **cryptography==42.0.5**: Provides the underlying cryptographic primitives for JWT signing and Strategy A (Encryption).
* **pytest-cov==4.1.0**: Assures test suite coverage tracking to enforce our quality gates.

> **Enforcement Notice:** Standard wildcard operators (`*`), optimistic tracking (`~=`), or caret requirements (`^`) are strictly prohibited in this repository to guarantee deterministic, reproducible CI/CD pipeline builds.

---

## 2. Mock Vulnerability Scanner Report

The codebase was subjected to a mock static application security testing (SAST) audit simulating a `bandit` scan. Below are the discovered vulnerabilities and their remediation status.

| Vulnerability ID | Severity | Component | Description | Resolution Status |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-001** | **High** | `legacy_auth.py` | Hardcoded JWT secret key discovered in the source code. | **Fixed** (Moved to environment variables) |
| **SEC-002** | **Medium** | `strategy.py` | Use of an insecure/weak cryptographic block cipher mode for Strategy A. | **Fixed** (Upgraded to AES-GCM via `cryptography`) |
| **SEC-003** | **Low** | `factory.py` | Standard `Exception` handling logging descriptive system errors to stdout. | **Fixed** (Sanitized error responses to prevent info leakage) |

---

## 3. Vulnerability Mitigation Details

### SEC-001: Hardcoded Secrets Mitigation
* **Risk:** Exposure of token-signing keys in source control allows attackers to forge valid JWTs and bypass service discovery access controls.
* **Remediation:** The hardcoded string was deleted. The system now binds secrets dynamically at runtime using secure environment variables.

### SEC-002: Insecure Cryptographic Strategy
* **Risk:** Inadequate encryption schemes applied to the data stream `[78, 82, 91, 65, 40, 99, 88]` could allow deterministic pattern analysis.
* **Remediation:** Strategy A was refactored to employ authenticated encryption (AES) using the specified key `004F`, padded to meet standard cryptographic lengths.

---

## 4. Automated Security Gates

Security compliance is continuously enforced. Every push to the `final-exam-submission` branch triggers a GitHub Actions workflow that executes:
1. **Bandit:** Automatically scans python files for known security flaws (rejecting any code introducing High/Medium risks).
2. **Flake8:** Audits code style consistency to prevent obfuscated or malicious code structures.