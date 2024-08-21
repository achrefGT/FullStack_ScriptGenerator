/* eslint-disable no-unused-vars */
import { useState } from 'react';
import api from "../api";
import GeneratedScript from './GeneratedScript';

function UploadLLD() {
    const [file, setFile] = useState(null);
    const [scriptContent, setScriptContent] = useState('');
    const [error, setError] = useState('');
    const [showModal, setShowModal] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event, endpoint) => {
        event.preventDefault();

        if (!file) {
            setError('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post(endpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setScriptContent(response.data.script_content);
            setError('');  
            setShowModal(true);  

        } catch (err) {
            setError('An error occurred while uploading the file.');
        }
    };

    const handleCloseModal = () => setShowModal(false);

    return (
        <div className="container mt-5 d-flex justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
            <div className="card p-4 shadow" style={{ width: '90%', maxWidth: '650px', border: '2px solid #D80030' }}>
                <div className="card-body text-center">
                    <h2 className="mb-4">UPLOAD YOUR LLD</h2>

                    {error && <div className="alert alert-danger" role="alert">{error}</div>}

                    <form encType="multipart/form-data">
                        <input type="file" name="file" onChange={handleFileChange} className="custom-file-input form-control mb-3" />

                        <div className="btn-group d-flex" style={{ width: '100%' }}>
                            <button type="button" onClick={(e) => handleSubmit(e, '/upload-lld-api/')} className="btn btn-custom-outline">Trans-Dediers</button>
                            <button type="button" onClick={(e) => handleSubmit(e, '/upload-lld-Co-Trans-api/')} className="btn btn-custom-outline">Co-Trans</button>
                        </div>
                    </form>
                </div>
            </div>

            {/* Generated Script Modal */}
            <GeneratedScript
                show={showModal}
                onClose={handleCloseModal}
                scriptContent={scriptContent}
            />
        </div>
    );
}

export default UploadLLD;