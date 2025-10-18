# Equinix SmartView MCP Server

[![GitHub release](https://img.shields.io/github/v/release/sliuuu/equinix-smartview-mcp)](https://github.com/sliuuu/equinix-smartview-mcp/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCP (Model Context Protocol) server for Equinix SmartView Data Center Infrastructure Management (DCIM) APIs with OAuth 2.0 authentication.

## 🚀 Features

- **OAuth 2.0 Authentication** - Secure client credentials flow with automatic token refresh
- **23 MCP Tools** - Complete coverage of SmartView API endpoints
- **Real-time Monitoring** - Environment, power, assets, and alerts
- **Subscription Management** - Near real-time event streaming
- **Production Ready** - Comprehensive error handling and documentation

## 📦 What's Included

### Environment Monitoring (4 tools)
- Current temperature and humidity data
- Historical trending data
- Sensor listings and details

### Power Management (2 tools)
- Current power consumption
- Historical power trends

### Subscription Management (6 tools)
- Create/update/delete subscriptions
- Real-time streaming data access

### Asset Management (4 tools)
- List infrastructure assets
- Search with wildcards
- Get affected customer assets

### Hierarchy Navigation (2 tools)
- Location hierarchy
- Power hierarchy

### System Alerts (2 tools)
- Get system alerts
- Advanced search capabilities

**Plus 3 additional tools** for tag points and asset management

## 🔧 Quick Start

### Prerequisites

- Python 3.10 or higher
- Equinix Customer Portal account
- SmartView API access enabled

### Installation

```bash
# Clone the repository
git clone https://github.com/sliuuu/equinix-smartview-mcp.git
cd equinix-smartview-mcp

# Run installation script
./scripts/install.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### OAuth 2.0 Setup

1. **Obtain OAuth Credentials**
   - Log in to [Equinix Customer Portal](https://portal.equinix.com)
   - Navigate to: Developer Settings → Apps
   - Click \"Create New App\"
   - Copy Client ID and Client Secret

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials
   ```

3. **Configure Claude Desktop**

   Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     \"mcpServers\": {
       \"equinix-smartview\": {
         \"command\": \"/path/to/venv/bin/python\",
         \"args\": [\"-m\", \"equinix_smartview_mcp.server\"],
         \"env\": {
           \"EQUINIX_CLIENT_ID\": \"your-client-id\",
           \"EQUINIX_CLIENT_SECRET\": \"your-client-secret\"
         }
       }
     }
   }
   ```

4. **Restart Claude Desktop**

## 💡 Usage Examples

### Environmental Monitoring
```
What's the current temperature in my SV1 cage?
```

### Create Subscription
```
Create a subscription to monitor power alerts in SV1 and NY5
```

### Asset Investigation
```
Which circuits are affected by electrical asset EL-12345 in SV1?
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - 5-minute setup
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Migration Guide](docs/MIGRATION.md) - Upgrade from v1.x
- [Changelog](CHANGELOG.md) - Version history

## 🔐 Security

- OAuth 2.0 standard compliance
- Automatic token refresh (1-hour TTL)
- Secure credential management
- No hardcoded secrets

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🔗 Links

- [Equinix SmartView Documentation](https://docs.equinix.com/smart-view/)
- [API Reference](https://docs.equinix.com/api-catalog/)
- [Report Issues](https://github.com/sliuuu/equinix-smartview-mcp/issues)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/sliuuu/equinix-smartview-mcp/issues)
- **Email**: api-support@equinix.com
- **Docs**: https://docs.equinix.com

---

**Version**: 2.0.0  
**Author**: Sam Liu (Equinix)  
**Status**: Production Ready
