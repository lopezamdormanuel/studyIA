from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/preguntar", methods=["POST"])
def preguntar():

    datos = request.get_json()
    mensaje = datos.get("mensaje", "")

    try:
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres StudyIA, un asistente de estudio. "
                        "Explicas de forma clara, haces resúmenes, "
                        "tests y ayudas a aprender."
                    )
                },
                {
                    "role": "user",
                    "content": mensaje
                }
            ]
        )

        return jsonify({
            "respuesta": respuesta.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "respuesta": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)
