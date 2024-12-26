import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Register from './components/Register';
import Login from "./components/Login";
import Auctions from "./components/Auctions";
import AdminDashboard from "./components/AdminDashboard";
import SellerDashboard from "./components/SellerDashboard";
import AddAuction from "./components/AddAuction";
import EditAuction from "./components/EditAuction";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/auctions" element={<Auctions />} />
        <Route path="/admin_dashboard" element={<AdminDashboard />} />
        <Route path="/seller_dashboard" element={<SellerDashboard />} />
        <Route path="/seller_dashboard/add-auction" element={<AddAuction />} />
        <Route path="/seller_dashboard/edit-auction/:id" element={<EditAuction />} />
      </Routes>
    </Router>
  );
};

export default App;
