document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  console.log("toc.js")
  let headings = document
    .getElementById("main-content")
    .querySelectorAll("h2, h3");
  let hlength = headings.length;
  let toc = [];
  let tocitem = {};

  function initHeadDict() {
    for (let soo = 0; soo < hlength; soo++) {
      let h = headings[soo];
      let hid = `hid${soo}`;
      if (h.tagName == "H2") {
        tocitem = {
          h2: h,
          h3s: [],
        };
        toc.push(tocitem);
      } else {
        tocitem.h3s.push(h);
      }
      h.setAttribute("id", hid);
    }
  }

  function createLiA(h) {
    let link = `#${h.getAttribute("id")}`;
    let text = h.innerText;
    let li = document.createElement("li");
    li.classList.add("nav-item");
    let a = document.createElement("a");
    a.setAttribute("href", link);
    a.classList.add("nav-link");
    a.innerHTML = text;
    li.append(a);
    return li;
  }

  function convertHeadDictToHTML() {
    if (hlength) {
      let tocElement = document.getElementById("toc");
      let titleElment = document.createElement("span");
      let listElment = document.createElement("ul");
      titleElment.innerText = '頁面索引';
      tocElement.appendChild(titleElment);
      listElment.classList.add("nav", "flex-column");
      for (let i = 0; i < toc.length; i++) {
        let h2 = toc[i].h2;
        let h3s = toc[i].h3s;
        let lv2 = createLiA(h2);
        if (h3s) {
          let lv3 = document.createElement("ul");
          lv3.classList.add("nav", "flex-column", "ms-3");
          for (let j = 0; j < h3s.length; j++) {
            let li3 = createLiA(h3s[j]);
            lv3.append(li3);
          }
          lv2.append(lv3);
        }
        listElment.appendChild(lv2);
      }
      tocElement.appendChild(listElment);
      tocElement.classList.remove("hide");
    }
  }

  function appendSuffixAnchor(){
    for (let soo = 0; soo < hlength; soo++) {
      let h = headings[soo];
      let hid = `hid${soo}`;
      let hanchor = document.createElement('a');
      hanchor.innerHTML = '#';
      hanchor.setAttribute("href",`#${hid}`);
      hanchor.classList.add("ms-1");
      h.appendChild(hanchor);
    }
  }
  initHeadDict();
  convertHeadDictToHTML();
  appendSuffixAnchor();
});
