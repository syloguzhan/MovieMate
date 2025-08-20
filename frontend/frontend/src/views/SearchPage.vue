<template>
  <div>
    <SearchBar @event-search="handleSearch" />
    <SearchResults :search-query="searchQuery" />
  </div>
</template>
<script>
import SearchBar from "@/components/SearchBar.vue";
import SearchResults from "@/components/SearchResults.vue";
export default {
  components: {
    SearchBar,
    SearchResults,
  },
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    handleSearch(searchQuery) {
      this.searchQuery = searchQuery;
    },
  },
};
</script>
