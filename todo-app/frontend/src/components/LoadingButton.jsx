// src/components/LoadingButton.jsx
import React from "react";
import { motion } from "framer-motion";

export default function LoadingButton({ isLoading, children, ...props }) {
  return (
    <button
      disabled={isLoading}
      className={`w-full flex justify-center items-center py-2 rounded-lg text-white 
        ${isLoading ? "bg-primary-300 cursor-not-allowed" : "bg-primary-600 hover:bg-primary-700"}`}
      {...props}
    >
      {isLoading && (
        <motion.span
          className="loader ease-linear rounded-full border-2 border-t-2 border-white w-5 h-5 mr-3"
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 1 }}
        />
      )}
      {children}
    </button>
  );
}
