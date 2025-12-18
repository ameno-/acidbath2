# PROJECT:
Build a comprehensive agent tooling system demonstrating four approaches to external tool integration beyond traditional MCP servers.

# SUMMARY:
This project creates a demonstration system showing four different approaches for connecting AI agents to external tools: traditional MCP servers, CLI-based tools, file system scripts, and Claude skills. Each approach trades complexity for control, with MCP servers being simplest but consuming most context, while CLI tools, scripts, and skills offer progressive context preservation. The system uses Kalshi prediction markets as the example integration, allowing agents to search markets, analyze betting data, and understand market sentiment. The goal is to help developers choose the right tool integration approach based on their specific needs for context management, portability, and customization.

# STEPS:
1. Set up project structure with four distinct tool integration approaches
2. Create MCP server implementation for Kalshi prediction markets integration
3. Build CLI-based tool system with command-line interface and documentation
4. Develop file system scripts approach with isolated single-file tools
5. Implement Claude skills with progressive disclosure and bundled scripts
6. Create comparison framework showing trade-offs between each approach
7. Add comprehensive documentation explaining when to use each method
8. Include example prompts and workflows for each integration type
9. Build setup scripts for easy installation and testing
10. Create evaluation system for context window consumption analysis

# STRUCTURE:
```
beyond-mcp-agents/
├── README.md
├── setup.py
├── requirements.txt
├── apps/
│   ├── 1-mcp-server/
│   │   ├── server.py
│   │   ├── kalshi_client.py
│   │   └── mcp.json
│   ├── 2-cli-tools/
│   │   ├── cli.py
│   │   ├── readme.md
│   │   └── prime_kalshi_cli_tools.md
│   ├── 3-file-system-scripts/
│   │   ├── readme.md
│   │   ├── search.py
│   │   ├── get_market.py
│   │   ├── get_trades.py
│   │   └── get_orderbook.py
│   └── 4-skills/
│       └── kalshi_markets/
│           ├── skill.md
│           ├── search.py
│           ├── get_market.py
│           ├── get_trades.py
│           └── get_orderbook.py
├── docs/
│   ├── comparison.md
│   ├── when_to_use.md
│   └── examples/
├── scripts/
│   ├── install.sh
│   └── test_all_approaches.py
└── tests/
    ├── test_mcp.py
    ├── test_cli.py
    ├── test_scripts.py
    └── test_skills.py
```

# DETAILED EXPLANATION:
- MCP server provides traditional tool integration with full feature set
- CLI tools offer controlled interface with reduced context consumption
- File system scripts enable progressive disclosure with isolated functionality
- Skills provide Claude-specific integration with automatic tool discovery
- Kalshi client handles prediction market API interactions and authentication
- Prime prompts teach agents how to use each tool approach
- Comparison documentation helps developers choose appropriate integration method
- Setup scripts automate installation and configuration for all approaches
- Test suite validates functionality across all four integration methods
- Documentation provides comprehensive usage examples and best practices

# CODE:

## README.md
```markdown
# Beyond MCP: Four Approaches to Agent Tool Integration

This project demonstrates four different approaches for connecting AI agents to external tools, using Kalshi prediction markets as an example integration.

## Approaches

1. **MCP Server** - Traditional approach with full feature set but high context consumption
2. **CLI Tools** - Command-line interface with controlled context usage
3. **File System Scripts** - Progressive disclosure with isolated single-file tools
4. **Claude Skills** - Native Claude integration with automatic discovery

## Quick Start

```bash
# Install dependencies
./scripts/install.sh

# Test all approaches
python scripts/test_all_approaches.py

# Run specific approach
cd apps/2-cli-tools
python cli.py search --query "OpenAI AGI"
```

## Context Window Comparison

- MCP Server: ~10,000 tokens (5% of context window)
- CLI Tools: ~5,600 tokens (2.8% of context window)
- File System Scripts: ~2,000 tokens (1% of context window)
- Claude Skills: ~1,500 tokens (0.75% of context window)

## When to Use Each Approach

### MCP Server (80% of external tools)
- Use for existing third-party integrations
- When you need full feature set (tools, resources, prompts)
- For quick prototyping and standard integrations

### CLI Tools (15% of time)
- When you need to modify or extend existing tools
- For better context control with external services
- When building tools for humans and agents

### File System Scripts (4% of time)
- When context preservation is critical
- For highly focused, single-purpose tools
- When you need maximum portability

### Claude Skills (1% of time)
- For Claude-specific workflows
- When you want automatic tool discovery
- For bundled, self-contained functionality

## Configuration

Set your Kalshi API credentials:
```bash
export KALSHI_EMAIL="your_email@example.com"
export KALSHI_PASSWORD="your_password"
```

## Examples

See `docs/examples/` for detailed usage examples of each approach.
```

## apps/1-mcp-server/server.py
```python
#!/usr/bin/env python3
"""
Kalshi Prediction Markets MCP Server

Provides AI agents with access to Kalshi prediction markets data
including market search, trade analysis, and sentiment tracking.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from kalshi_client import KalshiClient

# Initialize MCP server
server = Server("kalshi-markets")

# Global client instance
kalshi_client = None

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available Kalshi market tools."""
    return [
        Tool(
            name="search_markets",
            description="Search Kalshi prediction markets by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for markets"
                    },
                    "limit": {
                        "type": "integer", 
                        "description": "Maximum number of results",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_market_details",
            description="Get detailed information about a specific market",
            inputSchema={
                "type": "object",
                "properties": {
                    "market_ticker": {
                        "type": "string",
                        "description": "Market ticker symbol"
                    }
                },
                "required": ["market_ticker"]
            }
        ),
        Tool(
            name="get_market_trades",
            description="Get recent trades for a market",
            inputSchema={
                "type": "object",
                "properties": {
                    "market_ticker": {
                        "type": "string",
                        "description": "Market ticker symbol"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of trades to fetch",
                        "default": 50
                    }
                },
                "required": ["market_ticker"]
            }
        ),
        Tool(
            name="get_market_orderbook",
            description="Get current orderbook for a market",
            inputSchema={
                "type": "object",
                "properties": {
                    "market_ticker": {
                        "type": "string",
                        "description": "Market ticker symbol"
                    }
                },
                "required": ["market_ticker"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from the agent."""
    global kalshi_client
    
    # Initialize client if needed
    if kalshi_client is None:
        kalshi_client = KalshiClient()
        await kalshi_client.authenticate()
    
    try:
        if name == "search_markets":
            # Search for markets matching the query
            results = await kalshi_client.search_markets(
                query=arguments["query"],
                limit=arguments.get("limit", 10)
            )
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
            
        elif name == "get_market_details":
            # Get detailed market information
            details = await kalshi_client.get_market_details(
                market_ticker=arguments["market_ticker"]
            )
            return [TextContent(
                type="text", 
                text=json.dumps(details, indent=2)
            )]
            
        elif name == "get_market_trades":
            # Get recent trades for the market
            trades = await kalshi_client.get_market_trades(
                market_ticker=arguments["market_ticker"],
                limit=arguments.get("limit", 50)
            )
            return [TextContent(
                type="text",
                text=json.dumps(trades, indent=2)
            )]
            
        elif name == "get_market_orderbook":
            # Get current market orderbook
            orderbook = await kalshi_client.get_market_orderbook(
                market_ticker=arguments["market_ticker"]
            )
            return [TextContent(
                type="text",
                text=json.dumps(orderbook, indent=2)
            )]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kalshi-markets",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## apps/1-mcp-server/kalshi_client.py
```python
#!/usr/bin/env python3
"""
Kalshi API Client

Handles authentication and API interactions with Kalshi prediction markets.
Provides methods for market search, trade data, and orderbook access.
"""

import os
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional

class KalshiClient:
    """Client for interacting with Kalshi prediction markets API."""
    
    def __init__(self):
        """Initialize the Kalshi client with credentials from environment."""
        self.base_url = "https://trading-api.kalshi.com/trade-api/v2"
        self.email = os.getenv("KALSHI_EMAIL")
        self.password = os.getenv("KALSHI_PASSWORD")
        self.session = None
        self.token = None
        
        if not self.email or not self.password:
            raise ValueError("KALSHI_EMAIL and KALSHI_PASSWORD must be set")
    
    async def authenticate(self) -> None:
        """Authenticate with Kalshi API and get access token."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        auth_data = {
            "email": self.email,
            "password": self.password
        }
        
        async with self.session.post(
            f"{self.base_url}/login",
            json=auth_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                self.token = data.get("token")
            else:
                raise Exception(f"Authentication failed: {response.status}")
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to Kalshi API."""
        if not self.token:
            await self.authenticate()
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        async with self.session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"API request failed: {response.status}")
    
    async def search_markets(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for markets matching the given query."""
        params = {
            "cursor": None,
            "limit": limit,
            "event_ticker": query,  # Search by event ticker
            "series_ticker": query,  # Also search by series ticker
        }
        
        # Make request to markets endpoint
        result = await self._make_request("markets", params)
        markets = result.get("markets", [])
        
        # Filter results that match query in title or ticker
        filtered_markets = []
        query_lower = query.lower()
        
        for market in markets:
            title = market.get("title", "").lower()
            ticker = market.get("ticker", "").lower()
            
            if query_lower in title or query_lower in ticker:
                filtered_markets.append({
                    "ticker": market.get("ticker"),
                    "title": market.get("title"),
                    "subtitle": market.get("subtitle"),
                    "yes_price": market.get("yes_bid", 0),
                    "no_price": market.get("no_bid", 0),
                    "volume": market.get("volume", 0),
                    "open_interest": market.get("open_interest", 0),
                    "close_time": market.get("close_time"),
                    "status": market.get("status")
                })
        
        return filtered_markets[:limit]
    
    async def get_market_details(self, market_ticker: str) -> Dict:
        """Get detailed information for a specific market."""
        result = await self._make_request(f"markets/{market_ticker}")
        market = result.get("market", {})
        
        return {
            "ticker": market.get("ticker"),
            "title": market.get("title"),
            "subtitle": market.get("subtitle"),
            "description": market.get("description"),
            "yes_price": market.get("yes_bid", 0),
            "no_price": market.get("no_bid", 0),
            "last_price": market.get("last_price", 0),
            "volume": market.get("volume", 0),
            "volume_24h": market.get("volume_24h", 0),
            "open_interest": market.get("open_interest", 0),
            "liquidity": market.get("liquidity", 0),
            "close_time": market.get("close_time"),
            "expiration_time": market.get("expiration_time"),
            "status": market.get("status"),
            "category": market.get("category"),
            "rules": market.get("rules")
        }
    
    async def get_market_trades(self, market_ticker: str, limit: int = 50) -> List[Dict]:
        """Get recent trades for a market."""
        params = {"limit": limit}
        result = await self._make_request(f"markets/{market_ticker}/trades", params)
        trades = result.get("trades", [])
        
        return [
            {
                "trade_id": trade.get("trade_id"),
                "price": trade.get("price"),
                "count": trade.get("count"),
                "side": trade.get("side"),
                "timestamp": trade.get("ts"),
                "taker_side": trade.get("taker_side")
            }
            for trade in trades
        ]
    
    async def get_market_orderbook(self, market_ticker: str) -> Dict:
        """Get current orderbook for a market."""
        
