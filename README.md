# Claims MCP Server

A Model Context Protocol (MCP) server that enables AI assistants like Claude to query insurance claims data using natural language. This is intended to behave like a data warehouse analytics workflow using CSV files and Pandas.

## Overview

This project uses an MCP server to bridges AI with structured claims + member data, enabling natural language querying of insurance claims without requiring SQL knowledge.

## Features

- Query 10,000+ synthetic insurance claims records
- Filter by status, claim type, amount ranges, and more
- Generate statistics such as totals, averages, median
- Member and policy lookup
- Natural language interface via Claude AI
- Tools for quick data analysis

## Data Schema

### Claims Table (10,000 records)
| Field | Type | Description |
|-------|------|-------------|
| `claim_id` | String | Unique claim identifier (CLM-XXXXX) |
| `member_id` | String | Associated member ID |
| `claim_date` | Date | When claim was filed |
| `claim_type` | String | MEDICAL, DENTAL, VISION, PHARMACY, MENTAL_HEALTH |
| `claim_amount` | Float | Dollar amount |
| `status` | String | APPROVED, DENIED, PENDING, UNDER_REVIEW |
| `processed_date` | Date | When claim was processed (null if pending) |
| `provider_name` | String | Healthcare provider name |

### Members Table (1,000 records)
- `member_id`, `name`, `age`, `email`, `phone`, `zip_code`

### Policies Table (1,000 records)
- `policy_id`, `member_id`, `plan_type`, `premium`, `deductible`, `effective_date`

## Tech Stack

- **Python
- **MCP
- **Pandas** 
- **Faker** 

## Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mini-snowflake-mcp.git
cd mini-snowflake-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python generate_data.py
```

## Usage

### Command-Line Tools

**Get Statistics:**
```bash
# Overall statistics
python get_stats.py

# Specific queries
python get_stats.py status      # Claims by status
python get_stats.py type        # Claims by type
python get_stats.py approved    # Approved claims stats
python get_stats.py denied      # Denied claims stats
python get_stats.py pending     # Pending claims stats
```

**Look Up Specific Claim:**
```bash
python claim.py CLM-00001
python claim.py CLM-00500
```

### MCP Server

**Run the server:**
```bash
python server.py
```

**Test the server:**
```bash
python test_server.py
```

### Use with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):
```json
{
  "mcpServers": {
    "claims": {
      "command": "python",
      "args": ["/full/path/to/mini-snowflake-mcp/server.py"]
    }
  }
}
```

Then ask Claude:
- "Show me all approved medical claims over $5000"
- "What's the average claim amount by status?"
- "Get details for claim CLM-00123"
- "How many denied claims do we have?"

## Available MCP Tools

### `query_claims`
Search and filter claims with optional parameters:
- `status` - Filter by claim status
- `claim_type` - Filter by claim type  
- `min_amount` / `max_amount` - Amount range
- `limit` - Max results (default 10)

### `get_claim_by_id`
Get detailed information about a specific claim including associated member info.

**Parameters:**
- `claim_id` (required) - Claim ID (e.g., CLM-00001)

### `get_claim_stats`
Get aggregate statistics with optional grouping and filtering.

**Parameters:**
- `group_by` - Group by "status", "claim_type", or "none" for overall stats
- `status` - Filter by status before aggregating

### `search_members`
Search members by ID or name (supports partial name matching).

**Parameters:**
- `member_id` - Exact member ID
- `name` - Partial name search

## Project Structure
```
mini-snowflake-mcp/
├── server.py              # Main MCP server
├── generate_data.py       # Synthetic data generator
├── test_server.py         # MCP server tests
├── get_stats.py           # CLI statistics tool
├── claim.py               # CLI claim lookup tool
├── claims.csv             # Generated claims data (10K records)
├── members.csv            # Generated member data (1K records)
├── policies.csv           # Generated policy data (1K records)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Example Queries

**Natural Language (via Claude):**
- "Show me all approved medical claims over $5000"
- "What's the average claim amount for denied claims?"
- "How many pending claims are there?"
- "Get details for claim CLM-00456"
- "Show me claims from member MEM-00123"

**Command Line:**
```bash
# Quick stats
python get_stats.py approved

# Look up claim
python claim.py CLM-00789
```

## Development

**Regenerate data with different seed:**
```python
# In generate_data.py
Faker.seed(123)  # Change this number
```

**Add new claim types or statuses:**
```python
# In generate_data.py
claim_types = ['MEDICAL', 'DENTAL', 'VISION', 'PHARMACY', 'MENTAL_HEALTH', 'CUSTOM_TYPE']
statuses = ['APPROVED', 'DENIED', 'PENDING', 'UNDER_REVIEW', 'CUSTOM_STATUS']
```

