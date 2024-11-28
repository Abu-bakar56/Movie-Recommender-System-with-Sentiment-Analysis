document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const movieId = urlParams.get('movie_id');
    const apiUrl = `/api/movie_reviews?movie_id=${encodeURIComponent(movieId)}`;
    console.log(`Fetching data from: ${apiUrl}`);

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);

       
            const movieName = data.movie_name.names;
            document.getElementById('movieName').textContent = movieName;

            
            const originalReviews = data.original_reviews || [];
            const predictions = data.predictions || [];

            const tableBody = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = '';

            if (data.message) {
       
                const noReviewMessage = document.createElement('tr');
                const cell = document.createElement('td');
                cell.setAttribute('colspan', '2');
                cell.textContent = data.message;
                noReviewMessage.appendChild(cell);
                tableBody.appendChild(noReviewMessage);
            } else if (originalReviews.length === 0) {
            
                const noReviewMessage = document.createElement('tr');
                const cell = document.createElement('td');
                cell.setAttribute('colspan', '2');
                cell.textContent = 'No reviews found';
                noReviewMessage.appendChild(cell);
                tableBody.appendChild(noReviewMessage);
            } else {
              
                originalReviews.forEach((review, index) => {
                    const row = document.createElement('tr');

                    const reviewCell = document.createElement('td');
                    reviewCell.textContent = review;

                    const predictionCell = document.createElement('td');
                    const predictionText = predictions[index] || 'No Prediction';
                    predictionCell.textContent = predictionText;

                    if (predictionText.toLowerCase() === 'positive') {
                        predictionCell.style.backgroundColor = 'lightgreen';
                    } else if (predictionText.toLowerCase() === 'negative') {
                        predictionCell.style.backgroundColor = 'lightcoral';
                    }

                    row.appendChild(reviewCell);
                    row.appendChild(predictionCell);

                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => console.error('Error fetching movie reviews:', error));
});
