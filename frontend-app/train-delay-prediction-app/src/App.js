import React, { Fragment }  from 'react';

import { Routes, Route, Link } from "react-router-dom";

import Layout from './components/Layout/Layout';
import About from './components/about/About';

import './App.css';

function App() {
  return (
    <Fragment>
      <Layout>
        <Routes>
          <Route path="about" element={<About />} />
        </Routes>
      </Layout>
    </Fragment>
  );
}

export default App;
