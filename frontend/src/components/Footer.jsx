import React from "react";
import { Box, Typography } from "@mui/material";

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        position: "fixed",
        bottom: 0,
        left: 0,
        width: "100%",
        backgroundColor: "#1e1e1e",
        color: "#fff",
        textAlign: "center",
        padding: "10px 0",
        zIndex: 1000,
        animation: "slideUp 0.5s ease-in-out",
        "@keyframes slideUp": {
          from: { transform: "translateY(50px)", opacity: 0 },
          to: { transform: "translateY(0)", opacity: 1 },
        },
      }}
    >
      <Typography variant="body2">
        © {new Date().getFullYear()} Movie Recommender | Built with ❤️ by Mayank
      </Typography>
    </Box>
  );
};

export default Footer;
