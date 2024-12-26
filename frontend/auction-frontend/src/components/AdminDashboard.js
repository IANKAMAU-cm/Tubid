import React from 'react';
import LogoutButton from './LogoutButton';

const AdminDashboard = () => {
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px'
      }}>
        <h1>Admin Dashboard</h1>
        <LogoutButton />
      </div>
      {/* Add your admin dashboard content here */}
    </div>
  );
};

export default AdminDashboard;
