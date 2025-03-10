import React, { useContext } from "react";
import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import { ThemeContext } from "../context/ThemeContext";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";

const Navbar = () => {
    const { darkMode, setDarkMode } = useContext(ThemeContext);

    return (
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Movie Recommender
            </Typography>

            <IconButton color="inherit" onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>
      );
    };

    export default Navbar;
