if(!self.define){let e,s={};const l=(l,i)=>(l=new URL(l+".js",i).href,s[l]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=l,e.onload=s,document.head.appendChild(e)}else e=l,importScripts(l),s()})).then((()=>{let e=s[l];if(!e)throw new Error(`Module ${l} didn’t register its module`);return e})));self.define=(i,n)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(s[r])return;let o={};const c=e=>l(e,r),u={module:{uri:r},exports:o,require:c};s[r]=Promise.all(i.map((e=>u[e]||c(e)))).then((e=>(n(...e),o)))}}define(["./workbox-5b385ed2"],(function(e){"use strict";e.setCacheNameDetails({prefix:"PPH"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.d8f99b3c.css",revision:null},{url:"/css/chunk-vendors.d81ba0ba.css",revision:null},{url:"/fonts/Bellota-Light.0277ce35.ttf",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNa.4ad034d2.woff",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.13749f83.woff2",revision:null},{url:"/guest-particlesjs-config.json",revision:"aab449b324c5a17b76401ad39f50090b"},{url:"/img/capsule2.efa435a4.png",revision:null},{url:"/img/controle2.ee12c8bc.jpg",revision:null},{url:"/img/demande3.593b0d7f.jpg",revision:null},{url:"/img/gelules.e6c37735.png",revision:null},{url:"/img/molecule.f42c6dc4.jpg",revision:null},{url:"/index.html",revision:"ca009b7b2dc4c0c857286be0cf0183a3"},{url:"/js/app.08234251.js",revision:null},{url:"/js/chunk-vendors.0b9e44b3.js",revision:null},{url:"/manifest.json",revision:"629c49e8179ec2ae20fb5c76f49dcc44"},{url:"/particlesjs-config.json",revision:"5a44728a5d93b079d7375160c4ac15d2"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map
