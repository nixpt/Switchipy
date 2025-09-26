# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Switchipy, please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. Email security details to: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Considerations

Switchipy handles system theme switching and may require elevated permissions. Security considerations include:

- **Theme switching**: Uses xfconf-query which may require system access
- **Hotkey registration**: Global hotkeys require system-level access
- **File system access**: Reads/writes configuration files
- **Desktop integration**: Creates desktop files and autostart entries

## Best Practices

- Run Switchipy with minimal required permissions
- Review configuration files before use
- Keep the application updated
- Use official installation methods

## Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Resolution**: Depends on severity and complexity

Thank you for helping keep Switchipy secure!
