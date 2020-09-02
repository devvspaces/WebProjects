// $(document).ready(function(){

	
	// Code for the navbar
	$('#menu').slicknav({
		label:'',
		prependTo: '.mobile',
		closeOnClick: true,
		closedSymbol: '&#43;',
		openedSymbol: '-'
	});


	// code for signup and login sliding with slick
	try{
		$('#auth').slick({
	        arrows: false,
	        infinite: false,
            draggable: false,
	    });
	} catch(e){
		console.log("Slick is not installed: "+e.message);
	}

	// Code to make any element contenteditable
	function setEdit(obj,bool, style=true) {
		obj.setAttribute('contenteditable', bool);
		if (style) {
			if (bool) {
				obj.style.color='rgba(255, 255, 255, 0.5)';
			} else {
				obj.style.color='white';
			}
		}
	}
   	


	// Code for adding class focus and removing it on markup

	function addcl(){
		let parent = this.parentNode.parentNode;
		parent.classList.add("focus");
	}

	function remcl(){
		let parent = this.parentNode.parentNode;
		if(this.value == ""){
			parent.classList.remove("focus");
		}
	}
	function addModal(){
		let parent = this.parentNode;
		parent.classList.add("focus");
	}

	function remModal(){
		let parent = this.parentNode;
		if(this.value == ""){
			parent.classList.remove("focus");
		}
	}
	function setUpFocusing(){
		let inputs = document.querySelectorAll("input");
		inputs.forEach(input => {
			input.addEventListener("focus", addcl);
			input.addEventListener("blur", remcl);
		});
	}
	setUpFocusing()


	// Same focusing code for modal textarea
	let textarea = document.querySelector(".modal-form textarea");
	try{
		textarea.addEventListener("focus", addModal);
		textarea.addEventListener("blur", remModal);
	} catch(e){
		console.log(e.message);
	}

	// Code to make sure all links in todo card i.e. edit, delete, save
	// and done or undone does prevent default event when clicked
	$("#todos a").on('click', function(event) {
		if (this.hash == "") {
			event.preventDefault();
		}
	});


	// Code to make todo cards editable and un-editable
	function makeEditable() {
		try{
			let todos = document.querySelector('#todos');
			let edits = document.querySelectorAll('.edit');
			function Editable(i, input) {
				let myForm = input.parentElement
				let fromer = myForm.children[3]
				let todo_text = myForm.children[1]
				p = todos.children[i].children[1];
				if(p.isContentEditable){
					setEdit(p,false, false);
					input.innerHTML='<i class="fas fa-edit"></i>';
					input.classList.remove('save');
					fromer.value = 'save'
					todo_text.innerHTML = p.innerHTML
					input.nextElementSibling.style.display = 'none'
				} else {
					setEdit(p,true, false);
					input.innerHTML='<i class="fas fa-save"></i>';
					input.classList.add('save');
					fromer.value = 'edit'
					input.nextElementSibling.style.display = 'block'
				}
			}
			let p = 0;
			edits.forEach(input => {
				input.onclick=function () {
					let i=0;
					edits.forEach(input2 => {
						if (input.isSameNode(input2)) {
							Editable(i, input);
						}
						i++;
					});
				};
			});
		} catch(e){
			console.log(e);
		}
	}
	makeEditable()

	// Code for listening to Todo card select onchange
	function callListen() {
		let selects = document.querySelectorAll('#todos .todo-card .my-ajax-form .todo_category')
		selects.forEach(i=>{
			i.addEventListener('change', function(e) {
				let category = {'ST': 'Short Term', 'LT': 'Long Term'}[e.target.value]
				e.path[2].firstElementChild.lastElementChild.innerHTML = category
			})
		})
	}
	callListen()

	function makeDoable() {
		try{
			let ajax_do = document.querySelectorAll('#todos .todo-card form button.close')
			ajax_do.forEach(a=>{
				a.onclick=function () {
					let fromer = this.parentElement.children[3]
					fromer.value = 'done'
					let todo_card = this.parentElement.parentElement
					if (todo_card.getAttribute('data-clicked') == 'True'){
						todo_card.setAttribute('data-clicked', 'False')
					} else {
						todo_card.setAttribute('data-clicked', 'True')
					}
				}
			})
		} catch(e){
			print(e)
		}
	}
	makeDoable()

	function fade(obj, time=300) {
		obj.style.transition = (time/1000).toString()+'s'
		obj.style.opacity = '0'
		setTimeout(function() {
			obj.remove()
		}, time)
	}

	function shrink(obj, time=300) {
		obj.style.transition = (time/1000).toString()+'s'
		obj.style.overflow = 'hidden'
		obj.style.height = obj.offsetHeight.toString()+'px'
		obj.style.width = '0px'
		print(obj.style.height)
		obj.style.height = '0px'
		setTimeout(function() {
			obj.remove()
		}, time)
	}

	function makeDeletable() {
		try{
			let ajax_delete = document.querySelectorAll('#todos .todo-card form button.delete')
			ajax_delete.forEach(a=>{
				a.onclick=function () {
					let fromer = this.parentElement.children[3]
					fromer.value = 'delete'
					let todo_card = this.parentElement.parentElement
					fade(todo_card)
				}
			})
		} catch(e){
			print(e)
		}
	}
	makeDeletable()
	

	// Code for changing profile card to being editable
	$("#save").on('click', function() {
		let parent = this.parentNode;
		let editable = function(bool){
			let colors = {
				1: 'rgba(255,255,255, 0.4)',
				0: '#5cbf60'
			};
			arr=[0,1];
			arr.forEach(n => {
				let node = parent.children[1].children[n];
				// node.setAttribute('contenteditable',bool);
				setEdit(node,bool,false);
				if (bool=='true'){
					node.style.color='white';
				} else {
					node.style.color=colors[n];
				}
			});
		}
		let editImg = document.querySelector('#edit-img');
		if (parent.getAttribute('editable')) {
			parent.setAttribute('editable', '');
			let details = this.previousElementSibling.children
			let name = details[0]
			let email = details[1]
			let profileForm = document.querySelector('#header form')
			let input_details = profileForm.children
			let input_name = input_details[input_details.length-3]
			let input_email = input_details[input_details.length-2]
			input_name.value = name.innerText
			input_email.value = email.innerText
			editable('false');
			this.innerHTML='<span><i class="fas fa-edit"></i></span>Edit';
			editImg.style.opacity='0';
			editImg.style.cursor='default';
			editImg.setAttribute('disabled', '');
			profileForm.submit()
		} else {
			parent.setAttribute('editable', 'true');
			editable('true');
			this.innerHTML='<span><i class="fas fa-save"></i></span>Save';
			editImg.style.opacity='1';
			editImg.style.cursor='pointer';
			editImg.removeAttribute('disabled');
		}
	});



	// Code for previewing images
	function showImage(src, target) {
		var fr = new FileReader();
		fr.onload=function(e) {
			target.src = this.result;
			target.parentElement.style.background='transparent'
		}
		src.addEventListener('change', function() {
			fr.readAsDataURL(src.files[0]);
		});
	}
	try{
		var src = document.getElementById('src');
		var target = document.getElementById('target');
		showImage(src,target);
	} catch(e){
		print(e)
	}

	try{
		let modalImage = document.querySelector('#modal-image .modal-save')
		let modalImageForm = document.querySelector('#modal-image form')
		// modalImage.onclick = function () {
		// 	mes()
		// }
		modal_closes('#modal-image .modal-save', 5)
		// function mes(){
		// }
		modalImageForm.addEventListener('submit', mess)
		function mess(e){
			e.preventDefault()
			let imgPic = document.querySelector('#img-pic img')
			let dataUri = e.target.children[1].firstElementChild.src
			let profileForm = document.querySelector('#header form')
			let a = e.target.children[2].cloneNode()
			if (profileForm.children[0].getAttribute('name') == 'image') {
				profileForm.children[0].remove()
			}
			profileForm.insertBefore(a, profileForm.children[0])
			if (dataUri.length > 100) {
				imgPic.src = dataUri
			}
		}
	} catch(e){
		print(e)
	}
	



	// Code for starting modal
	let body =document.querySelector('body');
	function openModal(target) {
		target.style.width='100%';
		target.style.height='100vh';
		target.style.top='0';
		target.style.left='0';
		target.style.opacity='1';
		// Code to make sure body doesn't scroll when modal in on
		body.style.position='fixed';
		body.style.top='0';
		body.style.left='0';
	}
	
	function closeModal(target){
		target.style.width='0';
		target.style.height='0';
		target.style.top='50%';
		target.style.left='50%';
		target.style.opacity='0';
		body.style.position='relative';
	}

	let modalBtn = document.querySelectorAll('.modal-btn');
	modalBtn.forEach(input=>{
		input.onclick=function(){
			let target=this.dataset.target.toString();
			target=document.querySelector(target);
			if (target.style.width!='100%') {
				openModal(target);
			}
		}
	});


	function modal_closes(selector, iterations) {
		let close = document.querySelectorAll(selector);
		close.forEach(input=>{
			input.onclick=function(){
				obj = this
				for (var i = iterations - 1; i >= 0; i--) {
					obj=obj.parentNode
				}
				closeModal(obj);
			}
		});
	}
	modal_closes('.modal-close', 3)
	// modal_closes('.modal-save', 5)

	// Code to make password visible and hidden
	let eye = $('.eye');
	eye.toArray().forEach(input=>{
		input.onclick=function(){
			let obj = this.parentNode.firstElementChild;
			if (obj.attributes[0].value=='password') {
				obj.setAttribute('type','text');
				this.innerHTML='<i class="fas fa-eye"></i>';
				this.style.color='#5cbf60';
				this.classList.add('hide');
			} else {
				obj.setAttribute('type','password');
				this.innerHTML='<i class="fas fa-eye-slash"></i>';
				this.style.color='#6a6b6e';
				this.classList.remove('hide');
			}
		}
	});
	

	
	// Code for making answer show in QA
	
	function openAnswer(obj, input, svg) {
		obj.style.height='1rem';
		obj.style.padding='0.6rem 0';
		input.innerHTML=svg;
		input.style.color='#5cbf60';
		input.classList.add('toggled');
	}
	function closeAnswer(obj, input, svg) {
		obj.style.height='0px';
		obj.style.padding='0px';
		input.innerHTML=svg;
		input.style.color='rgba(7,9,14, 0.4)';
		input.classList.remove('toggled');
		if (input.parentNode.children[3].classList.contains('toggled')) {
			closeAnswer(obj, input.parentNode.children[3], '<i class="fas fa-eye-slash"></i>');
		}
	}

	function qaShowFunc() {
		let qaShow = document.querySelectorAll('.show');
		qaShow.forEach(input=>{
			input.onclick=function(){
				let obj = this.parentNode.parentNode.parentNode.lastElementChild;
				if ((obj.style.height=='' || obj.style.height=='0px') || this.nextElementSibling.classList.contains('toggled')) {
					openAnswer(obj, this, '<i class="fas fa-eye"></i>');

				} else {
					closeAnswer(obj, this, '<i class="fas fa-eye-slash"></i>');
				}
			}
		});	
	}

	// Code for making answer and question editable in QA
	function qaEditFunc() {
		let qaEdit = document.querySelectorAll('#QA .qas .qa .head .edit');
		qaEdit.forEach(input=>{
			input.onclick=function(){
				let obj = this.parentNode.parentNode.parentNode.children[2];
				let obj2 = this.parentNode.parentNode.parentNode.children[1];
				if (obj.style.height=='' || obj.style.height=='0px' || (this.previousElementSibling.classList.contains('toggled') && !this.classList.contains('toggled'))) {
					openAnswer(obj, this, '<i class="fas fa-save"></i>');
					setEdit(obj.firstElementChild,true);
					setEdit(obj2.firstElementChild,true);
					this.parentNode.children[2].value = 'edit'
				} else {
					closeAnswer(obj, this, '<i class="fas fa-edit"></i>');
					setEdit(obj.firstElementChild,false);
					setEdit(obj2.firstElementChild,false);
					this.parentNode.children[0].value = obj2.firstElementChild.innerText
					this.parentNode.children[1].value = obj.firstElementChild.innerText
					this.parentNode.children[2].value = 'save'
				}
			}
		});	
	}

	function qaDeleteFunc() {
		let qaEdit = document.querySelectorAll('#QA .qas .qa .head .delete');
		qaEdit.forEach(input=>{
			input.onclick=function(){
				this.parentNode.children[2].value = 'delete'
				fade(this.parentNode.parentNode.parentNode)
			}
		});	
	}

	qaShowFunc();
	qaEditFunc();
	qaDeleteFunc();

	// Code for making add button in qa to add new nodes to qa
	try{
		let qaAdd = document.querySelector('.add');
		qaAdd.onclick=function() {
			let obj = this.parentNode;
			let data_url = obj.children[0].children[0].children[0].getAttribute('data-url');
			let div = document.createElement('div');
			div.className='qa';
			div.innerHTML= `<div class="head">
								<form method="POST" class="my-ajax-form" action='.' data-url=`+data_url+`>
                                    <input type="text" name="question">
                                    <input type="text" name="answer">
                                    <input type="text" name="from">
                                    <input type="text" name="pk" value='-1'>
                                    <button class="show" type="button"><i class="fas fa-eye-slash"></i></button>
                                    <button class="edit" type='submit'><i class="fas fa-edit"></i></button>
                                    <button class="delete" type='submit'><i class="fas fa-trash-alt"></i></button>
                                </form>
							</div>
							<div class="question">
								<p>Question</p>
							</div>
							<div class="answer">
								<p>Answer</p>
							</div>`
			obj.insertBefore(div,this);
			qaShowFunc();
			qaEditFunc();
			qaDeleteFunc();
			let form = div.firstElementChild.firstElementChild
		    form.addEventListener('submit',function(event){
		        event.preventDefault()
		        resetForm()
		        var $formData = $(this).serialize()
		        var $thisURL = form.getAttribute('data-url') || window.location.href // or set your own url
		        $.ajax({
		            method: "POST",
		            url: $thisURL,
		            data: $formData,
		            success: handleFormSuccess,
		            error: handleFormError,
		            complete: destroyLoader,
		        })
		    })
		}
	} catch(e) {
		print(e)
	}

	// Code for adding todo nodes to parent
	function addTodo(response) {
		try{
			let obj = document.querySelector("#todos");
			let crsf_token = obj.firstElementChild.lastElementChild.firstElementChild.getAttribute('value')
			let category = {'ST': 'Short Term', 'LT': 'Long Term'}[response['category']]
			let selectCategory = ''
			if(response['category'] == 'ST'){
				selectCategory = `<option value="LT">Long Term</option>
                                  <option selected="" value="ST">Short Term</option>`
			} else {
				selectCategory = `<option selected="" value="LT">Long Term</option>
                                  	  <option value="ST">Short Term</option>`
			}
			let div = document.createElement('div');
			div.className='todo-card';
			div.setAttribute('data-clicked', 'False');
			div.innerHTML= `<p class="date">`+response['date']+`<br>
                                `+category+`
                            </p>
                            <p>`+response['todo']+`<br><small>Refresh to edit</small></p>
                            <form method="POST" class="my-ajax-form" action="." data-url="http://127.0.0.1:8000/">
                                <input type="hidden" name="csrfmiddlewaretoken" value=`+crsf_token+`>
                                <textarea name="todo">`+response['todo']+`</textarea>
                                <input type="text" name="tid" value=`+response['tid']+`>
                                <input type="text" class="fromer" name="from">
                                <button type="submit" class="close"><i class="fas fa-check-circle"></i></button>
                                <button  type="submit" class="delete"><span class="fas fa-trash-alt"></span></button>
                                <button  type="submit" class="edit"><span class="fas fa-edit"></span></button>
                                <select name="category" class="todo_category" value=`+response['category']+`>
                                 `+selectCategory+`   
                                </select>
                            </form>`
			obj.insertBefore(div, obj.childNodes[obj.childNodes.length-1])
			makeEditable()
			makeDoable()
			makeDeletable()
		} catch(e) {
			print(e)
		}
	}

	// Code to set alert
	function setAlert(str, status='success') {
		let alert = document.querySelector('.alert');
		if (status != 'success') {
			alert.firstElementChild.style.backgroundColor = 'rgba(232,111,74,0.99)';
		} else {
			alert.firstElementChild.style.backgroundColor = 'rgba(114,226,110,0.99)';
		}
		alert.firstElementChild.firstElementChild.innerHTML = str;
		alert.style.opacity = '1';
		setTimeout(function(){
			alert.style.opacity = '0';
		}, 3000)
	}
// });