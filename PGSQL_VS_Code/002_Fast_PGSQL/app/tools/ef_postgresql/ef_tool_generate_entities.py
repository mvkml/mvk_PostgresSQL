"""
Generate SQLAlchemy entity models from PostgreSQL
Run from terminal:
    python tools/generate_entities.py
"""

import subprocess
import sys
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

SQLACODEGEN_EXE = r"C:\Users\mvidh\AppData\Roaming\Python\Python314\Scripts\sqlacodegen.exe"

DB_URL = "postgresql+psycopg2://postgres:Postgres%40007@localhost:5432/VikiHospitalBot"

SCHEMA_NAME = "conv"
TABLE_NAME = "ai_message"

# ✅ Works when this file is at: <project-root>\tools\generate_entities.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "app" / "models"
OUTPUT_FILE = OUTPUT_DIR / "ai_message.py"

# =========================
# SCRIPT
# =========================

def main() -> None:
    print("🚀 Starting entity generation using sqlacodegen...")

    if not Path(SQLACODEGEN_EXE).exists():
        print(f"❌ sqlacodegen.exe not found: {SQLACODEGEN_EXE}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        SQLACODEGEN_EXE,
        DB_URL,
        "--schemas", SCHEMA_NAME,
        "--tables", TABLE_NAME,
        "--outfile", str(OUTPUT_FILE),
    ]

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)

        print("✅ Entity generated successfully!")
        print(f"📄 Output file: {OUTPUT_FILE}")

    except subprocess.CalledProcessError as ex:
        print("❌ Failed to generate entity")
        if ex.stdout:
            print("---- STDOUT ----")
            print(ex.stdout)
        if ex.stderr:
            print("---- STDERR ----")
            print(ex.stderr)
        sys.exit(ex.returncode)


if __name__ == "__main__":
    main()
