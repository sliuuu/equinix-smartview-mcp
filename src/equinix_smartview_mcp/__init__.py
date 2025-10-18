"""Equinix SmartView MCP Server"""

__version__ = "2.0.0"
__author__ = "Sam Liu / Equinix"
__description__ = "MCP Server for Equinix SmartView DCIM APIs with OAuth 2.0"

from .server import SmartViewClient, app

__all__ = ["SmartViewClient", "app"]
