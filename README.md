# Seed Phrase Generator (Python + JavaScript)

Demo/learning tool. Do NOT use it to create a phrase for a wallet that will hold real money.

## Run
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Structure
- app.py            Flask server (serves the page + public wordlist only)
- bip39.py          Python BIP39 generate/validate (CLI: `python bip39.py 12`)
- static/index.html page
- static/style.css  styling
- static/app.js     generation + checker (runs in the browser, phrases never reach the server)
- wordlist/english.txt  official BIP39 2048 words

## Deploying
Serve over HTTPS if you host it (e.g. gunicorn behind nginx). Never log requests' contents; none carry phrases.
