import React, { useState, useEffect } from 'react';
import api from '../api';

const Auctions = () => {
    const [auctions, setAuctions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAuctions = async () => {
            try {
                console.log("Fetching auctions...");
                const response = await api.get('/api/auctions');
                console.log("Raw API response:", response);
                
                if (response.data && response.data.auctions) {
                    console.log("Auctions data:", response.data.auctions);
                    setAuctions(response.data.auctions);
                } else {
                    console.log("No auctions found in response:", response.data);
                }
                setError(null);
            } catch (err) {
                console.error("Error fetching auctions:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAuctions();
    }, []);

    if (loading) return <div>Loading auctions...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Available Auctions</h1>
            {auctions.length > 0 ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem', padding: '1rem' }}>
                    {auctions.map(auction => (
                        <div key={auction.id} style={{
                            border: '1px solid #ddd',
                            padding: '1rem',
                            borderRadius: '8px',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                        }}>
                            <h3>{auction.item_name}</h3>
                            <p>{auction.description}</p>
                            <p>Current Price: ${auction.current_price}</p>
                            <p>End Time: {new Date(auction.end_time).toLocaleString()}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No auctions available at this time.</p>
            )}
        </div>
    );
};

export default Auctions;
