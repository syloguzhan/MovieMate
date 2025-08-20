<template>
  <div class="popular-tvshows">
    <h2>Popular TVShows</h2>
    <div v-if="loading" class="loading-text">Loading...</div>
    <div v-else class="popular-list">
      <div v-for="tvshow in tvshows" :key="tvshow.id" class="tvshow-card">
        <img
          :src="tvshow.poster_url"
          :alt="tvshow.title"
          class="tvshow-poster"
        />
        <h3>{{ tvshow.title }}</h3>
        <p>IMDB:{{ tvshow.imdb_rating }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "PopularTVShows",
  data() {
    return {
      tvshows: [],
      loading: true,
    };
  },
  mounted() {
    this.get_popular_tvshows();
  },
  methods: {
    get_popular_tvshows() {
      axios
        .get("http://localhost:5000/tvshow/popular")
        .then((response) => {
          this.tvshows = response.data;
          console.log(response.data);
        })
        .catch((error) => {
          console.error("API Hatasi", error);
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
  color: #fff;
  font-size: 24px;
  font-weight: 600px;
  text-shadow: 0px 2px 10px rgba(255, 255, 255, 0.5);
  letter-spacing: 1px;
}
.popular-tvshows {
  padding: 20px;
  background-color: #0b175f;
}
.popular-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
}
.tvshow-card {
  background-color: #fff;
  width: 200px;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}
.tvshow-card:hover {
  transform: scale(1.1);
}
.tvshow-poster {
  object-fit: cover;
  height: 300px;
  width: 100%;
}
.tvshow-card h3 {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  padding: 10px 0;
}
.tvshow-card p {
  color: #555;
  text-align: center;
  font-size: 14px;
  padding-bottom: 8px;
}
.loading-text {
  font-size: 20px;
}
</style>
