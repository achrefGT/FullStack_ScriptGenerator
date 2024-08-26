/* eslint-disable react/no-unescaped-entities */
/* eslint-disable no-unused-vars */
import { useState, useEffect } from "react";
import api from "../api";
import Script from "../components/Script";
import Navbar from "../components/Navbar";
import '../styles/Script.css';

function getFirstDayOfWeek(d) {
    const date = new Date(d);
    const day = date.getDay(); // Get day of week
    const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Adjust to Monday
    return new Date(date.setDate(diff));
}

const isThisWeek = (date) => {
    const today = new Date();
    const firstDayOfWeek = getFirstDayOfWeek(today);
    const lastDayOfWeek = new Date(firstDayOfWeek);
    lastDayOfWeek.setDate(firstDayOfWeek.getDate() + 6);

    // Reset time for accurate comparison
    date.setHours(0, 0, 0, 0);
    firstDayOfWeek.setHours(0, 0, 0, 0);
    lastDayOfWeek.setHours(23, 59, 59, 999);
    
    return date >= firstDayOfWeek && date <= lastDayOfWeek;
};

const isToday = (date) => {
    const today = new Date();
    return (
        date.getFullYear() === today.getFullYear() &&
        date.getMonth() === today.getMonth() &&
        date.getDate() === today.getDate()
    );
};

const isThisMonth = (date) => {
    const today = new Date();
    return (
        date.getFullYear() === today.getFullYear() &&
        date.getMonth() === today.getMonth()
    );
};

const isOlderThanThisMonth = (date) => {
    const today = new Date();
    return (
        date.getFullYear() < today.getFullYear() ||
        (date.getFullYear() === today.getFullYear() && date.getMonth() < today.getMonth())
    );
};

function MyScripts() {
    const [scripts, setScripts] = useState([]);
    const [showToday, setShowToday] = useState(true);
    const [showThisWeek, setShowThisWeek] = useState(true);
    const [showThisMonth, setShowThisMonth] = useState(true);
    const [showOlder, setShowOlder] = useState(true);

    useEffect(() => {
        getScripts();
    }, []);

    const getScripts = () => {
        api
            .get('/MyScripts/')
            .then((res) => res.data)
            .then((data) => {
                setScripts(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const today = new Date();
    const todayScripts = scripts.filter(script => isToday(new Date(script.created_at)));
    const thisWeekScripts = scripts.filter(script => isThisWeek(new Date(script.created_at)) && !isToday(new Date(script.created_at)));
    const thisMonthScripts = scripts.filter(script => isThisMonth(new Date(script.created_at)) && !isThisWeek(new Date(script.created_at)));
    const oldScripts = scripts.filter(script => isOlderThanThisMonth(new Date(script.created_at)));

    const toggleToday = () => setShowToday(!showToday);
    const toggleThisWeek = () => setShowThisWeek(!showThisWeek);
    const toggleThisMonth = () => setShowThisMonth(!showThisMonth);
    const toggleOlder = () => setShowOlder(!showOlder);

    return (
        <>
            <Navbar />
            <div className="page-container">
                <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
                    <div className="card p-4 shadow" style={{ width: '90%', maxWidth: '1000px', border: '2px solid #D80030' }}>
                        <div className="card-body text-center">
                            <h2 className="mb-4">My Scripts</h2>

                            {/* Today's Scripts */}
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h6 
                                    style={{ cursor: 'pointer' }} 
                                    onClick={toggleToday} 
                                >
                                    Today's Scripts
                                </h6>
                                <button 
                                    className="btn btn-link" 
                                    type="button" 
                                    data-toggle="collapse" 
                                    data-target="#todayCollapse" 
                                    aria-expanded={showToday} 
                                    aria-controls="todayCollapse"
                                    onClick={toggleToday}
                                >
                                    {showToday ? <img src="src/assets/arrow-up.svg" alt="arrow-up" style={{ width: '20px'}} /> : <img src="src/assets/arrow-down.svg" alt="arrow-down" style={{ width: '20px'}} />}
                                </button>
                            </div>
                            <div className={`collapse ${showToday ? 'show' : ''}`} id="todayCollapse">
                                {todayScripts.length > 0 ? (
                                    todayScripts.map((script) => (
                                        <Script script={script} key={script.id} />
                                    ))
                                ) : (
                                    <p>No scripts available</p>
                                )}
                            </div>

                            <hr />

                            <div>
                            {/* This Week's Scripts */}
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h6 
                                    style={{ cursor: 'pointer' }} 
                                    onClick={toggleThisWeek} 
                                >
                                    This Week's Scripts
                                </h6>
                                <button 
                                    className="btn btn-link" 
                                    type="button" 
                                    data-toggle="collapse" 
                                    data-target="#weekCollapse" 
                                    aria-expanded={showThisWeek} 
                                    aria-controls="weekCollapse"
                                    onClick={toggleThisWeek}
                                >
                                    {showThisWeek ? <img src="src/assets/arrow-up.svg" alt="arrow-up" style={{ width: '20px'}} /> : <img src="src/assets/arrow-down.svg" alt="arrow-down" style={{ width: '20px'}} />}
                                </button>
                            </div>
                            <div className={`collapse ${showThisWeek ? 'show' : ''}`} id="weekCollapse">
                                {thisWeekScripts.length > 0 ? (
                                    thisWeekScripts.map((script) => (
                                        <Script script={script} key={script.id} />
                                    ))
                                ) : (
                                    <p>No scripts available</p>
                                )}
                            </div>

                            <hr />

                            {/* This Month's Scripts */}
                            <div className="d-flex justify-content-between align-items-center mb-3">
                            <h6 
                                style={{ cursor: 'pointer' }} 
                                onClick={toggleThisMonth} 
                            >
                                This Month's Scripts
                            </h6>
                                <button 
                                    className="btn btn-link" 
                                    type="button" 
                                    data-toggle="collapse" 
                                    data-target="#monthCollapse" 
                                    aria-expanded={showThisMonth} 
                                    aria-controls="monthCollapse"
                                    onClick={toggleThisMonth}
                                >
                                    {showThisMonth ? <img src="src/assets/arrow-up.svg" alt="arrow-up" style={{ width: '20px'}} /> : <img src="src/assets/arrow-down.svg" alt="arrow-down" style={{ width: '20px'}} />}
                                </button>
                            </div>
                            <div className={`collapse ${showThisMonth ? 'show' : ''}`} id="monthCollapse">
                                {thisMonthScripts.length > 0 ? (
                                    thisMonthScripts.map((script) => (
                                        <Script script={script} key={script.id} />
                                    ))
                                ) : (
                                    <p>No scripts available</p>
                                )}
                            </div>

                            <hr />

                            {/* Older than This Month's Scripts */}
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h6 
                                    style={{ cursor: 'pointer' }} 
                                    onClick={toggleOlder} 
                                >
                                    Older than This Month's Scripts
                                </h6>
                                <button 
                                    className="btn btn-link" 
                                    type="button" 
                                    data-toggle="collapse" 
                                    data-target="#olderCollapse" 
                                    aria-expanded={showOlder} 
                                    aria-controls="olderCollapse"
                                    onClick={toggleOlder}
                                >
                                    {showOlder ? <img src="src/assets/arrow-up.svg" alt="arrow-up" style={{ width: '20px'}} /> : <img src="src/assets/arrow-down.svg" alt="arrow-down" style={{ width: '20px'}} />}
                                </button>
                            </div>
                            <div className={`collapse ${showOlder ? 'show' : ''}`} id="olderCollapse">
                                {oldScripts.length > 0 ? (
                                    oldScripts.map((script) => (
                                        <Script script={script} key={script.id} />
                                    ))
                                ) : (
                                    <p>No scripts available</p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>
    );
}

export default MyScripts;
