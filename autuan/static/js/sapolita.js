document.addEventListener("DOMContentLoaded", (event) => {
    "use strict";

  	const content_root = document.getElementById('main-content');
	let img_tin = [];
	if (content_root) {
		img_tin = [...content_root.getElementsByTagName('img')];
	}

	for (let i=0;i<img_tin.length;i++){
		let img = img_tin[i];
		wrapImgWithButtonElement(i, img);
		createModelElement(i, img);
	}

	function wrapImgWithButtonElement(mid, img){
		let btnElm = document.createElement('button');
		btnElm.setAttribute('type', 'button');
		btnElm.classList.add("modal-toggler-btn", "bg-transparent", "border-0");
		btnElm.dataset.bsToggle = 'modal';
		btnElm.dataset.bsTarget = '#myModal' + mid;
		img.classList.add("border", "border-1");
		img.before(btnElm);
		btnElm.appendChild(img);
	}

	function createModelElement(mid, img){
		const parser = new DOMParser();
		const src = img.getAttribute('src');
		const alt = img.getAttribute('alt');
		let html = `
			<div class="modal fade" id="myModal${mid}" tabindex="-1" 
				aria-labelledby="modalabel${mid}" aria-hidden="true">
			  <div class="modal-dialog modal-dialog-centered">
			    <div class="modal-content">
			      <div class="modal-header border-bottom-0">
					<span id="modalabel${mid}" class="visually-hidden">放大檢視：${alt}</span>
			        <button type="button" class="btn-close" 
			            data-bs-dismiss="modal" aria-label="Close"></button>
			      </div>
			      <div class="modal-body">
					<div class="container">
					    <div class="row">
					      <div class="col-12">
			      			<img src="${src}" alt="${alt}" class="border border-1 sa-img"></div>
					    </div>
					</div>
			      </div>
			    </div>
			  </div>
			</div>`;

		const doc = parser.parseFromString(html, "text/html");
		const modalElement = doc.body.firstElementChild;

	    if (!modalElement) {
	        console.error("無法從 HTML 字串中解析出 Modal 元素。");
	        return;
	    }

		document.body.appendChild(modalElement);
	}
});
