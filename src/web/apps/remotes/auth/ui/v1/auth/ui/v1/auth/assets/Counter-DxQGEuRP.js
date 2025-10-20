import{u as i}from"./counter-C-CjsEyt.js";var l={exports:{}},s={};/**
 * @license React
 * react-jsx-runtime.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var x=Symbol.for("react.transitional.element"),c=Symbol.for("react.fragment");function a(n,t,e){var r=null;if(e!==void 0&&(r=""+e),t.key!==void 0&&(r=""+t.key),"key"in t){e={};for(var o in t)o!=="key"&&(e[o]=t[o])}else e=t;return t=e.ref,{$$typeof:x,type:n,key:r,ref:t!==void 0?t:null,props:e}}s.Fragment=c;s.jsx=a;s.jsxs=a;l.exports=s;var u=l.exports;function d({useCounterHook:n=i}={}){const t=n(r=>r.count),e=n(r=>r.increment);return u.jsx("div",{className:"m-2",children:u.jsxs("button",{className:"p-2 bg-blue-500 text-white",onClick:e,children:["Remote count is ",t]})})}const j=Object.freeze(Object.defineProperty({__proto__:null,default:d},Symbol.toStringTag,{value:"Module"}));export{d as C,j as a,u as j};
