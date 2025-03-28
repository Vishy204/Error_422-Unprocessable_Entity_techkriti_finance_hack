import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import axios from "axios";
import "./App.css";
import "./chatBubble";
import ChatIcon from "./chatBubble";
import ReactMarkdown from "react-markdown";
import Loader from "./loader";

// Navbar Component
const Navbar = () => {
  return (
    <nav className="navbar animate-slide-down">
      <div className="navbar-container">
        <div className="navbar-brand">FinanceInsight</div>

        <Link to="/" className="nav-link">
          Home
        </Link>
        <Link to="/upload" className="nav-link">
          PDF Analyzer
        </Link>
      </div>
    </nav>
  );
};

// Home Page Component
const HomePage = () => {
  return (
    <div className="home-container animate-fade-in">
      <h1 className="home-title">Annual Reports , Simplified</h1>
      <p className="home-description">
        Upload an annual report of a company and get a clear, jargon-free
        explanation of what it means for the company's health and future. No
        financial expertise required.
      </p>
      <div className="home-cta">
        <Link to="/upload" className="cta-button pulse-animation">
          Analyze Your Finances
        </Link>
      </div>
    </div>
  );
};

const PDFAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSection, setCurrentSection] = useState("summary");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setAnalysis(response.data);
      setCurrentSection("summary");
    } catch (error) {
      console.error("Error uploading file", error);
      alert("Failed to analyze the PDF");
    }
    setIsLoading(false);
  };

  const renderSection = () => {
    if (!analysis) return null;

    const sectionConfig = {
      summary: {
        title: "Executive Summary",
        content: analysis.summary,
        className: "summary-section",
      },
      flags: {
        title: "Financial Risk Assessment",
        content: (
          <div className="flag-container">
            <div className="red-flags">
              <h3>Potential Risks</h3>
              <ReactMarkdown>{analysis.redFlags}</ReactMarkdown>
            </div>
            <div className="green-flags">
              <h3>Positive Indicators</h3>
              <ReactMarkdown>{analysis.greenFlags}</ReactMarkdown>
            </div>
          </div>
        ),
        className: "flags-section",
      },
      story: {
        title: "Financial Narrative",
        content: <ReactMarkdown>{analysis.story}</ReactMarkdown>,
        className: "story-section",
      },
      conclusion: {
        title: "Strategic Insights",
        content: (
          <>
            <p>{analysis.conclusion}</p>
            <br></br>
            <p>
              <strong>
                <em>
                  *Note: This data gathers information from Google News about
                  the company and compares it with our collected data. A high
                  score indicates that our data is reliable, while a low score
                  suggests that the company may be disseminating misleading
                  information, ultimately presenting a false narrative.
                </em>
              </strong>
            </p>
          </>
        ),
        className: "conclusion-section",
      },
      visualisations: {
        title: "Visualizations",
        content: (
          <img
            src="../public/download.png"
            style={{
              maxWidth: "100%",
              height: "auto",
              display: "block",
              margin: "0 auto",
            }}
            alt="Visualization"
          />
        ),

        className: "visualisations-section",
      },
    };

    const currentSectionData = sectionConfig[currentSection];

    return (
      <div className={`analysis-section ${currentSectionData.className}`}>
        <h3>{currentSectionData.title}</h3>
        {currentSectionData.content}
      </div>
    );
  };

  return (
    <div className="analyzer-container">
      {isLoading ? (
        <Loader />
      ) : (
        <div className="analyzer-card">
          {!analysis ? (
            <>
              <h2 className="analyzer-title">Upload Financial PDF</h2>
              <div className="file-input-container">
                <label htmlFor="file-upload" className="file-input-label">
                  {file ? file.name : "Select Financial Document"}
                  <input
                    type="file"
                    id="file-upload"
                    accept="application/pdf"
                    onChange={handleFileChange}
                    className="file-input"
                  />
                </label>
              </div>

              <button
                onClick={handleUpload}
                disabled={!file}
                className={`upload-button ${file ? "pulse-animation" : ""}`}
              >
                Analyze Document
              </button>
            </>
          ) : (
            <div className="full-analysis-container">
              <div className="section-navigation">
                {[
                  "summary",
                  "flags",
                  "story",
                  "conclusion",
                  "visualisations",
                ].map((section) => (
                  <button
                    key={section}
                    onClick={() => setCurrentSection(section)}
                    className={`nav-button ${
                      currentSection === section ? "active" : ""
                    }`}
                  >
                    {section.charAt(0).toUpperCase() + section.slice(1)}
                  </button>
                ))}
              </div>

              <div className="section-content">{renderSection()}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="route-container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<PDFAnalyzer />} />
          </Routes>
        </div>
        <ChatIcon />
      </div>
    </Router>
  );
}

export default App;
