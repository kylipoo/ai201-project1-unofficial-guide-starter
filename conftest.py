import sys
from pathlib import Path

# Add the project root to sys.path so tests in tests/ can import top-level modules.
sys.path.insert(0, str(Path(__file__).parent))
