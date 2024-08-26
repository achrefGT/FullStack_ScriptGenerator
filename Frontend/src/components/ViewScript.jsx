// eslint-disable-next-line no-unused-vars
import React from 'react';
import api from "../api";

// eslint-disable-next-line react/prop-types
const GeneratedScript = ({ show, onClose, scriptContent}) => {
    const handleDownload = async () => {
        try {
            
            const formData = new FormData();
            formData.append('script_content', scriptContent);

            
            const response = await api.post('/download-script-api/', formData, {
                responseType: 'blob', 
            });

           
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'script.txt'); 
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
                            <div className="outer">
                                <div className="inner" onClick={onClose}>
                                    <label className="inner-label">Back</label>
                                </div>
                            </div>
                            
                        </div>
                        <div className="modal-body" style={{ maxHeight: '490', overflowY: 'auto' }}>
                            <textarea className="form-control" rows="17" readOnly value={scriptContent} />
                        </div>
                        <div className="modal-footer">
                            <div className="btn-group">
                                <button type="button" className="btn btn-custom-outline" onClick={handleDownload}><img src="src/assets/download.svg" alt="download" style={{ width: '18px',marginBottom: '3px', marginRight: '5px' }} />Download</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={`modal-backdrop fade ${show ? 'show' : ''}`} style={{ display: show ? 'block' : 'none', zIndex: 1040 }}></div>
            </div>
        </>
    );
};

export default GeneratedScript;
