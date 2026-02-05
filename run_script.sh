# !/bin/bash
# Setup virtual environment and run the FastAPI app Automatically

if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

read -p "Install riskauth-ml package? (yes/no) " response
if [ "$response" = "yes" ]; then
    pip install -e ../riskauth_ml
fi


uvicorn services.api:app --reload