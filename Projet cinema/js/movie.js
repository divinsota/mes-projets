const API_KEY = "11441893"; // Ta clé OMDb

// Récupérer l'ID du film depuis l'URL
const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");

// Sélecteurs DOM
const titleEl = document.getElementById("movieTitle");
const posterEl = document.getElementById("moviePoster");
const plotEl = document.getElementById("moviePlot");
const genreEl = document.getElementById("movieGenre");
const actorsEl = document.getElementById("movieActors");
const ratingsEl = document.getElementById("movieRatings");
const dvdEl = document.getElementById("movieDVD");

// Formater la date en jj/mm/aaaa
function formatDateFR(dateStr) {
  if (!dateStr || dateStr === "N/A") return "Non disponible";
  const date = new Date(dateStr);
  return `${date.getDate().toString().padStart(2,"0")}/${(date.getMonth()+1).toString().padStart(2,"0")}/${date.getFullYear()}`;
}

// Afficher les infos du film depuis OMDb
function displayMovie(movie) {
  titleEl.textContent = movie.Title || "Non disponible";
  posterEl.src = movie.Poster !== "N/A" ? movie.Poster : "";
  posterEl.alt = `Poster de ${movie.Title}`;
  plotEl.textContent = movie.Plot || "Résumé non disponible";
  genreEl.textContent = movie.Genre || "Non disponible";
  actorsEl.textContent = movie.Actors || "Non disponible";

  // Notes
  if (movie.Ratings && movie.Ratings.length > 0) {
    ratingsEl.textContent = movie.Ratings.map(r => `${r.Source}: ${r.Value}`).join(", ");
  } else {
    ratingsEl.textContent = "Non disponible";
  }

  dvdEl.textContent = formatDateFR(movie.DVD);
}

// Appel API OMDb
async function fetchMovieDetails(id) {
  if (!id) {
    alert("Aucun film sélectionné !");
    return;
  }

  try {
    const response = await fetch(`https://www.omdbapi.com/?apikey=${API_KEY}&i=${id}&plot=full`);
    const data = await response.json();
    if (data.Response === "True") {
      displayMovie(data);
    } else {
      alert("Film introuvable !");
    }
  } catch (error) {
    console.error("Erreur lors de l'appel API :", error);
  }
}

// Lancer la récupération dès le chargement
fetchMovieDetails(movieId);

