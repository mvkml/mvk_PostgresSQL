# Ensure we are in project root
Set-Location "C:\v\v\learn\lv_python\ai\VishAgent"

# Activate venv
.\app\venv\Scripts\activate

$entityShema = "conv"
$entityName = "ai_message"
$entityFolder = "app\dal\entities\$entityShema"

#if folder not exists create folder
if (-Not (Test-Path -Path $entityFolder)) {
    New-Item -ItemType Directory -Path $entityFolder
}

$entityPath = "$entityFolder\$entityName.py"

# Generate SQLAlchemy entity
python -m sqlacodegen `
  "postgresql+psycopg2://postgres:Postgres%40007@localhost:5432/VikiHospitalBot" `
  --schemas $entityShema `
  --tables $entityName `
  --outfile $entityPath

Write-Host "✅ Entity generated: $entityPath"
#open created $entityPath
