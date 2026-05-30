import { useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/layout/Layout";
import GeneratorPage from "@/pages/GeneratorPage";
import LibraryPage from "@/pages/LibraryPage";

function App() {
  useEffect(() => {
    // Default to dark theme per design guidelines
    if (!document.documentElement.classList.contains("dark") && !document.documentElement.classList.contains("light")) {
      document.documentElement.classList.add("dark");
    }
  }, []);

  return (
    <div className="App suno-grain">
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<GeneratorPage />} />
            <Route path="/library" element={<LibraryPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
      <Toaster position="top-right" richColors closeButton />
    </div>
  );
}

export default App;
