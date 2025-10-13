document.addEventListener("DOMContentLoaded", (event) => {
	console.log('hi')
	const content_root = document.getElementById('main-content');
	const img_tin = [...content_root.getElementsByTagName('img')];

	console.log(img_tin)
	for (let i=0;i<img_tin.length;i++){
		let img = img_tin[i];
		let wrapper = document.createElement('button');
		wrapper.setAttribute('type', 'button');	
		content_root.insertBefore(wrapper, img);
		wrapper.appendChild(img);
	}
});