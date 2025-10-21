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

  let headings = [];
  try {
    headings = document
      .getElementById("main-content")
      .querySelectorAll("h2, h3");
    } catch (e) {
  }
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

  function convertHeadDictToHTML() {
    if (hlength) {
      let tocElement = document.getElementById("toc");
      let titleElment = document.createElement("span");
      let listElment = document.createElement("ul");
      titleElment.innerText = '頁面索引';
      tocElement.appendChild(titleElment);
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
