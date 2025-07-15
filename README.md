# DevSecOps Portfolio Project: From Vulnerable to Secure

**Author:** Craig McCart

*   [LinkedIn](https://www.linkedin.com/in/your-profile-url) | [GitHub](https://github.com/your-github-username)


## 1. Introduction

This project demonstrates a complete DevSecOps lifecycle, showcasing the ability to **identify, remediate, and verify** the security of a web application and its infrastructure.

It tells a story in two parts:
*   **Part 1: The Vulnerable Application (`vulnerable_app.py`)**: An intentionally vulnerable Python Flask application designed to be caught by our security scanners.
*   **Part 2: The Secure Refactor (`app.py`)**: A remediated version of the application where all identified OWASP Top 10 vulnerabilities have been fixed using secure coding best practices.

The goal is to prove the effectiveness of a "shift-left" security approach within a modern CI/CD pipeline using GitHub Actions.

## 2. The DevSecOps Pipeline

This project uses GitHub Actions to create two distinct security pipelines, defined in `.github/workflows/`.

### `main-ci.yml` - The Secure Pipeline

This is the primary CI pipeline that runs on every push and pull request to the `main` branch. It scans the **secure** application (`app.py`), its dependencies (`requirements.txt`), and the infrastructure code (`main.tf`).

This pipeline is **expected to pass**, demonstrating that the remediated code meets our security standards. It includes three key jobs:

1.  **`sast-scan`**: Uses **GitHub CodeQL** to perform Static Application Security Testing on the secure Python code, ignoring the vulnerable file.
2.  **`sca-scan`**: Uses **Trivy** to perform Software Composition Analysis on the `requirements.txt` file, checking for dependencies with known vulnerabilities.
3.  **`iac-scan`**: Uses **Trivy** to scan the Terraform (`main.tf`) configuration for any infrastructure misconfigurations.

### `vulnerability-scan.yml` - The Vulnerability Demonstration Pipeline

This pipeline exists to prove that our security tools are working correctly. It is triggered **manually** (via the GitHub Actions UI) and runs against the **insecure** code.

This pipeline is **expected to show failures and vulnerabilities**. It includes two jobs:

1.  **`sast-scan-vulnerable`**: Runs **GitHub CodeQL** specifically on `vulnerable_app.py` to highlight the numerous code-level vulnerabilities.
2.  **`sca-scan-vulnerable`**: Runs **Trivy** on `vulnerable-requirements.txt`, which contains packages with known security issues.

## 3. Project Structure

```
.
├── .github/
│   ├── codeql/                 # CodeQL configuration files
│   │   ├── codeql-config.yml       # -> Ignores vulnerable_app.py
│   │   └── vulnerable-codeql-config.yml # -> Scans only vulnerable_app.py
│   └── workflows/
│       ├── main-ci.yml             # ✅ Main CI pipeline for secure code (should pass)
│       └── vulnerability-scan.yml  # ❌ Manual workflow to show scanners finding issues (should fail/report issues)
├── app.py                      # ✅ The new, secure, and remediated Flask application.
├── vulnerable_app.py           # ❌ The original, intentionally vulnerable Flask application.
├── requirements.txt            # ✅ Dependencies for the secure application.
├── vulnerable-requirements.txt # ❌ Dependencies for the vulnerable application.
├── main.tf                     # 🌎 Terraform IaC file, scanned by the main CI pipeline.
└── README.md                   # 📄 This file.
```

## 4. Conclusion

By structuring the project this way, it serves as a powerful portfolio piece that doesn't just show a final, secure product, but demonstrates a deep understanding of the entire DevSecOps process: from an insecure baseline, through automated detection, to a final, remediated, and continuously verified secure state. It proves not just *what* to do, but *why* it's important.

## 5. Key Learnings & Future Improvements

*   **SAST in Practice**: Implementing CodeQL highlighted the importance of custom configuration (`codeql-config.yml`) to precisely target or ignore specific parts of a codebase, which is critical in a monorepo.
*   **SCA for Source vs. Image**: Shifting the SCA scan from a Docker image to a `requirements.txt` file provides faster feedback and makes it easier to pinpoint the exact source of a dependency vulnerability.
*   **The Narrative is Key**: A portfolio project is more effective when it tells a story. Demonstrating both the "problem" (`vulnerable_app.py`) and the "solution" (`app.py`) is more powerful than just showing a finished product.

**Future Work:**
*   Integrate a secret scanning tool (e.g., Gittyleaks) into the pipeline.
*   Expand the IaC security to include checks against custom policies using a tool like Checkov.