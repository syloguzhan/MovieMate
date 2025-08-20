<template>
  <div class="homepage">
    <RandomHighlights />
    <NewMovies />
    <NewTVShows />
    <PopularMovies />
    <PopularTVShows />
  </div>
</template>
<script>
import NewMovies from "@/components/NewMovies.vue";
import NewTVShows from "@/components/NewTVShows.vue";
import PopularMovies from "@/components/PopularMovies.vue";
import PopularTVShows from "@/components/PopularTVShows.vue";
import RandomHighlights from "@/components/RandomHighlights.vue";
export default {
  name: "HomePage",
  components: {
    PopularMovies,
    PopularTVShows,
    NewMovies,
    NewTVShows,
    RandomHighlights,
  },
};
</script>
<style scoped></style>
