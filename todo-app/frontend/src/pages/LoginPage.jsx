import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import { TextInput } from "../components/TextInput";
import LoadingButton from "../components/LoadingButton";
import { toast } from "react-toastify";
import { User, Lock } from "lucide-react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5001/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.msg || "Login failed");
        setLoading(false);
        return;
      }
      toast.success("Logged in!");
      localStorage.setItem("token", data.access_token);
      navigate("/", { replace: true });
    } catch (err) {
      toast.error(err.message);
      setLoading(false);
    }
  };

  return (
    <AuthCard title="Login">
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
      <LoadingButton isLoading={loading} onClick={handleLogin}>
        Login
      </LoadingButton>
      <p className="text-center text-sm mt-4">
        Don’t have an account?{" "}
        <Link to="/register" className="text-primary-700 hover:underline">
          Register
        </Link>
      </p>
    </AuthCard>
  );
}
