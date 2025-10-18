import os
from pathlib import Path
from dotenv import load_dotenv

root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / ".env"

if env_path.exists():
    load_dotenv(env_path, override=True)

os.environ["ENVIRONMENT"] = "test"