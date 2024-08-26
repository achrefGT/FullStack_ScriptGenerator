import "../styles/Navbar.css";

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <img src="src/assets/Huawei.svg" alt="Huawei Logo" style={{ width: '70px' }} />
                <a className="navbar-brand" href="/">ScriptGenerator</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav me-auto">
                        <li className="nav-item">
                            <a className="nav-link" href="/MyScripts">My scripts</a>
                        </li>
                    </ul>
                    <ul className="navbar-nav">
                        <li className="nav-item d-flex align-items-center">
                            
                            <a className="nav-link" href="/logout"><img src="src/assets/logout.svg" alt="logout" style={{ width: '18px', marginBottom: '2px', marginRight: '5px' }} />Logout</a>
                        </li>

                        <li className="nav-item separator">
                            <span>|</span>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="http://127.0.0.1:8000/admin/">Admin</a>
                        </li>
                    </ul>



                    
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
