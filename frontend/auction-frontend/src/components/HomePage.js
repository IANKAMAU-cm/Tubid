import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.logo}>Tubid</h1>
        <nav>
          <Link to="/login" style={styles.navLink}>
            Login
          </Link>
          <Link to="/register" style={styles.navLink}>
            Register
          </Link>
        </nav>
      </header>

      <main style={styles.main}>
        <h2 style={styles.heading}>Welcome to Tubid</h2>
        <p style={styles.subheading}>
          Discover, Sell, or Manage Auctions seamlessly.
        </p>
        <Link to="/login" style={styles.ctaButton}>
          Get Started
        </Link>
      </main>

      <footer style={styles.footer}>
        <p>© 2024 Tusome | Designed with ❤️</p>
      </footer>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: "'Arial', sans-serif",
    textAlign: "center",
    color: "#333",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    padding: "1rem 2rem",
    backgroundColor: "#f8f9fa",
    borderBottom: "1px solid #ddd",
  },
  logo: {
    margin: 0,
    fontSize: "1.5rem",
    fontWeight: "bold",
  },
  navLink: {
    margin: "0 10px",
    textDecoration: "none",
    color: "#007bff",
  },
  main: {
    padding: "2rem",
    backgroundColor: "#e9ecef",
    minHeight: "calc(100vh - 160px)", // Header + Footer height
  },
  heading: {
    fontSize: "2rem",
    marginBottom: "1rem",
  },
  subheading: {
    fontSize: "1.2rem",
    marginBottom: "2rem",
  },
  ctaButton: {
    display: "inline-block",
    padding: "0.5rem 1.5rem",
    fontSize: "1rem",
    color: "#fff",
    backgroundColor: "#007bff",
    borderRadius: "5px",
    textDecoration: "none",
    boxShadow: "0 2px 5px rgba(0,0,0,0.2)",
  },
  footer: {
    padding: "1rem",
    backgroundColor: "#f8f9fa",
    borderTop: "1px solid #ddd",
    marginTop: "2rem",
  },
};

export default HomePage;