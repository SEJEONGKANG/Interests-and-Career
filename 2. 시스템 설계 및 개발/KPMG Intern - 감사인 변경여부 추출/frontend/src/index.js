import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";
import App from "./App"; // Your main application component
import reportWebVitals from "./reportWebVitals";

const rootElement = document.getElementById("root");

ReactDOM.render(
    <React.StrictMode>
        <Router>
            <App />
        </Router>
    </React.StrictMode>,
    rootElement
);

reportWebVitals();
