import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

const EditAuction = () => {
  const { id } = useParams(); // Get auction ID from URL
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    item_name: "",
    description: "",
    start_price: "",
    current_price: "",
    end_time: "",
    image: null,
  });

  useEffect(() => {
    // Fetch auction details to prefill the form
    const fetchAuction = async () => {
      try {
        const response = await axios.get(`/api/auctions/${id}`);
        const auction = response.data;
        setFormData({
          item_name: auction.item_name,
          description: auction.description,
          start_price: auction.start_price,
          current_price: auction.current_price,
          end_time: new Date(auction.end_time).toISOString().slice(0, 16), // Format for input[type="datetime-local"]
        });
      } catch (error) {
        console.error(error);
        alert("Failed to fetch auction details.");
      }
    };

    fetchAuction();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    for (const key in formData) {
      data.append(key, formData[key]);
    }

    try {
      await axios.put(`/api/auctions/${id}`, data);
      alert("Auction updated successfully!");
      navigate("/seller_dashboard");
    } catch (error) {
      console.error(error);
      alert("Failed to update auction.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Edit Auction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Item Name:</label>
          <input
            type="text"
            name="item_name"
            value={formData.item_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Start Price:</label>
          <input
            type="number"
            name="start_price"
            value={formData.start_price}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Current Price:</label>
          <input
            type="number"
            name="current_price"
            value={formData.current_price}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>End Time:</label>
          <input
            type="datetime-local"
            name="end_time"
            value={formData.end_time}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Image:</label>
          <input type="file" onChange={handleFileChange} />
        </div>
        <button type="submit">Update Auction</button>
      </form>
    </div>
  );
};

export default EditAuction;