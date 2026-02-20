# CLAUDE.md — equinix-smartview-mcp

MCP server for the Equinix SmartView DCIM API — power, environmental monitoring, assets, and alerts.

## Project layout

```
src/equinix_smartview_mcp/
    __init__.py
    server.py                    ← active MCP server (use this)
    smartview_server_complete.py ← alternate/extended version
    smartview_server_improved.py ← alternate/improved version
    server.bak                   ← snapshot, do not edit
tests/
    test_server.py
    smartview_tests.py
```

`server.py` is the canonical entry point. The `smartview_server_complete.py` and `smartview_server_improved.py` variants may have more tools — check before adding features that might already exist there.

## Auth

Bearer token authentication (despite the env var name being `EQUINIX_SMARTVIEW_API_KEY`, the value is a Bearer token):

```bash
export EQUINIX_SMARTVIEW_API_KEY="your-bearer-token"
export EQUINIX_SMARTVIEW_API_URL="https://api.equinix.com"  # optional, this is the default
```

Different from equinix-fabric-mcp — SmartView uses a static Bearer token, not OAuth2 client_credentials.

## Setup

```bash
cd ~/Development/Equinix/equinix-smartview-mcp
source venv/bin/activate

# First time / after pulling
pip install -e ".[dev]"
```

## Running

```bash
source venv/bin/activate
export EQUINIX_SMARTVIEW_API_KEY="your-token"

# Via module (preferred)
python -m equinix_smartview_mcp.server

# Via installed entry point
equinix-smartview-mcp
```

## Testing

```bash
source venv/bin/activate

# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=src/equinix_smartview_mcp --cov-report=term-missing

# Specific test file
pytest tests/test_server.py -v
```

## Code quality

```bash
source venv/bin/activate

black src/           # format
ruff check src/      # lint
mypy src/            # type check
```

Line length: 100. Target: Python 3.10+. Mypy strict mode.

## Build

```bash
pip install build
python -m build      # outputs to dist/
```

## Key differences from equinix-fabric-mcp

| | equinix-fabric-mcp | equinix-smartview-mcp |
|---|---|---|
| Auth | OAuth2 client_credentials | Bearer token |
| Entry point | `server_v2.py` (direct) | `python -m equinix_smartview_mcp.server` |
| Layout | Flat | `src/` package layout |
| HTTP wrapper | Yes (`http_wrapper.py` + Docker) | No |
| Domains | Connections, ports, routers | Power, environment, assets, alerts |
| Config | `pyproject.toml` | — |

## Note on README

The top-level `README.md` says to copy files from Claude artifacts — this was the initial scaffolding step. `server.py` is already present in `src/`. The README is outdated on this point.
