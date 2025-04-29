// src/components/TextInput.jsx
import React, { useState } from "react";
import { User, Lock, Eye, EyeOff } from "lucide-react";

export function TextInput({ type = "text", icon: Icon, ...props }) {
  const [show, setShow] = useState(false);
  const isPassword = type === "password";
  const actualType = isPassword && show ? "text" : type;

  return (
    <div className="relative mb-4">
      <Icon className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
      <input
        type={actualType}
        className="w-full pl-10 pr-10 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
        {...props}
      />
      {isPassword && (
        <button
          type="button"
          onClick={() => setShow((v) => !v)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
        >
          {show ? <EyeOff size={18}/> : <Eye size={18}/>}
        </button>
      )}
    </div>
  );
}
