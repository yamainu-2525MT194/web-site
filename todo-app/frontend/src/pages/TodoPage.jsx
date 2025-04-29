import React, { useEffect, useState } from "react";

export default function TodoPage() {
  const [tasks, setTasks] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    fetch("http://localhost:5001/api/tasks", {
      method:"GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch tasks");
        return res.json();
      })
      .then(setTasks)
      .catch((err) => console.error(err));
  }, []);

  const addTask = () => {
    if (!input.trim()) return;
    fetch("http://localhost:5001/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ title: input.trim() }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to add task");
        return res.json();
      })
      .then((newTask) => {
        setTasks((prev) => [...prev, newTask]);
        setInput("");
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="max-w-2xl mx-auto my-12 space-y-6">
      <h1 className="text-3xl font-bold">My Todo List</h1>
      <div className="flex gap-3">
        <input
          type="text"
          className="flex-1 px-3 py-2 border rounded"
          placeholder="New task"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          className="bg-primary-500 text-white px-4 py-2 rounded"
          onClick={addTask}
        >
          Add
        </button>
      </div>
      <ul className="space-y-2">
        {tasks.map((t) => (
          <li key={t.id} className="p-4 bg-white shadow rounded flex justify-between">
            <span>{t.title}</span>
            <span>{t.done ? "✅" : "⏳"}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
