<template>
  <div class="new-tvshow">
    <h2>New Released TV Shows</h2>
    <div v-if="loading" class="loading-text">Loading...</div>
    <div v-else class="new-list">
      <div v-for="tvshow in tvshows" :key="tvshow.id" class="tv-card">
        <img :src="tvshow.poster_url" :alt="tvshow.id" class="tv-poster" />
        <h3>{{ tvshow.title }}</h3>
        <p>IMDB:{{ tvshow.imdb_rating }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "NewTVShows",
  data() {
    return {
      loading: true,
      tvshows: [],
    };
  },
  mounted() {
    this.get_new_tvshows();
  },
  methods: {
    get_new_tvshows() {
      axios
        .get("http://localhost:5000/tvshow/new")
        .then((res) => {
          console.log(res.data);
          this.tvshows = res.data;
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
.new-tvshow {
  padding: 34px;
  background-color: #0b175f;
}
h2 {
  margin-bottom: 34px;
  color: #fff;
  font-size: 24px;
  font-weight: 600px;
  text-shadow: 0px 2px 10px rgba(255, 255, 255, 0.5);
  letter-spacing: 1px;
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
.tv-card {
  background-color: #fff;
  width: 200px;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}
.tv-card:hover {
  transform: scale(1.1);
}
.tv-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}
.tv-card h3 {
  font-size: 18px;
  text-align: center;
  font-weight: 600px;
  padding: 10px 0;
}
.tv-card p {
  text-align: center;
  color: #555;
  padding-bottom: 8px;
  font-size: 14px;
}
</style>
