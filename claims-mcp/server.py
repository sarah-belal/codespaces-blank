import asyncio
import pandas as pd
from mcp.server import Server
from mcp.types import Tool, TextContent

# Load data
claims_df = pd.read_csv('claims.csv')
members_df = pd.read_csv('members.csv')
policies_df = pd.read_csv('policies.csv')

app = Server("mini-snowflake-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Define available tools for Claude"""
    return [
        Tool(
            name="query_claims",
            description="Search and filter claims data",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status (APPROVED, DENIED, PENDING, UNDER_REVIEW)"},
                    "claim_type": {"type": "string", "description": "Filter by type (MEDICAL, DENTAL, VISION, PHARMACY, MENTAL_HEALTH)"},
                    "min_amount": {"type": "number", "description": "Minimum claim amount"},
                    "max_amount": {"type": "number", "description": "Maximum claim amount"},
                    "limit": {"type": "integer", "description": "Max number of results (default 10)"}
                }
            }
        ),
        Tool(
            name="get_claim_by_id",
            description="Get detailed information about a specific claim",
            inputSchema={
                "type": "object",
                "properties": {
                    "claim_id": {"type": "string", "description": "Claim ID (e.g., CLM-00001)"}
                },
                "required": ["claim_id"]
            }
        ),
        Tool(
            name="get_claim_stats",
            description="Get aggregate statistics about claims",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_by": {"type": "string", "description": "Group by: status, claim_type, or none for overall stats"},
                    "status": {"type": "string", "description": "Filter by status before aggregating"}
                }
            }
        ),
        Tool(
            name="search_members",
            description="Search for members by name or ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "member_id": {"type": "string", "description": "Member ID"},
                    "name": {"type": "string", "description": "Search by name (partial match)"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls from Claude"""
    
    if name == "query_claims":
        # Start with all claims
        filtered = claims_df.copy()
        
        # Apply filters
        if 'status' in arguments and arguments['status']:
            filtered = filtered[filtered['status'] == arguments['status'].upper()]
        
        if 'claim_type' in arguments and arguments['claim_type']:
            filtered = filtered[filtered['claim_type'] == arguments['claim_type'].upper()]
        
        if 'min_amount' in arguments:
            filtered = filtered[filtered['claim_amount'] >= arguments['min_amount']]
        
        if 'max_amount' in arguments:
            filtered = filtered[filtered['claim_amount'] <= arguments['max_amount']]
        
        # Limit results
        limit = arguments.get('limit', 10)
        result = filtered.head(limit)
        
        # Format output
        output = f"Found {len(filtered)} claims (showing {len(result)}):\n\n"
        output += result.to_string(index=False)
        
        return [TextContent(type="text", text=output)]
    
    elif name == "get_claim_by_id":
        claim_id = arguments['claim_id']
        claim = claims_df[claims_df['claim_id'] == claim_id]
        
        if claim.empty:
            return [TextContent(type="text", text=f"No claim found with ID: {claim_id}")]
        
        # Get member info
        member_id = claim.iloc[0]['member_id']
        member = members_df[members_df['member_id'] == member_id]
        
        output = "CLAIM DETAILS:\n"
        output += claim.to_string(index=False)
        
        if not member.empty:
            output += "\n\nMEMBER INFO:\n"
            output += member.to_string(index=False)
        
        return [TextContent(type="text", text=output)]
    
    elif name == "get_claim_stats":
        filtered = claims_df.copy()
        
        # Apply status filter if provided
        if 'status' in arguments and arguments['status']:
            filtered = filtered[filtered['status'] == arguments['status'].upper()]
        
        group_by = arguments.get('group_by', 'none')
        
        if group_by == 'none':
            stats = {
                'Total Claims': len(filtered),
                'Total Amount': f"${filtered['claim_amount'].sum():,.2f}",
                'Average Amount': f"${filtered['claim_amount'].mean():,.2f}",
                'Min Amount': f"${filtered['claim_amount'].min():,.2f}",
                'Max Amount': f"${filtered['claim_amount'].max():,.2f}"
            }
            output = "OVERALL STATISTICS:\n"
            for key, value in stats.items():
                output += f"{key}: {value}\n"
        
        elif group_by in ['status', 'claim_type']:
            grouped = filtered.groupby(group_by)['claim_amount'].agg(['count', 'sum', 'mean'])
            grouped.columns = ['Count', 'Total', 'Average']
            grouped['Total'] = grouped['Total'].apply(lambda x: f"${x:,.2f}")
            grouped['Average'] = grouped['Average'].apply(lambda x: f"${x:,.2f}")
            
            output = f"STATISTICS BY {group_by.upper()}:\n\n"
            output += grouped.to_string()
        
        else:
            output = f"Invalid group_by value: {group_by}. Use 'status', 'claim_type', or 'none'"
        
        return [TextContent(type="text", text=output)]
    
    elif name == "search_members":
        if 'member_id' in arguments and arguments['member_id']:
            result = members_df[members_df['member_id'] == arguments['member_id']]
        elif 'name' in arguments and arguments['name']:
            result = members_df[members_df['name'].str.contains(arguments['name'], case=False, na=False)]
        else:
            return [TextContent(type="text", text="Please provide either member_id or name")]
        
        if result.empty:
            return [TextContent(type="text", text="No members found")]
        
        output = f"Found {len(result)} member(s):\n\n"
        output += result.to_string(index=False)
        
        return [TextContent(type="text", text=output)]

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())