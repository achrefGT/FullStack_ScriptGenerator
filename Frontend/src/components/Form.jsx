/* eslint-disable react/no-unescaped-entities */
import { useState, useEffect } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";
import huaweiImage from "../assets/Huawei.svg";

// eslint-disable-next-line react/prop-types
function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    useEffect(() => {
        document.title = name; // Change the title
    }, [name]);

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, { username, password });
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            alert(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-image-container">
            <div className="form-content">
                <div className="form-container">
                    <form onSubmit={handleSubmit} className="inner-container">
                        <h1>{name}</h1>
                        <div className="form-group">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input
                                id="username"
                                className="form-input"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter your username"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input
                                id="password"
                                className="form-input"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter your password"
                            />
                        </div>
                        {loading && (
                            <div className="loading-container">
                                <LoadingIndicator />
                            </div>
                        )}
                        <button className="form-button" type="submit">
                            {name}
                        </button>
                        {method === "register" ? (
                            <p className="form-footer-text">
                                Already have an account? <a href="/login" className="form-link">Login</a>
                            </p>
                        ) : (
                            <p className="form-footer-text">
                                Don't have an account? <a href="/register" className="form-link">Register</a>
                            </p>
                        )}
                    </form>
                </div>
                <div className="image-container">
                    <img src={huaweiImage} alt="Huawei Logo" className="image" />
                </div>
            </div>
        </div>
    );
}

export default Form;
