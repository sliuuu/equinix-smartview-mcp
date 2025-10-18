# SmartView MCP Server - Quick Start Guide

Get up and running with OAuth 2.0 in 5 minutes.

## Prerequisites

- Python 3.10+
- Equinix Customer Portal account
- SmartView API access

## Step 1: Obtain OAuth Credentials (2 min)

1. Log in to https://portal.equinix.com
2. Navigate to: **Developer Settings** → **Apps**
3. Click **"Create New App"**
4. Fill in:
   - App Name: `SmartView MCP`
   - Environment: Production
5. Copy **Client ID** and **Client Secret** (shown once!)

## Step 2: Install (2 min)

```bash
git clone https://github.com/sliuuu/equinix-smartview-mcp.git
cd equinix-smartview-mcp
./scripts/install.sh
```

## Step 3: Configure (1 min)

```bash
cp .env.example .env
# Edit .env and add your credentials
```

## Step 4: Test

```bash
python test_oauth.py  # See repository for test script
```

## Next Steps

- Configure Claude Desktop (see README.md)
- Try example prompts
- Read full documentation
