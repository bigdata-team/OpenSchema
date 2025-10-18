import { Component, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router';

import Layout from "../page/layout/layout";
import Home from "../page/home";
import About from "../page/about/about";
import Setting from "../page/setting/setting";

export default class Router extends Component {
  render() {
    return (
      <BrowserRouter>
        <Suspense fallback={<div></div>}>
          <Routes>
            <Route path="/" element={<Layout />} >
                <Route index element={<Home />} />
            </Route>
            <Route path="about" element={<Layout />} >
              <Route index element={<About />} />
              <Route path="setting" element={<Setting />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    );
  }
}