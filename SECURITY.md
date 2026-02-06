# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please email Muhammad Farooq directly at **mfarooqshafee333@gmail.com** instead of using the public issue tracker.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge your email within 48 hours and provide an update on our progress within 5 business days.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |

## Security Best Practices

When using this project:

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Environment Variables**
   - Never commit `.env` files with secrets
   - Use `.env.example` as template
   - Store credentials securely

3. **API Keys & Tokens**
   - Don't hardcode API keys
   - Use environment variables or configuration files
   - Rotate keys regularly

4. **Data Security**
   - Ensure data at rest encryption in production
   - Use HTTPS/TLS for data in transit
   - Follow GDPR and data privacy regulations

5. **Code Review**
   - All changes go through peer review
   - Security-focused code review checklist

6. **Dependency Management**
   - Regularly update dependencies
   - Run `safety check` to check for known vulnerabilities
   - Monitor security advisories

## Vulnerability Disclosure Timeline

- **T+0h**: Initial report received and acknowledged
- **T+24h**: Vulnerability assessed and confirmed
- **T+72h**: Fix development and testing begins
- **T+7d**: Patch released (if approved)
- **T+14d**: Full disclosure

## Security Scanning

This project uses:
- GitHub Actions for automated testing
- Bandit for security linting
- Safety for dependency vulnerability checks

## Compliance

This project follows security best practices for:
- **Python**: [Python Security Guidelines](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- **ML Models**: [AI/ML Security Guidelines](https://www.nist.gov/publications/outline-risk-management-framework)
- **Data Handling**: [GDPR](https://gdpr-info.eu/) and privacy regulations

## Questions?

For security questions, contact Muhammad Farooq at mfarooqshafee333@gmail.com
