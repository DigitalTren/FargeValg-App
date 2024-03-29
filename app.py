import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'
            )


def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes

    You shall generate color palettes that fit the theme, mood, or instuctuions in the prompt.
    The palettes shall be between 2 and 8 colors.
    Q: Convert the following verbal description of a color palette into a list of colors: a beautiful sunset
    A: ["#efc326", "#ff723c", "#f14545", "#bc2a66", "#7661c8", "#3e6afa"]

    Q: Convert the following verbal description of a color palette into a list of colors: a beautiful day at sea
    A: ["#d6e2fe", "#b2c2fe", "#7b9dfc", "#4758f1", "#1130e0", "#080fb8"]

    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:

    Result:
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors


@app.route('/palette', methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
