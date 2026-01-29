const API_KEY = "11441893"; // Ta clé OMDb
const searchInput = document.getElementById("searchInput");
const resultsContainer = document.getElementById("resultsContainer");
const loadMoreBtn = document.getElementById("loadMore");

let timeout = null; // debounce
let currentQuery = ""; // requête actuelle
let currentPage = 1;   // page OMDb

// Fonction pour afficher les films
function displayMovies(movies, reset = false) {
  if (reset) resultsContainer.innerHTML = ""; // vider les anciens résultats si nouvelle recherche

  if (!movies || movies.length === 0) {
    if (reset) resultsContainer.innerHTML = "<p>Aucun résultat trouvé</p>";
    return;
  }

  movies.forEach(movie => {
    const article = document.createElement("article");
    article.innerHTML = `
      <img src="${movie.Poster !== "N/A" ? movie.Poster : ''}" alt="Affiche ${movie.Title}">
      <h3>${movie.Title}</h3>
      <p>${movie.Year}</p>
      <a href="movie.html?id=${movie.imdbID}">Voir plus</a>
    `;
    resultsContainer.appendChild(article);
  });
}

// Fonction pour appeler l'API OMDb avec pagination
async function fetchMovies(query, page = 1) {
  try {
    const response = await fetch(`https://www.omdbapi.com/?apikey=${API_KEY}&s=${encodeURIComponent(query)}&page=${page}`);
    const data = await response.json();

    if (data.Response === "True") {
      displayMovies(data.Search, page === 1); // si page 1 => reset
      // Vérifier si on peut afficher "Charger plus"
      loadMoreBtn.style.display = (page * 10 < parseInt(data.totalResults)) ? "block" : "none";
    } else {
      displayMovies([], page === 1);
      loadMoreBtn.style.display = "none";
    }
  } catch (error) {
    console.error("Erreur lors de l'appel API :", error);
  }
}

// Recherche en temps réel avec debounce
searchInput.addEventListener("input", () => {
  const query = searchInput.value.trim();
  clearTimeout(timeout);

  if (query.length > 0) {
    timeout = setTimeout(() => {
      currentQuery = query;
      currentPage = 1;
      fetchMovies(currentQuery, currentPage);
    }, 300); // 300ms après la dernière frappe
  } else {
    resultsContainer.innerHTML = "";
    loadMoreBtn.style.display = "none";
  }
});

// Événement bouton "Charger plus"
loadMoreBtn.addEventListener("click", () => {
  currentPage++;
  fetchMovies(currentQuery, currentPage);
});
