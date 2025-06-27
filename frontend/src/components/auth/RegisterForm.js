import React, { useState } from 'react';
import Button from '../common/Button';

const RegisterForm = ({ onRegisterSuccess }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      console.log('Attempting registration with:', email, username, password);
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password, full_name: username }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }
      // Auto-login after registration is a common pattern
      const loginResponse = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password: password }).toString(),
      });
      if (!loginResponse.ok) {
          const errorData = await loginResponse.json();
          throw new Error(errorData.detail || 'Auto-login failed after registration');
      }
      const loginData = await loginResponse.json();
      localStorage.setItem('token', loginData.access_token);

      onRegisterSuccess();
    } catch (err) {
      setError(err.message || 'Registration failed.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <div>
        <label htmlFor="reg-username" className="block text-sm font-medium text-gray-700">Username</label>
        <input
          type="text"
          id="reg-username"
          name="username"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="reg-email" className="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          id="reg-email"
          name="email"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="reg-password" className="block text-sm font-medium text-gray-700">Password</label>
        <input
          type="password"
          id="reg-password"
          name="password"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <Button type="submit" className="w-full">Register</Button>
    </form>
  );
};

export default RegisterForm;