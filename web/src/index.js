import React from 'react';
import ReactDOM from 'react-dom';
import './content/styles/index.scss';
import App from './App';
import customHistory from './customHistory'
import reportWebVitals from './reportWebVitals';
import { Router } from "react-router";

ReactDOM.render(
  <Router history={customHistory}>
    <App />
  </Router>,
  document.getElementById('root')
);

reportWebVitals();
