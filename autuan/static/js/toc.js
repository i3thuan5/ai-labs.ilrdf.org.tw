function createLiA(h) {
  "use strict";

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

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  let mainContent = document.getElementById("main-content");
  let headings = [];
  if (mainContent) {
    headings = mainContent.querySelectorAll("h2, h3");
  }
  let hlength = headings.length;
  let toc = [];
  let tocitem = {};

  function initHeadDict() {
    if (hlength) {
        if (headings[0].tagName != "H2") {
          hlength = 0;
        }
    }
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

  function convertHeadDictToHTML() {
    if (hlength) {
      let tocElement = document.getElementById("toc");
      let navElement = document.createElement("nav");
      let titleElment = document.createElement("p");
      let listElment = document.createElement("ul");
      navElement.setAttribute("aria-label", "頁面索引");
      navElement.classList.add("sticky-top","border","border-primary",
        "rounded","bg-primary","bg-opacity-10","p-2","mb-5");
      titleElment.innerText = '頁面索引';
      navElement.appendChild(titleElment);
      listElment.classList.add("nav", "flex-column");
      for (let item of toc) {
        let lv2 = createLiA(item.h2);
        if (item.h3s) {
          let lv3 = document.createElement("ul");
          lv3.classList.add("nav", "flex-column", "ms-3");
          for (let h of item.h3s) {
            let li = createLiA(h);
            lv3.append(li);
          }
          lv2.append(lv3);
        }
        listElment.appendChild(lv2);
      }
      navElement.appendChild(listElment);
      tocElement.appendChild(navElement);
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
