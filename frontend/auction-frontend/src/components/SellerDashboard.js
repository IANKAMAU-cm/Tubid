import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import LogoutButton from "./LogoutButton";

const SellerDashboard = () => {
  const [auctions, setAuctions] = useState([]);

  useEffect(() => {
    const fetchAuctions = async () => {
      try {
        const response = await axios.get("/api/auctions");
        setAuctions(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchAuctions();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px'
      }}>
        <h1>Seller Dashboard</h1>
        <LogoutButton />
      </div>
      <div style={{ margin: "20px 0" }}>
        <Link to="/seller_dashboard/add-auction">
          <button>Add New Auction</button>
        </Link>
      </div>
      <div>
        <h2>Your Auctions</h2>
        <ul>
          {auctions.map((auction) => (
            <li key={auction.id}>
              {auction.item_name} - 
              <Link to={`/seller_dashboard/edit-auction/${auction.id}`}>Edit</Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SellerDashboard;