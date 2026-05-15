from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

APP_ID = "7410598410667802"
SECRET_KEY = "acl6zQelCtwhtcxSXdqjQHFmhrncbscL"
REDIRECT_URI = "https://threaten-elm-wrist.ngrok-free.dev/callback"
ACCESS_TOKEN = "APP_USR-7410598410667802-051409-c50ce3709fd332ec9374d9d83002ae78-3395553141"


@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return jsonify({"error": "No se recibió el código de autorización"}), 400

    response = requests.post(
        "https://api.mercadolibre.com/oauth/token",
        headers={
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "authorization_code",
            "client_id": APP_ID,
            "client_secret": SECRET_KEY,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
    )

    data = response.json()
    print("✅ ACCESS_TOKEN:", data.get("access_token"))
    print("✅ REFRESH_TOKEN:", data.get("refresh_token"))  # debe empezar con TG-
    
    return jsonify(data)
    #print("Access Token:", token_data.get("access_token"))
    #return jsonify(token_data)  # <-- jsonify para que Flask lo devuelva correctamente


@app.route("/me")
def me():
    """Ruta de prueba para verificar que el token funciona"""
    response = requests.get(
        "https://api.mercadolibre.com/users/me",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(port=5000)
