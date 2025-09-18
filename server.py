#!/usr/bin/env python3
import asyncio, subprocess, tempfile, sys, os
from fastmcp import FastMCP

mcp = FastMCP("PyExecutor")

@mcp.tool()
async def exec_python(code: str) -> dict:
    """Execute Python code and return stdout / stderr"""
    max_mem = int(os.getenv('MAX_MEM_LIMIT', '500')) * 1024 * 1024
    with tempfile.NamedTemporaryFile("w+", suffix=".py") as f:
        f.write(f'''import resource\nresource.setrlimit(resource.RLIMIT_AS, ({max_mem}, {max_mem}))\n{code}''')
        f.flush()
        proc = await asyncio.create_subprocess_exec(
            sys.executable, f.name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
    return {"stdout": stdout.decode(), "stderr": stderr.decode()}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
