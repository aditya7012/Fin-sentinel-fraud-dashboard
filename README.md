# Fin-Sentinel

AI fraud detection dashboard built with Streamlit for product demo and internship showcase.

## Run locally

```bash
python3.13 -m venv .venv313
.venv313/bin/pip install -r requirements.txt
.venv313/bin/streamlit run app.py --server.port 8502
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload these files to the repo:
   - `app.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`
3. Do not upload `creditcard.csv` (already excluded in `.gitignore`).
4. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
5. Click **Create app**.
6. Select your repo and branch.
7. Set **Main file path** to `app.py`.
8. Click **Deploy**.

## Notes

- The app automatically uses `creditcard.csv` if present locally.
- On Community Cloud, it will use the fallback hosted CSV URL.
