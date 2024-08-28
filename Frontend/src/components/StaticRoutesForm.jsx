/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
// StaticRoutesForm.js

import React, { useState } from 'react';
import api from "../api";
import GeneratedScript from './GeneratedScript';

function StaticRoutesForm({ show, onClose, routers }) {
    if (!show) return null;

    const [showModal, setShowModal] = useState(false);
    const [scriptContent, setScriptContent] = useState('');
    const [edit, setEdit] = useState(false); 
    const [editedScriptContent, setEditedScriptContent] = useState('');
    const [scriptId, setScriptId] = useState(null); 
    const [error, setError] = useState('');

    // Initialize state with router IDs
    const [nextHopAddresses, setNextHopAddresses] = useState(
        routers.reduce((acc, router) => ({
            ...acc,
            [router.id]: {  // Use router ID as the key
                name: router.name,
                o_and_m_next: '',
                tdd_next: ''
            }
        }), {})
    );

    // Handle input changes
    const handleChange = (routerId, field, value) => {
        setNextHopAddresses(prev => ({
            ...prev,
            [routerId]: {
                ...prev[routerId],
                [field]: value
            }
        }));
    };

    // Handle form submission
    const handleSubmit = async () => {
        try {
            const response = await api.put('/update-static-routes/', {
                routes: Object.entries(nextHopAddresses).map(([routerId, { o_and_m_next, tdd_next }]) => ({
                    router_id: routerId,
                    o_and_m_next,
                    tdd_next
                }))
            });
            if (response.status === 200) {    
                setScriptContent(response.data.script_content);
                setEditedScriptContent(response.data.script_content); 
                setScriptId(response.data.id); 
                setError('');
                setShowModal(true);
            } else {
                console.error('Failed to update routes:', response.statusText);
            }
        } catch (error) {
            console.error('Error updating routes:', error);
        }
    };

    // Handle modal close
    const handleCloseModal = () => {
        setShowModal(false);
        onClose();  // Call the onClose prop to close the main form modal
    };

    const handleEditClick = () => {
        setEdit(true);
    };

    const handleSaveEdit = async () => {
        if (!scriptId) {
            console.error('Script ID is missing.');
            return;
        }

        try {
            const response = await api.put(`/edit-script/${scriptId}/`, {
                content: editedScriptContent, 
            });

            if (response.status === 204) {
                console.log('Script saved successfully.');
                setScriptContent(editedScriptContent);
                setEdit(false);
                setShowModal(true);
            } else {
                console.error('Failed to save the script:', response.statusText);
            }

        } catch (error) {
            console.error('Error saving the script:', error);
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
            <div className="modal-dialog" style={{ maxWidth: '60%' }}>
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Static Routes</h5>
                        <button type="button" className="btn-close" aria-label="Close" onClick={onClose}></button>
                    </div>
                    <div className="modal-body">
                        {routers.map(router => (
                            <div key={router.id} className="mb-4"> {/* Use router ID as key */}
                                <h5>{router.name}</h5>
                                <div className="d-flex mb-3 align-items-center">
                                    <label htmlFor={`o_and_m_next_${router.id}`} className="me-2" style={{ width: '150px' }}>
                                        O&M static route
                                    </label>
                                    <input
                                        type="text"
                                        id={`o_and_m_next_${router.id}`}
                                        placeholder="next hop address"
                                        value={nextHopAddresses[router.id]?.o_and_m_next || ''}
                                        onChange={(e) => handleChange(router.id, 'o_and_m_next', e.target.value)}
                                        className="form-control"
                                        style={{ flex: 1 }}
                                    />
                                </div>
                                <div className="d-flex mb-3 align-items-center">
                                    <label htmlFor={`tdd_next_${router.id}`} className="me-2" style={{ width: '150px' }}>
                                        TDD static route
                                    </label>
                                    <input
                                        type="text"
                                        id={`tdd_next_${router.id}`}
                                        placeholder="next hop address"
                                        value={nextHopAddresses[router.id]?.tdd_next || ''}
                                        onChange={(e) => handleChange(router.id, 'tdd_next', e.target.value)}
                                        className="form-control"
                                        style={{ flex: 1 }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-custom-outline" onClick={handleSubmit}>Upload</button>
                    </div>
                </div>
            </div>
        </div>
        <div className={`modal-backdrop fade ${show ? 'show' : ''}`} style={{ display: show ? 'block' : 'none', zIndex: 1040 }}></div>

        <GeneratedScript
            show={showModal}
            onClose={handleCloseModal}
            scriptContent={scriptContent}
            edit={edit}
            setEdit={setEdit}
            editedScriptContent={editedScriptContent}
            setEditedScriptContent={setEditedScriptContent}
            handleSaveEdit={handleSaveEdit}
        />
    </>
    );
}

export default StaticRoutesForm;
