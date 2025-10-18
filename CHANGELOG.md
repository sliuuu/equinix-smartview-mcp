# Changelog

All notable changes to the Equinix SmartView MCP Server will be documented in this file.

## [2.0.0] - 2025-10-18

### 🚨 BREAKING CHANGES

#### Changed Authentication Method
- **REMOVED**: Simple API key authentication (`EQUINIX_SMARTVIEW_API_KEY`)
- **ADDED**: OAuth 2.0 client credentials flow
- **REQUIRED**: `EQUINIX_CLIENT_ID` and `EQUINIX_CLIENT_SECRET`

### ✨ Added

#### OAuth 2.0 Implementation
- OAuth 2.0 client credentials authentication flow
- Automatic access token refresh (before 1-hour expiry)
- Refresh token management (60-day lifetime)
- Token expiry tracking and validation
- Seamless token rotation

#### New Authentication Features
- `SmartViewClient.authenticate()` - Initial OAuth token request
- `SmartViewClient.refresh_access_token()` - Token refresh logic
- `SmartViewClient.ensure_valid_token()` - Auto-refresh before requests
- Token expiry calculation (refreshes 5 min before expiry)

#### Enhanced Error Handling
- OAuth-specific error messages
- Automatic re-authentication on refresh failure
- Better credential validation
- Improved HTTP error reporting

#### Documentation Updates
- Complete OAuth 2.0 setup guide
- Token lifecycle documentation
- Security best practices
- Troubleshooting OAuth issues

### 🔄 Changed

- `SmartViewClient.__init__()` - Now accepts `client_id` and `client_secret`
- All API requests now use Bearer token from OAuth flow
- Request headers automatically include OAuth token

### 🔒 Security

- OAuth 2.0 standard compliance
- Short-lived access tokens (1 hour)
- Long-lived refresh tokens (60 days)
- Automatic token rotation
- No long-term credential storage in memory

### 📝 Documentation

- Updated README.md with OAuth sections
- Complete QUICKSTART guide rewrite
- Added security best practices
- Migration guide from v1.x

## [1.0.0] - 2024-12-XX

### Initial Release

- 23 MCP tools for SmartView APIs
- Environment monitoring (4 tools)
- Power management (2 tools)
- Subscription management (6 tools)
- Hierarchy navigation (2 tools)
- Asset management (4 tools)
- System alerts (2 tools)
- Plus 3 additional tools

---

**Full Changelog**: https://github.com/sliuuu/equinix-smartview-mcp/compare/v1.0.0...v2.0.0
