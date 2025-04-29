// src/components/AuthCard.jsx
import React from "react";

export default function AuthCard({ title, children }) {
  return (
    <div className="max-w-sm mx-auto mt-16 bg-white rounded-2xl shadow-lg overflow-hidden">
      <div className="bg-primary-600 px-6 py-4 text-center">
        <h1 className="text-white text-2xl font-bold">MyTodo Pro</h1>
      </div>
      <div className="px-8 py-10">
        <h2 className="text-xl font-semibold mb-6 text-gray-800">{title}</h2>
        {children}
      </div>
    </div>
  );
}
