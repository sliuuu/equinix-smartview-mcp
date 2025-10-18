#!/usr/bin/env python3
"""
Equinix SmartView MCP Server with OAuth 2.0

Data Center Infrastructure Management (DCIM) integration
Provides access to power, environmental, assets, and alerting data
"""

import asyncio
import os
import json
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration - OAuth 2.0
CLIENT_ID = os.getenv("EQUINIX_CLIENT_ID")
CLIENT_SECRET = os.getenv("EQUINIX_CLIENT_SECRET")
BASE_URL = os.getenv("EQUINIX_API_URL", "https://api.equinix.com")
TOKEN_ENDPOINT = f"{BASE_URL}/oauth2/v1/token"
REFRESH_ENDPOINT = f"{BASE_URL}/oauth2/v1/refreshaccesstoken"

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "EQUINIX_CLIENT_ID and EQUINIX_CLIENT_SECRET environment variables are required. "
        "Obtain these from Equinix Customer Portal: Developer Settings > Apps"
    )


class SmartViewClient:
    """Client for Equinix SmartView APIs with OAuth 2.0 authentication"""
    
    def __init__(self, client_id: str, client_secret: str, base_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        await self.authenticate()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
    
    async def authenticate(self) -> None:
        """Obtain OAuth 2.0 access token"""
        try:
            response = await self.http_client.post(
                TOKEN_ENDPOINT,
                json={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data.get("refresh_token")
            timeout = int(data.get("token_timeout", 3600))
            self.token_expiry = datetime.now() + timedelta(seconds=timeout - 300)
        except httpx.HTTPError as e:
            raise Exception(f"OAuth authentication failed: {e}")
    
    async def refresh_access_token(self) -> None:
        """Refresh access token"""
        if not self.refresh_token:
            await self.authenticate()
            return
        try:
            response = await self.http_client.post(
                REFRESH_ENDPOINT,
                json={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                },
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data.get("refresh_token", self.refresh_token)
            timeout = int(data.get("token_timeout", 3600))
            self.token_expiry = datetime.now() + timedelta(seconds=timeout - 300)
        except httpx.HTTPError:
            await self.authenticate()
    
    async def ensure_valid_token(self) -> None:
        """Ensure token is valid, refresh if needed"""
        if not self.access_token or not self.token_expiry:
            await self.authenticate()
        elif datetime.now() >= self.token_expiry:
            await self.refresh_access_token()
    
    def _clean_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values and convert lists"""
        cleaned = {}
        for key, value in params.items():
            if value is not None and value != "" and value != []:
                if isinstance(value, list):
                    cleaned[key] = ",".join(str(v) for v in value)
                else:
                    cleaned[key] = value
        return cleaned
    
    async def request(
        self, endpoint: str, method: str = "GET", body: Optional[Dict] = None,
        query_params: Optional[Dict] = None
    ) -> Any:
        """Make authenticated HTTP request"""
        await self.ensure_valid_token()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        filtered_params = self._clean_params(query_params) if query_params else {}
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.http_client.request(
                method=method, url=url, params=filtered_params,
                json=body if body else None, headers=headers
            )
            response.raise_for_status()
            return response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        except httpx.HTTPStatusError as e:
            raise Exception(f"API Error {e.response.status_code}: {e.response.text}")
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error: {e}")
    
    # Environment APIs
    async def get_current_environment(self, account_no: str, ibx: str, level_type: str, level_value: Optional[str] = None) -> Any:
        return await self.request("/environment/v1/current", query_params={"accountNo": account_no, "ibx": ibx, "levelType": level_type, "levelValue": level_value})
    
    async def get_trending_environment(self, account_no: str, ibx: str, level_type: str, level_value: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, interval: Optional[int] = None) -> Any:
        return await self.request("/environment/v1/trending", query_params={"accountNo": account_no, "ibx": ibx, "levelType": level_type, "levelValue": level_value, "fromDate": from_date, "toDate": to_date, "interval": interval})
    
    async def get_environment_sensors(self, account_no: str, ibx: str, offset: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None) -> Any:
        return await self.request("/environment/v1/sensors", query_params={"accountNo": account_no, "ibx": ibx, "offset": offset, "limit": limit, "sort": sort})
    
    async def get_environment_sensor_by_id(self, account_no: str, ibx: str, sensor_id: str) -> Any:
        return await self.request("/environment/v1/sensor", query_params={"accountNo": account_no, "ibx": ibx, "sensorId": sensor_id})
    
    # Subscription APIs
    async def get_all_subscriptions(self) -> Any:
        return await self.request("/smartview/v2/streaming/subscriptions")
    
    async def get_subscription_by_id(self, subscription_id: str) -> Any:
        return await self.request(f"/smartview/v2/streaming/subscriptions/{subscription_id}")
    
    async def create_subscription(self, subscription: Dict) -> Any:
        return await self.request("/smartview/v2/streaming/subscriptions", method="POST", body=subscription)
    
    async def update_subscription(self, subscription_id: str, subscription: Dict) -> Any:
        return await self.request(f"/smartview/v2/streaming/subscriptions/{subscription_id}", method="PUT", body=subscription)
    
    async def delete_subscription(self, subscription_id: str) -> Any:
        return await self.request(f"/smartview/v2/streaming/subscriptions/{subscription_id}", method="DELETE")
    
    async def get_subscription_data(self, subscription_id: str, ibxs: Optional[List[str]] = None, message_types: Optional[List[str]] = None, stream_ids: Optional[List[str]] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Any:
        return await self.request(f"/smartview/v2/streaming/subscriptions/{subscription_id}/data", query_params={"ibxs": ibxs, "messageTypes": message_types, "streamIds": stream_ids, "offset": offset, "limit": limit})
    
    # Hierarchy APIs
    async def get_location_hierarchy(self, account_no: str, ibx: str, asset_id: Optional[str] = None) -> Any:
        return await self.request("/smartview/v1/hierarchy/location", query_params={"accountNo": account_no, "ibx": ibx, "assetId": asset_id})
    
    async def get_power_hierarchy(self, account_no: str, ibx: str, asset_id: Optional[str] = None) -> Any:
        return await self.request("/smartview/v1/hierarchy/power", query_params={"accountNo": account_no, "ibx": ibx, "assetId": asset_id})
    
    # Assets APIs
    async def list_assets(self, account_no: str, ibx: str, cage: str, classification: str, category: Optional[str] = None, template: Optional[str] = None) -> Any:
        return await self.request("/smartview/v1/asset/list", query_params={"accountNo": account_no, "ibx": ibx, "cage": cage, "classification": classification, "category": category, "template": template})
    
    async def get_asset_details(self, body: Dict) -> Any:
        return await self.request("/smartview/v1/asset/details", method="POST", body=body)
    
    async def get_affected_assets(self, account_no: str, ibx: str, asset_id: str, classification: str) -> Any:
        return await self.request("/smartview/v1/asset/tagpoint/affected-assets", query_params={"accountNo": account_no, "ibx": ibx, "assetId": asset_id, "classification": classification})
    
    async def search_assets(self, account_no: str, ibx: str, search_pattern: str, classification: str) -> Any:
        return await self.request("/smartview/v1/asset/search", query_params={"accountNo": account_no, "ibx": ibx, "searchPattern": search_pattern, "classification": classification})
    
    # Power APIs
    async def get_current_power(self, account_no: str, ibx: str, level_type: str, level_value: Optional[str] = None) -> Any:
        return await self.request("/dcim/v1/power/current", query_params={"accountNo": account_no, "ibx": ibx, "levelType": level_type, "levelValue": level_value})
    
    async def get_trending_power(self, account_no: str, ibx: str, level_type: str, level_value: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, interval: Optional[int] = None) -> Any:
        return await self.request("/dcim/v1/power/trending", query_params={"accountNo": account_no, "ibx": ibx, "levelType": level_type, "levelValue": level_value, "fromDate": from_date, "toDate": to_date, "interval": interval})
    
    # System Alert APIs
    async def get_system_alerts(self, account_no: str, ibx: Optional[str] = None, severity: Optional[str] = None, status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Any:
        return await self.request("/dcim/v1/system-alert", query_params={"accountNo": account_no, "ibx": ibx, "severity": severity, "status": status, "fromDate": from_date, "toDate": to_date, "offset": offset, "limit": limit})
    
    async def search_system_alerts(self, body: Dict) -> Any:
        return await self.request("/dcim/v1/system-alert/search", method="POST", body=body)
    
    async def close(self):
        await self.http_client.aclose()


# Initialize MCP Server
app = Server("equinix-smartview-mcp")
client_instance = None


async def get_client():
    global client_instance
    if client_instance is None:
        client_instance = SmartViewClient(CLIENT_ID, CLIENT_SECRET, BASE_URL)
        await client_instance.authenticate()
    return client_instance