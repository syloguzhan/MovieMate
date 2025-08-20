<template>
  <div class="result-cards">
    <div v-if="loading" class="loading-text">Loading...</div>
    <div v-else-if="results.length === 0">No results found</div>
    <div v-else class="search-card-list">
      <div v-for="result in results" :key="result.id" class="search-card">
        <img :src="result.poster_url" :alt="result.title" class="card-poster" />
        <h3>{{ result.title }}</h3>
        <p>IMDB:{{ result.imdb_rating }}</p>
        <button
          @click="markAsWatched(result)"
          class="mark-button"
          :disabled="isWatched(result)"
        >
          👁 Watched
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { useToast } from "vue-toastification";
export default {
  name: "SearchResults",
  props: ["searchQuery"],
  data() {
    return {
      results: [],
      loading: true,
      toast: null,
      watched: true,
      watchedMovies: [],
      watchedTvshows: [],
    };
  },
  mounted() {
    this.fetchResult();
    this.toast = useToast();
    this.get_watched_list();
  },
  watch: {
    searchQuery() {
      this.fetchResult();
      this.get_watched_list();
    },
  },
  methods: {
    fetchResult() {
      if (!this.searchQuery || this.searchQuery.trim() === "") {
        this.results = [];
        this.loading = false;
        return;
      }

      this.loading = true;
      axios
        .get(`http://localhost:5000/search?query=${this.searchQuery}`)
        .then((res) => {
          const movies = res.data.movies || [];
          const tvshows = res.data.tvshows || [];
          this.results = [...movies, ...tvshows];
        })
        .catch((err) => {
          console.error("API Error", err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    markAsWatched(result) {
      const token = localStorage.getItem("token");
      if (!token) {
        this.toast.error("Please log in to add movies and series !", {
          setTimeout: 1500,
          pauseOnHover: false,
        });
        this.$router.push("/login");
        return;
      }

      let payload = {};
      if (result.type === "movie") {
        payload.movie_id = result.id;
      } else if (result.type === "tvshow") {
        payload.tv_show_id = result.id;
      }

      console.log("");
      axios
        .post("http://localhost:5000/watch-history/add", payload, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(() => {
          alert("Watch history succesfully added");
          if (result.type === "movie") {
            this.watchedMovies.push(result.id);
          } else if (result.type === "tvshow") {
            this.watchedTvshows.push(result.id);
          }
        })
        .catch((err) => {
          console.error("API Error", err);
        });
    },
    get_watched_list() {
      const token = localStorage.getItem("token");
      if (!token) {
        console.warn("No token found,user not logged in");
      }
      axios
        .get("http://localhost:5000/watch-history/list", {
          headers: {
            Authorization: `Bearer ${token} `,
          },
        })
        .then((res) => {
          console.log(res.data);
          this.watchedMovies = res.data.movies;
          this.watchedTvshows = res.data.tvshows;
        })
        .catch((error) => {
          console.error("API Error", error);
        })
        .finally(() => {});
    },
    isWatched(result) {
      if (result.type === "movie") {
        return this.watchedMovies.includes(result.id);
      } else if (result.type === "tvshow") {
        return this.watchedTvshows.includes(result.id);
      } else {
        return false;
      }
    },
  },
};
</script>
<style scoped>
.result-cards {
  padding: 20px;
  background-color: #f9f9f9;
  justify-content: center;
  padding: 20px;
}
.loading-text {
  font-size: 20px;
  text-align: center;
  color: #555;
}
.search-card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 45px;
}
.search-card {
  background-color: rgb(231, 232, 236);
  border-radius: 8px;
  box-shadow: 0 2px rgba(0, 0, 0, 0.1);
  padding: 10px;
  text-align: center;
  transition: transform 0.2s ease;
  width: 100%;
  max-width: 220px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
@media (max-width: 600px) {
  .search-card {
    max-width: 100%;
  }
}
.search-card:hover {
  transform: translateY(-20px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}
.card-poster {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}
.search-card h3 {
  font-size: 18px;
  margin: 5px 0;
  color: #222;
}
.search-card p {
  font-size: 14px;
  color: #666;
}
.search-card image {
  width: 100%;
  height: auto;
}
.mark-button {
  cursor: pointer;
  background-color: #18be73;
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  font-weight: 500;
  margin-top: auto;
  transition: background-color 0.3s ease;
}
.mark-button:hover {
  background-color: #369f6b;
}
</style>
