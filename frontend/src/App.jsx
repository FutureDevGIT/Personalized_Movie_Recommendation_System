import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Recommendations from "./components/Recommendations";
import Navbar from "./components/Navbar";

const App = () => {
  return (
    <>
      <Navbar />
      <Recommendations />
    </>
  );
};

export default App;
