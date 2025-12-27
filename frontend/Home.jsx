import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-wrapper">

      {/* Top Header */}
      <header className="top-header">
        <h1 className="logo">GearGuard</h1>

        <div className="header-buttons">
          <button
            className="login-btn"
            onClick={() => navigate('/login')}
          >
            Login
          </button>

          <button
            className="signup-btn"
            onClick={() => navigate('/signup')}
          >
            Sign Up
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <h2>Smart Maintenance Management Made Simple</h2>
        <p>
          Track equipment, manage maintenance, and keep your operations running smoothly.
        </p>
      </main>

    </div>
  );
};

export default Home;
