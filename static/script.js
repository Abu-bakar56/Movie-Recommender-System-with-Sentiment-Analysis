document.addEventListener("DOMContentLoaded", function () {
  const movieSelect = document.getElementById("movieSelect");
  const recommendBtn = document.getElementById("recommendBtn");

  const resultCols = [
      document.getElementById("col1"),
      document.getElementById("col2"),
      document.getElementById("col3"),
      document.getElementById("col4"),
      document.getElementById("col5"),
      document.getElementById("col6"),
  ];

 
  fetch("/api/movies")
      .then((response) => response.json())
      .then((data) => {
          data.forEach((movie) => {
              const option = document.createElement("option");
              option.value = movie.title;
              option.textContent = movie.title;
              movieSelect.appendChild(option);
          });
      })
      .catch((error) => {
          console.error("Error fetching movies:", error);
      });

  if (recommendBtn) {
      recommendBtn.addEventListener("click", () => {
          const selectedMovie = movieSelect.value;

          fetch(`/api/recommend?movie_title=${encodeURIComponent(selectedMovie)}`)
              .then((response) => response.json())
              .then((data) => {
                  const { names, posters, details
                    ,
                     movie_id 
                    } = data;

                  resultCols.forEach((col, index) => {
                      if (names[index] && posters[index] && details[index]
                         && movie_id[index]
                        ) {
                          const { watch } = details[index] || {};
                          const posterUrl = posters[index];

                          col.innerHTML = `
                              <div class="card mb-4">
                                  <img src="${posterUrl}" class="card-img-top" alt="${names[index]}">
                                  <div class="card-body">
                                      <h5 class="card-title" style="font-size:1.5rem;">${names[index]}</h5>
                                      <a href="${watch || "#"}" class="btn" style="margin-top:20px;" target="_blank">Watch</a>
                                      <button class="btn analysis-btn" data-movie="${movie_id[index]}" style="margin-top:20px; margin-left:20px;">Analysis</button>
                                  </div>
                              </div>
                          `;
                      } else {
                          col.innerHTML = "";
                      }
                  });
              })
              .catch((error) => {
                  console.error("Error fetching recommendations:", error);
              });
      });
  }

  

      document.addEventListener("click", (event) => {
        if (event.target && event.target.classList.contains("analysis-btn")) {
            const movieId = event.target.getAttribute("data-movie");
            window.location.href = `/result?movie_id=${movieId}`;
        }
    });
    
});


fetch("/api/recomm")
  .then((response) => response.json())
  .then((data) => {
    const postersDiv = document.getElementById("posters");
    postersDiv.innerHTML = "";

    const posters = data.posters;
    const details = data.details;

    posters.forEach((posterUrl, index) => {
      const { watch } = details[index] || {};

      const posterDiv = document.createElement("a");
      posterDiv.className = "poster";
      posterDiv.href = watch || "#";

      const img = document.createElement("img");
      img.src = posterUrl;
      img.style.cursor = "pointer";
      posterDiv.appendChild(img);
      postersDiv.appendChild(posterDiv);
    });
  })


fetch("/api/recomm")
  .then((response) => response.json())
  .then((data) => {
    const postersDiv = document.getElementById("sters");
    postersDiv.innerHTML = "";

    const posters = data.posters;
    const details = data.details;

    posters.forEach((posterUrl, index) => {
      const { watch } = details[index] || {};

      const posterDiv = document.createElement("a");
      posterDiv.className = "poster";
      posterDiv.href = watch || "#";

      const img = document.createElement("img");
      img.src = posterUrl;
      img.style.cursor = "pointer";
      posterDiv.appendChild(img);
      postersDiv.appendChild(posterDiv);
    });
  })

function updatePost() {
  fetch("/api/reco")
    .then((response) => response.json())
    .then((data) => {
      const postersDiv = document.getElementById("posterrr");

      postersDiv.innerHTML = "";

      const { posters, details } = data;

      posters.forEach((posterUrl, index) => {
        const { watch } = details[index] || {};

        const posterDiv = document.createElement("a");
        posterDiv.className = "er";
        posterDiv.href = watch || "#";

        const img = document.createElement("img");
        img.src = posterUrl;
        img.style.cursor = "pointer";
        posterDiv.appendChild(img);
        postersDiv.appendChild(posterDiv);
      });

      const postersClone = postersDiv.cloneNode(true);
      postersDiv.parentNode.appendChild(postersClone);
    })

}

setInterval(updatePost, 50000);

updatePost();

function updatePosters() {
  fetch("/api/ab")
    .then((response) => response.json())
    .then((data) => {
      const postersDiv = document.getElementById("post");

      postersDiv.innerHTML = "";

      const { posters, details } = data;

      posters.forEach((posterUrl, index) => {
        const { watch } = details[index] || {};

        const posterDiv = document.createElement("a");
        posterDiv.className = "er";
        posterDiv.href = watch || "#";

        const img = document.createElement("img");
        img.src = posterUrl;
        img.style.cursor = "pointer";
        posterDiv.appendChild(img);
        postersDiv.appendChild(posterDiv);
      });

      const postersClone = postersDiv.cloneNode(true);
      postersDiv.parentNode.appendChild(postersClone);
    })

}

setInterval(updatePosters, 50000);

updatePosters();
