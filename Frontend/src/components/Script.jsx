/* eslint-disable react/prop-types */
import { useState } from 'react'; 
import "../styles/Script.css";
import ViewScript from './ViewScript';

function Script({ script }) {
    const [showModal, setShowModal] = useState(false);
    const [scriptContent, setScriptContent] = useState('');

    const handleViewClick = () => {
        // Set scriptContent and show the modal
        setScriptContent(script.content);
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    if (!script || !script.content) {
        return <p>No content available</p>;
    }

    return (
        <>
            <div className="script-container">
                <h3>Script ID: {script.id}</h3>
                <p>Created At: {new Date(script.created_at).toLocaleString()}</p>
                <button className="view-button" onClick={handleViewClick}><img src="src/assets/view.svg" alt="download" style={{ width: '20px'}} /></button>
            </div>
            <ViewScript
                show={showModal}
                onClose={handleCloseModal}
                scriptContent={scriptContent}
            />
        </>
    );
}

export default Script;
