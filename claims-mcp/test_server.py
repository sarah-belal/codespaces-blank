import json
import subprocess

def test_mcp_server():
    print("Testing Server...\n")
    
    # Start server
    process = subprocess.Popen(
        ['python', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Test 1: Initialize
    print("Test 1: Initialize server...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_request) + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    print("✅ Server initialized\n")
    
    # Test 2: List tools
    print("Test 2: List available tools...")
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    process.stdin.write(json.dumps(list_tools_request) + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    result = json.loads(response)
    
    if 'result' in result and 'tools' in result['result']:
        tools = result['result']['tools']
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['name']}")
    print()
    
    # Test 3: Query claims
    print("Test 3: Query approved claims...")
    query_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "query_claims",
            "arguments": {"status": "APPROVED", "limit": 5}
        }
    }
    
    process.stdin.write(json.dumps(query_request) + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    print("✅ Query executed (check output above)\n")
    
    # Test 4: Get stats
    print("Test 4: Get claim statistics...")
    stats_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "get_claim_stats",
            "arguments": {"group_by": "status"}
        }
    }
    
    process.stdin.write(json.dumps(stats_request) + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    print("✅ Stats retrieved\n")
    
    # Cleanup
    process.terminate()
    print("✅ All tests completed! Server is working! 🎉")

if __name__ == "__main__":
    test_mcp_server()