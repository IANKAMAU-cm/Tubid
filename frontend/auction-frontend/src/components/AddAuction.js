import React, { useState } from "react";
import api from '../api';

const AddAuction = () => {
  const [formData, setFormData] = useState({
    item_name: "",
    description: "",
    start_price: "",
    end_time: "",
    image: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
        const response = await api.post("/api/add-auctions", {
            item_name: formData.item_name,
            description: formData.description,
            start_price: parseFloat(formData.start_price),
            end_time: formData.end_time,
        });
        
        if (response.status === 200) {
            alert("Auction added successfully!");
            window.location.href = '/seller_dashboard';
        }
    } catch (error) {
        console.log("Full error object:", error);
        console.log("Response data:", error.response?.data);
        console.log("Status code:", error.response?.status);
        alert(`Failed to add auction: ${error.response?.data?.error || error.message}`);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Add New Auction</h1>
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
          <input type="file" onChange={handleFileChange} required />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default AddAuction;