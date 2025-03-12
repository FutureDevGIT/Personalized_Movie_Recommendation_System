import React from "react";
import { Box } from "@mui/material";
import Recommendations from "./components/Recommendations";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";


const App = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <Navbar />
      <Box sx={{ flex: 1 }}>
        <Recommendations />
      </Box>
      <Footer />
    </Box>
  );
};

export default App;