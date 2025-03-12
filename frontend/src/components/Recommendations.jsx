import React, { useState, useCallback } from "react";
import axios from "axios";
import { debounce } from "lodash";
import {
  Container, Autocomplete, TextField, Grid, Card, CardMedia,
  CardContent, Typography, CircularProgress, Rating
} from "@mui/material";
import { motion } from "framer-motion";

const API_KEY = "20638e64d55d4bead3f42793f5551c6e";

const Recommendations = () => {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [suggestions, setSuggestions] = useState([]);

  // Fetch movie suggestions from TMDb API
  const fetchSuggestions = useCallback(
    debounce(async (searchQuery) => {
      if (!searchQuery.trim()) return;

      try {
        const response = await axios.get(`https://api.themoviedb.org/3/search/movie`, {
          params: {
            api_key: API_KEY,
            query: searchQuery,
            language: "en-US",
            page: 1
          }
        });

        if (response.data.results) {
          // Store both ID and title to avoid duplicate keys issue
          setSuggestions(response.data.results.map(movie => ({ id: movie.id, title: movie.title })));
        }
      } catch (err) {
        console.error("Error fetching movie suggestions:", err);
      }
    }, 300),
    []
  );

  // Fetch recommendations from backend
  const fetchRecommendations = async (selectedMovie) => {
    if (!selectedMovie) return;

    setLoading(true);
    setError(null);

    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/recommend/?title=${selectedMovie}`);

        if (response.data && response.data.recommendations) {
            setMovies(response.data.recommendations);
        } else {
            setMovies([]);
            setError("No recommendations found.");
        }
    } catch (err) {
        setError("Failed to fetch recommendations. Please try again.");
        console.error("API Error:", err);
    } finally {
        setLoading(false);
    }
};

  return (
    <motion.div initial={{ x: -50, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ duration: 0.6 }}>
      <Container sx={{ mt: 4, pb: 10 }}>
        {/* Autocomplete Search Bar */}
        <Autocomplete
          freeSolo
          options={suggestions}
          getOptionLabel={(option) => option.title} // Display movie title
          onInputChange={(event, value) => {
            setQuery(value);
            fetchSuggestions(value);
          }}
          onChange={(event, newValue) => {
            if (newValue) {
              setQuery(newValue.title);
              fetchRecommendations(newValue.title); // Fetch recommendations on selection
            }
          }}
          renderInput={(params) => (
            <TextField {...params} label="Search for a Movie" variant="outlined" fullWidth sx={{ marginBottom: 2 }} />
          )}
        />

        {loading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ repeat: Infinity, duration: 1 }}>
            <CircularProgress />
          </motion.div>
        )}

        {error && (
          <motion.div animate={{ x: [0, -5, 5, 0] }} transition={{ duration: 0.3 }}>
            <Typography color="error">{error}</Typography>
          </motion.div>
        )}

        {/* Movie Recommendations Grid */}
        <Grid container spacing={3} sx={{ marginTop: 2 }}>
          {movies.length > 0 ? (
            movies.map((movie, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={`${movie.title}-${index}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ scale: 1.05, boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)" }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                <Card sx={{ height: "100%", overflow: "hidden" }}>
                  <CardMedia
                    component="img"
                    height="300"
                    image={movie.poster || "https://via.placeholder.com/300"}
                    alt={movie.title}
                    sx={{ objectFit: "cover", transition: "0.3s" }}
                  />
                  <CardContent>
                    <motion.div whileHover={{ y: -5 }}>
                      <Typography variant="h6">{movie.title}</Typography>
                    </motion.div>
                    <Typography variant="body2" color="textSecondary">
                      {movie.overview.length > 100 ? movie.overview.substring(0, 100) + "..." : movie.overview}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Release Date:</strong> {movie.release_date}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Rating:</strong> ⭐ {movie.rating}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Genres:</strong> {Array.isArray(movie.genres) ? movie.genres.join(", ") : "N/A"}
                    </Typography>
                  </CardContent>
                </Card>
                </motion.div>
              </Grid>
            ))
          ) : (
            !loading && <Typography>No recommendations available.</Typography>
          )}
        </Grid>

      </Container>
    </motion.div>
  );
};

export default Recommendations;
