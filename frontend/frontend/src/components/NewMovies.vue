<template>
  <div class="new-movies">
    <h2>New Released Movies</h2>
    <div v-if="loading" class="loading-text">Loading...</div>
    <div v-else class="new-list">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img :src="movie.poster_url" :alt="movie.id" class="movie-poster" />
        <h3>{{ movie.title }}</h3>
        <p>IMDB:{{ movie.imdb_rating }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "NewMovies",
  data() {
    return {
      loading: true,
      movies: [],
    };
  },
  mounted() {
    this.get_new_movies();
  },
  methods: {
    get_new_movies() {
      axios
        .get("http://localhost:5000/movie/new")
        .then((response) => {
          console.log(response.data);
          this.movies = response.data;
        })
        .catch((err) => {
          console.error("API Error", err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
<style scoped>
.new-movies {
  padding: 20px;
  background-color: #f9f9f9;
}
h2 {
  margin-bottom: 34px;
}
.loading-text {
  font-size: 20px;
}
.new-list {
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
  text-align: center;
  font-weight: 600px;
  padding: 10px 0;
}
.movie-card p {
  text-align: center;
  color: #555;
  padding-bottom: 8px;
  font-size: 14px;
}
</style>
