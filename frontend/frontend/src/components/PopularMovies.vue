<template>
  <div class="popular-movies">
    <h2>Popular movies</h2>
    <div v-if="loading" class="loading-text">Loading...</div>
    <div v-else class="popular-list">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img :src="movie.poster_url" :alt="movie.title" class="movie-poster" />
        <h3>{{ movie.title }}</h3>
        <p>IMDB:{{ movie.imdb_rating }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "PopularMovies",
  data() {
    return {
      movies: [],
      loading: true,
    };
  },
  mounted() {
    this.get_popular_movie();
  },
  methods: {
    get_popular_movie() {
      axios
        .get("http://localhost:5000/movie/popular")
        .then((response) => {
          console.log(response.data);
          this.movies = response.data;
        })
        .catch((err) => {
          console.error("API HATASI", err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
<style scoped>
h2 {
  margin-bottom: 34px;
}
.popular-movies {
  padding: 20px;
  background-color: #f9f9f9;
}
.popular-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
}
.movie-card {
  background-color: #fff;
  width: 200px;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}
.movie-card:hover {
  transform: scale(1.1);
}
.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}
.movie-card h3 {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  padding: 10px 0;
}
.movie-card p {
  font-size: 14px;
  color: #555;
  text-align: center;
  padding-bottom: 8px;
}
.loading-text {
  font-size: 20px;
}
</style>
