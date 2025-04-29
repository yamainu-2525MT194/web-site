// src/App.js
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage    from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";  // ← 追加
import TodoPage     from "./pages/TodoPage";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  const token = localStorage.getItem("token");
  return (
    <BrowserRouter>
      <Routes>
      <Route path="/register" element={<RegisterPage />} />
        <Route path="/login"    element={<LoginPage />} />
        <Route
          path="/"
          element={token ? <TodoPage /> : <Navigate to="/login" replace />}
        />
      </Routes>
      <ToastContainer position="top-right" autoClose={3000} />
    </BrowserRouter>
  );
}

export default App;
