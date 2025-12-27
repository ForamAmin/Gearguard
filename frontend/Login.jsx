import React from 'react';
import './Login.css';

const Login = () => {
  return (
    <div className="login-wrapper">

      {/* Header */}
      <header className="top-header">
        <h1 className="logo">GearGuard</h1>
      </header>

      {/* Login Card */}
      <div className="login-container">
        <h2>Login</h2>

        <form className="login-form">
          <input
            type="email"
            placeholder="Email"
            required
          />

          <input
            type="password"
            placeholder="Password"
            required
          />

          <button type="submit">Login</button>
        </form>

        <p className="signup-text">
          Don’t have an account? <span>Sign Up</span>
        </p>
      </div>

    </div>
  );
};

export default Login;
