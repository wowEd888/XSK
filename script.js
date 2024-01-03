
// Function to handle adding and retrieving ratings
class RatingManager {
    constructor() {
        this.ratings = JSON.parse(localStorage.getItem('ratings')) || [];
    }

    addRating(professorName, schoolName, comment) {
        const newRating = { professorName, schoolName, comment };
        this.ratings.push(newRating);
        localStorage.setItem('ratings', JSON.stringify(this.ratings));
        return newRating;
    }

    getRatings() {
        return this.ratings;
    }

    searchRatings(query) {
        return this.ratings.filter(rating => 
            rating.professorName.toLowerCase().includes(query.toLowerCase()) ||
            rating.schoolName.toLowerCase().includes(query.toLowerCase())
        );
    }
}

const ratingManager = new RatingManager();

// Function to display ratings
function displayRatings(ratings) {
    const list = document.getElementById('professor-list');
    list.innerHTML = '';
    ratings.forEach(rating => {
        const item = document.createElement('div');
        item.innerHTML = `
            <h3>${rating.professorName} - ${rating.schoolName}</h3>
            <p>${rating.comment}</p>
        `;
        list.appendChild(item);
    });
}

// Handle form submission
document.getElementById('rating-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const professorName = document.getElementById('professor-name').value;
    const schoolName = document.getElementById('school-name').value;
    const comment = document.getElementById('rating-comment').value;
    const newRating = ratingManager.addRating(professorName, schoolName, comment);
    displayRatings([newRating]);
    document.getElementById('rating-form').reset();
});

// Handle search
document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value;
    const results = ratingManager.searchRatings(query);
    displayRatings(results);
});

// Initially display all ratings
displayRatings(ratingManager.getRatings());
