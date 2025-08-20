<template>
  <div class="random-highlights">
    <h2>Random Highlights</h2>
    <div v-if="loading">Loading...</div>
    <div v-else class="highlight-list">
      <div class="highlight-card">
        <img :src="movie.poster_url" :alt="movie.id" />
        <p>{{ movie.title }}</p>
        <p>IMDB: {{ movie.imdb_rating }}</p>
      </div>
      <div class="highlight-card">
        <img :src="tvShow.poster_url" :alt="tvShow.id" />
        <p>{{ tvShow.title }}</p>
        <p>{{ tvShow.imdb_rating }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "RandomHighlishts",
  data() {
    return {
      movie: {},
      tvShow: {},
      loading: true,
    };
  },
  mounted() {
    this.fetchRandomData();
  },
  methods: {
    fetchRandomData() {
      const movieRequest = axios.get("http://localhost:5000/movie/random");
      const tvShowRequest = axios.get("http://localhost:5000/tvshow/random");

      Promise.all([movieRequest, tvShowRequest])
        .then(([movieResponse, tvShowResponse]) => {
          this.movie = movieResponse.data;
          this.tvShow = tvShowResponse.data;
        })
        .catch((error) => {
          console.error("API Error", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
<style scoped>
.random-highlights {
  padding: 40px 20px;
  background-color: #0b175f;
}
.random-highlights h2 {
  text-align: center;
  margin-bottom: 50px;
  font-size: 28px;
  font-weight: bold;
}
.highlight-list {
  display: flex;
  gap: 100px;
  justify-content: center;
  flex-wrap: wrap;
}
.highlight-card {
  background-color: #fff;
  border-radius: 10px;
  width: 280px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  overflow: hidden;
  transition: transform 0.3s ease;
}
.highlight-card:hover {
  transform: scale(1.05);
}
.highlight-card img {
  object-fit: cover;
  width: 100%;
  height: 400px;
  border-bottom: 1px solid #eee;
}
.highlight-card h3 {
  font-size: 20px;
  margin: 10px 0 4px;
}
.highlight-card p {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}
.random-highlights h2 {
  font-size: 30px;
  font-weight: 600px;
  text-align: center;
  color: #fff;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.5);
  margin-bottom: 50px;
  letter-spacing: 1px;
}
</style>
