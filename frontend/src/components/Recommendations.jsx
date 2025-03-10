import React, { useState, useCallback } from "react";
import axios from "axios";
import { debounce } from "lodash";
import { Container, TextField, Grid, Card, CardMedia, CardContent, Typography, CircularProgress } from "@mui/material";

const Recommendations = () => {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = useCallback(
    debounce(async (searchQuery) => {
      if (!searchQuery) return;
      setLoading(true);
      setError(null);

      try {
        const response = await axios.get(`/api/recommend/?title=${searchQuery}`);
        setMovies(response.data);
      } catch (err) {
        setError("Failed to fetch recommendations. Please try again.");
        console.error("API Error:", err);
      } finally {
        setLoading(false);
      }
    }, 500),
    []
  );

  const handleChange = (e) => {
    setQuery(e.target.value);
    fetchRecommendations(e.target.value);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <TextField
        label="Search for a Movie"
        variant="outlined"
        fullWidth
        value={query}
        onChange={handleChange}
        sx={{ marginBottom: 2 }}
      />

      {loading && <CircularProgress />}
      {error && <Typography color="error">{error}</Typography>}

      <Grid container spacing={3} sx={{ marginTop: 2 }}>
        {movies.map((movie, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <Card sx={{ height: "100%" }}>
              <CardMedia
                component="img"
                height="300"
                image={movie.poster_url || "https://via.placeholder.com/300"}
                alt={movie.title}
                sx={{ objectFit: "cover" }}
              />
              <CardContent>
                <Typography variant="h6">{movie.title}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {movie.overview.length > 100 ? movie.overview.substring(0, 100) + "..." : movie.overview}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Recommendations;
