#==================Movie Recommendation System PYTHON FLASK CODE======================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify   #``````````````````````
import random

app = Flask(__name__)   
app.secret_key = 'your-secret-key-here-For flash messages'  # For flash messages

# Initialising the movie database
movies_list = {
    "Action": ["Pokiri", "Magadheera", "Eega", "Baahubali", "Pushpa", "Salaar", "Devara", "RRR", "KGF", "Mirchi"],
    "Adventure": ["Ammoru", "Anji", "Aditya 369", "Hanu-Man", "Bimbisara", "Little Soldiers", "Rajendrudu Gajendrudu", "Aranya", "Kondapolam", "Kalki 2898 AD"],
    "Biopic": ["83", "Saina", "Sardar Udham", "Mary Kom", "Maidaan", "Shershaah", "Major", "Sam Bahadur", "Mission Mangal", "Mahanati"],
    "Comedy": ["Jathi Ratnalu", "DJ Tillu", "MAD", "Tillu Square", "Venky", "Ready", "Maryada Ramanna", "Bhale Bhale Magadivoy", "Yamaleela", "Bunny"],
    "Crime": ["HIT Franchise", "Evaru", "Kshanam", "Goodachari", "Drushyam", "V", "Republic", "Agent Sai Srinivasa Athreya", "Mathu Vadalara", "Gangs of Godavari"],
    "Drama": ["Rangasthalam", "Arjun Reddy", "Jersey", "Pelli Choopulu", "C/O Kancharapalem", "Sita Ramam", "Vedam", "Ala Modalaindi", "Ee Nagaraniki Emaindi", "Godavari"],
    "Family": ["Nuvvu Naaku Nachchav", "Murari", "Sankranti", "Gopala Gopala", "Seethamma Vakitlo Sirimalle Chettu", "Malleswari", "Swayam Krushi", "Aha Naa Pellanta", "Jamba Lakidi Pamba", "Chitram! Bhalare Vichitram!!"],
    "Patriotic": ["Subrahmanyapuram", "Sye Raa Narasimha Reddy", "Kanche", "Major", "Sam Bahadur", "Shershaah", "Mission Mangal", "Gandhi, My Father", "The Kashmir Files", "Uri: The Surgical Strike"],
    "Historical": ["Baahubali", "Sye Raa Narasimha Reddy", "Rudhramadevi", "Kanche", "Ponniyin Selvan", "Gautamiputra Satakarni", "Kurukshetra", "Raajadhani", "Alluri Seetharama Raju", "Sri Krishna Pandaveeyam"],
    "Horror": ["Arundhati", "Raju Gari Gadhi", "Maya", "Kanchana", "Shyam Singha Roy", "Masooda", "Ekkadiki Pothavu Chinnavada", "Deyyam", "Rathri", "Avunu"],
    "Musical": ["Shankarabharanam", "Sagara Sangamam", "Mithunam", "Gang Leader", "Siri Vennela", "Geethanjali", "Kokila", "Siri Siri Muvva", "Manmadhudu", "Nuvve Nuvve"],
    "Mystery": ["Anveshana", "Rahasya", "Kshanam", "Agent Sai Srinivasa Athreya", "Evaru", "V", "HIT Franchise", "Maya", "Avunu", "Gamyam"],
    "Romance": ["Geethanjali", "Ala Modalaindi", "Sita Ramam", "Nuvve Nuvve", "Manmadhudu", "Ye Maya Chesave", "Tholi Prema", "Premam", "Arjun Reddy", "Padi Padi Leche Manasu"],
    "Science Fiction": ["Kalki 2898 AD", "Robot", "Eega", "Indra", "Kaala", "24", "Action", "Aditya 369", "Rajendrudu Gajendrudu", "Oke Oka Jeevitham"],
    "Sports": ["Jersey", "Sye", "Goal", "Malleswari", "Haathi Mere Saathi", "Gundello Godari", "Kanaa", "Chak De! India", "Million Dollar Arm", "Sultan"],
    "Thriller": ["HIT Franchise", "V", "Evaru", "Kshanam", "Goodachari", "Drushyam", "Gamyam", "Anveshana", "Dhruva", "Temper"],
    "War": ["Kanche", "Sye Raa Narasimha Reddy", "Alluri Seetharama Raju", "Saaho", "KGF", "Baahubali", "RRR", "Shershaah", "Uri: The Surgical Strike", "Major"]
}

# ===== HOME PAGE =====
@app.route('/')
def home():
    context = {
        'welcome_message': "Welcome to the Movie Recommendation System!!!!!",
        'genre_list': list(movies_list.keys()),
        'total_movies': sum(len(movies) for movies in movies_list.values()),
        'site_name': "Movie Recommender",
        'year': 2026
    }
    return render_template('index.html', **context)   # **context unpacks the dictionary into keyword arguments automatically  #index.html

#===== RECOMMENDATIONS (get_recommendations function) =====
@app.route('/recommend', methods=['GET', 'POST'])
def get_recommendations():
    if request.method == 'POST':
        genre_choice = request.form.get('genre')

        # Handle empty input
        if not genre_choice:
            flash("Please select a genre! Genre can't be empty!!!!!")
            return redirect(url_for('get_recommendations'))
        
        # Case-insensitive genre matching
        matching_genre = next((genre for genre in movies_list.keys() if genre.lower() == genre_choice.lower()), None)

        if matching_genre:
            # Validate number type input
            try:
                num_recommendations = int(request.form.get('num_recommendations', 3))
            except ValueError:
                flash("Please enter a valid number!")
                return redirect(url_for('get_recommendations')) 

            # Validate positive number
            if num_recommendations <= 0:
                flash("Please enter a positive number!") 
                return redirect(url_for('get_recommendations'))          
                
            movies = movies_list[matching_genre]

            if movies:
                # Handle request for more movies than available
                if num_recommendations > len(movies):
                    flash(f'Only {len(movies)} movies available. Showing all....')
                    recommendations = random.sample(movies, len(movies))                   
                else:
                    recommendations = random.sample(movies, num_recommendations)

                # Return recommendations to a template instead of printing--------------------------recommendations.html         
                return render_template('recommendations.html', 
                                     genre=matching_genre,
                                     movies=recommendations,
                                     count=len(recommendations),
                                     requested=num_recommendations)                      
                      
            else:
                flash(f"\nNo movies available in {matching_genre} genre yet.")
        else:
            flash(f'{matching_genre} Genre not found!')
            return redirect(url_for('get_recommendations'))

    # GET request - show the form
    genre_list = list(movies_list.keys())
    return render_template('recommend_form.html', genres=genre_list)

# ===== ADD MOVIE (Your add_new_movie function) =====
@app.route('/add', methods=['GET', 'POST'])
def add_new_movie():
    if request.method == 'POST':
        genre_name= request.form.get('genre')

        if not genre_name:
            flash("Please select a genre! Genre can't be empty!!!!!")
            return redirect(url_for('add_new_movie'))

        # Case-insensitive genre matching
        matching_genre = next((genre for genre in movies_list.keys() if genre.lower() == genre_name.lower()), None)

        if matching_genre:
            # Handle empty movie name
            movie_name = request.form.get('movie_name', '').strip()
            
            if not movie_name:
                flash('Movie name cannot be empty!')
                return redirect(url_for('add_new_movie'))           
            # Case-insensitive check
            if movie_name.lower() in (movie.lower() for movie in movies_list[matching_genre]):
                flash(f'"{movie_name}" already exists in {matching_genre}!')
            else:
                movies_list[matching_genre].append(movie_name)
                flash(f'"{movie_name}" successfully added to {matching_genre}!')
        else:
            flash(f'{matching_genre} Genre not found!')
            return redirect(url_for('add_new_movie'))

        return redirect(url_for('add_new_movie'))
    # GET request - show the form
    genre_list = list(movies_list.keys())
    return render_template('add_movie.html', genres=genre_list)

# ===== SEARCH MOVIE (Your search_movie function) =====
@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    if request.method == 'POST':
        # Handle empty search
        search_term = request.form.get("search_term", "").strip().lower()
        if not search_term:
            flash("Search term cannot be empty!")
            return redirect(url_for('search_movie'))
        # Show all genres where movie appears
        found_in = []
        for genre, movies in movies_list.items():
            if search_term in (movie.lower() for movie in movies):
                found_in.append(genre)
        if found_in:
            return render_template('search_results.html', 
                             search_term=search_term,
                             found_in=found_in)
        else:
            flash(f"\nNo movie found with the name '{search_term}'")
            return redirect(url_for('search_movie'))
    
    # GET request - show the search form
    return render_template('search.html')

# ===== VIEW ALL MOVIES =====
@app.route('/all')
def view_all():
    return render_template('all_movies.html', movies_list=movies_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)