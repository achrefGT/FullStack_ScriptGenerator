// eslint-disable-next-line no-unused-vars
import React from 'react';
import api from "../api";

// eslint-disable-next-line react/prop-types
const GeneratedScript = ({ show, onClose, scriptContent, edit, setEdit, editedScriptContent, setEditedScriptContent, handleSaveEdit }) => {
    const handleDownload = async () => {
        try {
            // Create a FormData object to send the script content
            const formData = new FormData();
            formData.append('script_content', scriptContent);

            // Send a POST request to the Django API
            const response = await api.post('/download-script-api/', formData, {
                responseType: 'blob', // Important for handling file downloads
            });

            // Create a URL for the file download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'script.txt'); // Set the filename for the download
            document.body.appendChild(link);
            link.click();
            link.remove();

        } catch (error) {
            console.error('Error downloading the script:', error);
        }
    };

    return (
        <>
            <div 
                className={`modal fade ${show ? 'show d-block' : ''}`} 
                tabIndex="-1" 
                role="dialog" 
                style={{ display: show ? 'block' : 'none', zIndex: 1050, marginTop: '70px' }}
            >
            <div className="modal-dialog modal-dialog-scrollable" role="document" style={{ maxWidth: '75%' }}> 
                    <div className="modal-content" style={{ zIndex: 1060 }}>
                        <div className="modal-header">
                            <h4 className="modal-title">Generated Script</h4>
                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                                aria-label="Close"
                            ></button>
                        </div>
                        <div className="modal-body" style={{ maxHeight: '490', overflowY: 'auto' }}>
                            {!edit ? (
                                <textarea className="form-control" rows="17" readOnly value={scriptContent} />
                            ) : (
                                <textarea 
                                    className="form-control" 
                                    rows="18" 
                                    value={editedScriptContent} 
                                    onChange={(e) => setEditedScriptContent(e.target.value)} 
                                />
                            )}
                        </div>
                        <div className="modal-footer">
                            {!edit ? (
                                <>
                                    <div className="btn-group">
                                        <button type="button" className="btn btn-custom-outline" onClick={handleDownload}>Download Script</button>
                                        <button type="button" className="btn btn-secondary" onClick={() => setEdit(true)}>Edit Script</button>
                                    </div>
                                    
                                </>
                            ) : (
                                <>
                                    <button type="button" className="btn btn-custom-outline" onClick={handleSaveEdit}>Save Edits</button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
                <div className={`modal-backdrop fade ${show ? 'show' : ''}`} style={{ display: show ? 'block' : 'none', zIndex: 1040 }}></div>
            </div>
        </>
    );
};

export default GeneratedScript;
