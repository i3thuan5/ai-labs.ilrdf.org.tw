document.addEventListener("DOMContentLoaded", (event) => {
	const content_root = document.getElementById('main-content');
	const img_tin = [...content_root.getElementsByTagName('img')];

	for (let i=0;i<img_tin.length;i++){
		let img = img_tin[i];
		let wrapper = document.createElement('button');
		wrapper.setAttribute('type', 'button');	
		wrapper.setAttribute('data-bs-toggle', 'modal');
		wrapper.setAttribute('data-bs-target', '#myModal' + i);
		content_root.insertBefore(wrapper, img);
		wrapper.appendChild(img);
		createModelElement(i);
	}

	function createModelElement(mid){
		const parser = new DOMParser();
		let html = `
			<!-- Modal -->
			<div class="modal fade" id="myModal${mid}" tabindex="-1" 
				aria-labelledby="modalabel${mid}" aria-hidden="true">
			  <div class="modal-dialog">
			    <div class="modal-content">
			      <div class="modal-header">
					<span id="modalabel${mid}"></span>
			        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			      </div>
			      <div class="modal-body"></div>
			      <div class="modal-footer">
			        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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
		var myModal = new bootstrap.Modal(document.getElementById('myModal' + mid), {
			backdrop: true,
			keyboard: true,
			focus: true
		});
		modalElement.addEventListener('shown.bs.modal', function (event) {
			const upclosebtn = modalElement.getElementsByClassName('btn-close')[0];
			if(upclosebtn){
				console.log('upclosebtn', upclosebtn)
				upclosebtn.focus();
			}
		});
	}
});
