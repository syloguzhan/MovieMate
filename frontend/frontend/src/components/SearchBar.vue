<template>
  <div class="search-bar">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Enter movie or tvshow ?"
      @keyup.enter="search"
    />
    <button class="search-button" @click="search">Search</button>
  </div>
</template>
<script>
export default {
  name: "SearchBar",
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    search() {
      this.$emit("event-search", this.searchQuery);
    },
  },
};
</script>
<style scoped>
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  box-shadow: none;
  border: none;
  margin-top: 10px;
  background-color: white;
}

input[type="text"] {
  height: 42px;
  width: 250px;
  padding: 0 12px;
  font-size: 16px;
  border: 2px solid #2b03b0;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus {
  border-color: #4a35f0;
}

.search-button {
  height: 42px;
  padding: 0 16px;
  background-color: #2b03b0;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.search-button:hover {
  background-color: #3a25d3;
}
</style>
