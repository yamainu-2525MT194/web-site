import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import { TextInput } from "../components/TextInput";
import LoadingButton from "../components/LoadingButton";
import { toast } from "react-toastify";
import { User, Lock } from "lucide-react";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    setLoading(true);
    if (!username.trim() || !password) {
      toast.error("Username and password are required");
      setLoading(false);
      return;
    }
    try {
      const res = await fetch("http://localhost:5001/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.trim(), password }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.msg || "Registration failed");
        setLoading(false);
        return;
      }
      toast.success("Registration successful! Please log in.");
      navigate("/login", { replace: true });
    } catch (err) {
      toast.error(err.message);
      setLoading(false);
    }
  };

  return (
    <AuthCard title="Register">
      <TextInput
        icon={User}
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextInput
        icon={Lock}
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <LoadingButton isLoading={loading} onClick={handleRegister}>
        Register
      </LoadingButton>
      <p className="text-center text-sm mt-4">
        Already have an account?{" "}
        <Link to="/login" className="text-primary-700 hover:underline">
          Log in
        </Link>
      </p>
    </AuthCard>
  );
}
