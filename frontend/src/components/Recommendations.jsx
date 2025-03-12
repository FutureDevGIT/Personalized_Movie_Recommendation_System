import React, { useState, useCallback } from "react";
import axios from "axios";
import { debounce } from "lodash";
import {
  Container, TextField, Grid, Card, CardMedia,
  CardContent, Typography, CircularProgress, Rating
} from "@mui/material";

const Recommendations = () => {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = useCallback(
    debounce(async (searchQuery) => {
      if (!searchQuery.trim()) return;

      setLoading(true);
      setError(null);

      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/recommend/?title=${searchQuery}`);

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
        {movies.length > 0 ? (
          movies.map((movie, index) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
              <Card sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
                <CardMedia
                  component="img"
                  height="350"
                  image={movie.poster || "https://via.placeholder.com/300"}
                  alt={movie.title}
                  sx={{ objectFit: "cover" }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6">{movie.title}</Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                    {movie.overview.length > 100 ? movie.overview.substring(0, 100) + "..." : movie.overview}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Release Date:</strong> {movie.release_date || "N/A"}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Genres:</strong> {movie.genres ? movie.genres.join(", ") : "N/A"}
                  </Typography>
                  <Rating
                    name="movie-rating"
                    value={movie.rating / 2}
                    precision={0.5}
                    readOnly
                    size="small"
                    sx={{ mt: 1 }}
                  />
                  <Typography variant="body2">
                    <strong>Rating:</strong> {movie.rating || "N/A"}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          !loading && <Typography>No recommendations available.</Typography>
        )}
      </Grid>
    </Container>
  );
};

export default Recommendations;
