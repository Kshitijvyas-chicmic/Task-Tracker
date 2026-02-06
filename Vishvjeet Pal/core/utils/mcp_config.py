# core/utils/mcp_config.py
import os
import sys
from mcp import StdioServerParameters

# 1. Locate the Python executable in your venv
# On Windows, it's usually in venv/Scripts/python.exe
# If you are running the app from the venv, sys.executable points to it automatically.
python_executable = sys.executable 

# 2. Locate the MCP server script
# We assume mcp_server.py is in the root directory
base_dir = os.getcwd()
mcp_script_path = os.path.join(base_dir, "mcp_server.py")

# 3. Define the parameters
server_params = StdioServerParameters(
    command=python_executable,
    args=[mcp_script_path],
    env={**os.environ, "PYTHONPATH": base_dir} # Ensure the subprocess can see your modules
)