import React from 'react';
import tellink from "../assets/tellink.png";

function Home() {
    return (
        <div className="home-container">
            <div className="content">
                <h1>Bem-vindo à Página Inicial</h1>
                <img src={tellink} alt="Logo" className="logo" />
            </div>
        </div>
    );
}

export default Home;
