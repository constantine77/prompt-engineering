from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = 'XYZ'

# Function to generate meal plan


def create_meals(ingredients, kcal=2000):
    prompt = f'''Create a healthy daily meal plan for breakfast, lunch and dinner based on
    the following ingredients {ingredients}.
    Explain each recipe.
    The total daily intake of kcal should be below {kcal}.
    Assign a suggestive and concise title to each meal.
    Your answer should end with 'Titles: ' and the title of each recipe.'''

    messages = [
        {'role': 'system', 'content': 'You are a talented cook.'},
        {'role': 'user', 'content': prompt}
    ]

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10,
    )

    return response.choices[0].text

# Function to create and save image


def create_and_save_image(title, extra=''):
    import requests
    import shutil

    image_prompt = f'{title}, {extra}, high quality food photography'
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size='1024x1024'
    )

    image_url = response['data'][0]['url']

    image_resource = requests.get(image_url, stream=True)

    image_filename = f'{title}.png'
    if image_resource.status_code == 200:
        with open(f'static/images/{image_filename}', 'wb') as f:
            shutil.copyfileobj(image_resource.raw, f)
            if os.path.isfile(f'static/images/{image_filename}'):
                return image_filename
            else:
                return False
    else:
        return False


# Home page


@app.route('/')
def home():
    return render_template('index.html')

# Meal plan generator page


@app.route('/mealplan', methods=['POST'])
def mealplan():
    ingredients = request.form['ingredients']
    kcal = request.form['kcal']
    output = create_meals(ingredients, kcal)
    titles = output.splitlines()[-3:]
    titles = [t.strip('- ') for t in titles]
    image_filenames = []
    for title in titles:
        image_filename = create_and_save_image(title, 'white background')
        if image_filename:
            image_filenames.append(image_filename)
    return render_template('mealplan.html', output=output, titles=titles, image_filenames=image_filenames)


if __name__ == '__main__':
    app.run(debug=True, port=5008)
