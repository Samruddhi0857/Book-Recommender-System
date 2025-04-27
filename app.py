from flask import Flask, render_template, request
import pickle
import numpy as np

pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def recommend_ui():
    return render_template('recommend.html', data=None, user_input="")

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    user_input_lower = user_input.lower()

    # Find the matching book title (case-insensitive)
    pt_titles_lower = [title.lower() for title in pt.index]

    if user_input_lower in pt_titles_lower:
        index = pt_titles_lower.index(user_input_lower)

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:9]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        
        return render_template('recommend.html', data=data, user_input=user_input)
    
    else:
        # If not found, show no recommendations
        return render_template('recommend.html', data=[], user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
