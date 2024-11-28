from flask import Flask, request, jsonify, render_template
import requests
import random
import re
import nltk
import joblib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer




app = Flask(__name__)


nltk.download('stopwords', quiet=True)



ps=PorterStemmer()

movies = joblib.load('movies.pkl')
similarity = joblib.load('similarity.pkl')
movies_reviews = joblib.load('review_model.pkl')
CounttVectorizer = joblib.load('count_ver.pkl')



def fetch_poster(movie_id):
    api_key = '0d949a24180760de0dd5d14b53560285'
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']




def fetch_movie_details(movie_id):
    api_key = '0d949a24180760de0dd5d14b53560285'
    
  
   
    watch_providers_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}')
    watch_providers = watch_providers_response.json()

    
    providers = watch_providers.get('results', {}).get('AU', {}).get('link')


    return {

        'poster_path': fetch_poster(movie_id),
        'watch': providers
    }




def fetch_movie_name(movie_id):
    api_key = '0d949a24180760de0dd5d14b53560285'
    
  
   
    watch_name = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    watch_names = watch_name.json()

    
    name = watch_names.get('original_title', '')


    return {
        'names':name,
    }






def fetch_movie_reviews(movie_id):
    api_key = '0d949a24180760de0dd5d14b53560285'
    reviews = []

    try:
       
        reviews_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}')
        reviews_response.raise_for_status()  

        reviews_data = reviews_response.json()

        
        review_results = reviews_data.get('results', [])

       
        for result in review_results:
            if isinstance(result, dict):
                content = result.get('content', '')
                if content:
                    reviews.append(content)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"JSON decoding error: {e}")

    
    if not reviews:
        return {"message": "No reviews found for this movie."}
    
    return {"reviews": reviews}




@app.route('/result')
def result():
    movie_id = request.args.get('movie_id', '')
    return render_template('result.html', movie_id=movie_id)


def fetch_movie_reviews_id(movie_id):
    api_key = '0d949a24180760de0dd5d14b53560285'
    
    
    reviews_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}')
    reviews_response.raise_for_status() 
        
    reviews_data = reviews_response.json()
        
    movie_idd = reviews_data.get('id','')
        
        
    return movie_idd
    
    



def remove_stopwords(text):
    x=[]
    for i in text.split():
        
        if i not in stopwords.words('english'):
            x.append(i)
    y=x[:]
    x.clear()
    return y


y = []
def stem_words(text):
    for i in text:
        y.append(ps.stem(i))
    z=y[:]
    y.clear()
    return z


def clean_html(text):
    """Remove HTML tags from a given text."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def convert_lower(text):
    return text.lower()

def remove_special(text):
    x = ''

    for i in text:
        if i.isalnum():
            x += i
        else:
            x=x+' '

    return x

def join_back(list_input):
    return " ".join(list_input)






@app.route('/api/movie_reviews', methods=['GET'])
def movie_reviews():
    movie_id = request.args.get('movie_id')
    reviews_data = fetch_movie_reviews(movie_id) 

    
    if 'message' in reviews_data:
        movie_name = fetch_movie_name(movie_id)
        return jsonify({
            'movie_name': movie_name,
            'message': reviews_data['message'],
        })

    reviews = reviews_data.get('reviews', [])

    
    first_reviews = reviews[:6]
    original_review = first_reviews.copy()

   
    first_reviews = [clean_html(review) for review in first_reviews]
    first_reviews = [convert_lower(review) for review in first_reviews]
    first_reviews = [remove_special(review) for review in first_reviews]
    first_reviews = [remove_stopwords(review) for review in first_reviews]
    first_reviews = [stem_words(review) for review in first_reviews]
    first_reviews = [join_back(review) for review in first_reviews]

    final = CounttVectorizer.transform(first_reviews).toarray()  
    predictions = movies_reviews.predict(final)

    predictions = ["positive" if p == 1 else "negative" for p in predictions] 

    movie_name = fetch_movie_name(movie_id)

    return jsonify({
        'movie_name': movie_name,
        'original_reviews': original_review,
        'predictions': predictions,
    })





@app.route('/')
def home():
    return render_template('index.html')





@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(movies[['title']].to_dict(orient='records'))



@app.route('/api/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('movie_title')
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommend_movie = []
    recommend_movie_poster = []
    recommended_movie_details = []
    recommend_movie_id = []

    for i in movie_indices:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_movie_id.append(fetch_movie_reviews_id(movie_id))
        recommend_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_details.append(fetch_movie_details(movie_id))

    return jsonify({
        'names': recommend_movie,
        'posters': recommend_movie_poster,
        'details': recommended_movie_details,
        'movie_id': recommend_movie_id,
    })


   

@app.route('/api/ab', methods=['GET'])
def ab():
   
    random_indices = random.sample(range(len(movies)), 10)

    recommended_movie_posters = []
    recommended_movie_details = []

    
    for idx in random_indices:
        movie_id = movies.iloc[idx].movie_id 
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_details.append(fetch_movie_details(movie_id))

    return jsonify({
        'posters': recommended_movie_posters,
        'details': recommended_movie_details
    })


@app.route('/api/recomm', methods=['GET'])
def recomm():


   
    random_indices = random.sample(range(len(movies)), 3)

    recommended_movie_posters = []
    recommeded_movie_details=[]

    for idx in random_indices:
        movie_id = movies.iloc[idx].movie_id 
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommeded_movie_details.append(fetch_movie_details(movie_id))

    return jsonify({
        'posters': recommended_movie_posters,
        'details': recommeded_movie_details
    })


@app.route('/api/reco', methods=['GET'])
def reco():
    
    random_indices = random.sample(range(len(movies)), 10)

    recommended_movie_posters = []
    recommended_movie_details = []

    for idx in random_indices:
        movie_id = movies.iloc[idx].movie_id 
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_details.append(fetch_movie_details(movie_id))

    return jsonify({
        'posters': recommended_movie_posters,
        'details': recommended_movie_details
    })




if __name__ == '__main__':
    app.run(debug=True)
