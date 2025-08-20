import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "@/views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import HomePage from "../views/HomePage.vue";
import PopularMovies from "@/components/PopularMovies.vue";
import PopularTVShows from "@/components/PopularTVShows.vue";
import NewMovies from "@/components/NewMovies.vue";
import NewTVShows from "@/components/NewTVShows.vue";
import RandomHighlights from "@/components/RandomHighlights.vue";
import SearchPage from "@/views/SearchPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/movie/popular",
    name: "Popular Movies",
    component: PopularMovies,
  },
  {
    path: "/tvshow/popular",
    name: "Popular TVShows",
    component: PopularTVShows,
  },
  {
    path: "/movie/new",
    name: "New Movies",
    component: NewMovies,
  },
  {
    path: "/tvshow/new",
    name: "New TVShows",
    component: NewTVShows,
  },
  {
    path: "/random",
    name: "Random Highlights",
    component: RandomHighlights,
  },
  {
    path: "/search",
    name: "Search Page",
    component: SearchPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
