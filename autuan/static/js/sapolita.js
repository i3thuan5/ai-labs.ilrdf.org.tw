document.addEventListener("DOMContentLoaded", (event) => {
	const content_root = document.getElementById('main-content');
	const img_tin = [...content_root.getElementsByTagName('img')];

	for (let i=0;i<img_tin.length;i++){
		let img = img_tin[i];
		let btn = document.createElement('button');
		btn.setAttribute('type', 'button');
		btn.dataset.bsToggle = 'modal';
		btn.dataset.bsTarget = '#myModal' + i;

		img.before(btn);
		btn.appendChild(img);
		createModelElement(i, img);

	}

	function createModelElement(mid, img){
		const parser = new DOMParser();
		const src = img.getAttribute('src');
		const alt = img.getAttribute('alt');
		let html = DOMPurify.sanitize(`
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
			      			<img src="${src}" alt="${alt}" class="border border-dark sa-img"></div>
					    </div>
					</div>
			      </div>
			    </div>
			  </div>
			</div>`);

		const doc = parser.parseFromString(html, "text/html");
		const modalElement = doc.body.firstElementChild;

	    if (!modalElement) {
	        console.error("無法從 HTML 字串中解析出 Modal 元素。");
	        return;
	    }

		document.body.appendChild(modalElement);
		modalElement.addEventListener('shown.bs.modal', function (event) {
			const upclosebtn = modalElement.getElementsByClassName('btn-close')[0];
			if(upclosebtn){
				upclosebtn.focus();
			}
		});
	}
});
