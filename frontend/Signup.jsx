import React, { useState } from 'react';
import './Signup.css';

const Signup = () => {
  const [role, setRole] = useState('manager');

  return (
    <div className="signup-wrapper">

      {/* Header */}
      <header className="top-header">
        <h1 className="logo">GearGuard</h1>
      </header>

      {/* Signup Card */}
      <div className="signup-container">
        <h2>Create Account</h2>

        {/* Role Selection */}
        <div className="role-select">
          <button
            className={role === 'manager' ? 'active' : ''}
            onClick={() => setRole('manager')}
          >
            Manager
          </button>
          <button
            className={role === 'employee' ? 'active' : ''}
            onClick={() => setRole('employee')}
          >
            Employee
          </button>
          <button
            className={role === 'technician' ? 'active' : ''}
            onClick={() => setRole('technician')}
          >
            Technician
          </button>
        </div>

        {/* Form */}
        <form className="signup-form">
          <input type="text" placeholder="Full Name" required />
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />

          <button type="submit">
            Sign Up as {role.charAt(0).toUpperCase() + role.slice(1)}
          </button>
        </form>
      </div>

    </div>
  );
};

export default Signup;
