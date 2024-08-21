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
                            <a className="nav-link" href="#">My scripts</a>
                        </li>
                    </ul>
                    <a className="btn btn-custom-outline" href="/logout" role="button">logout</a>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
