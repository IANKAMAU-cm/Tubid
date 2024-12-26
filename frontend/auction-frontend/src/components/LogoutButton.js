import React from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await api.post('/api/logout');
      if (response.status === 200) {
        navigate('/');
      }
    } catch (error) {
      console.error('Logout error:', error);
      alert('Failed to logout. Please try again.');
    }
  };

  return (
    <button 
      onClick={handleLogout}
      style={{
        padding: '8px 16px',
        backgroundColor: '#dc3545',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer'
      }}
    >
      Logout
    </button>
  );
};

export default LogoutButton; 