// Conteneur où on affiche les films
const container = document.getElementById("movies-container");

// Bouton "Charger plus"
const loadMoreButton = document.getElementById("load-more");

// Clé API OMDb 
const API_KEY = "11441893";

// Liste des films tendances
const movieTitles = [
  "john wick",
  "Spider-Man Into the Spider-Verse",
  "Avengers Infinity War",
  "creed",
  "kingsman the secret service",
  "jumanji welcome to the jungle",
  "Now you see me",
  "Deadpool",
  "my hero academia two heroes"
];

// Tableau qui stockera tous les films récupérés
let allMovies = [];

// Nombre de films actuellement affichés
let displayedCount = 3;


// ===============================
// 2. RÉCUPÉRATION DES FILMS (FETCH)
// ===============================

const fetchPromises = movieTitles.map(title => {
  const url = `https://www.omdbapi.com/?apikey=${API_KEY}&t=${encodeURIComponent(title)}`;
  return fetch(url).then(response => response.json());
});

Promise.all(fetchPromises)
  .then(movies => {
    // On garde uniquement les films valides
    allMovies = movies.filter(movie => movie.Response === "True");

    // Affichage initial
    displayMovies();
  })
  .catch(error => {
    console.error("Erreur lors du chargement des films :", error);
  });


// ===============================
// 3. FONCTION D’AFFICHAGE DES FILMS
// ===============================

function displayMovies() {
  container.innerHTML = "";

  allMovies.slice(0, displayedCount).forEach(movie => {
    const article = document.createElement("article");

    article.innerHTML = `
      <img src="${movie.Poster}" alt="Affiche du film ${movie.Title}">
      <h3>${movie.Title}</h3>
      <a href="movie.html?id=${movie.imdbID}">Voir plus</a>
    `;

    container.appendChild(article);
  });

  // Masquer le bouton si tous les films sont affichés
  if (displayedCount >= allMovies.length) {
    loadMoreButton.style.display = "none";
  }
}


// ===============================
// 4. BOUTON "CHARGER PLUS"
// ===============================

if (loadMoreButton) {
  loadMoreButton.addEventListener("click", () => {
    displayedCount += 3;
    displayMovies();
  });
}
