

function clearElement(id) {
	const element = document.getElementById(id);
	element.innerHTML = '';
}
function getCookieToken() {
	let cookies = document.cookie.split(';');
	for(let i = 0; i < cookies.length; i++) {
	  cookies[i] = cookies[i].split('=')
	};
	for (let x = 0; x < cookies.length; x++){
	  if (cookies[x][0] == 'token') {
		  return cookies[x][1];
	  }
    else {
      return null
    };
	};
};

function setAttributes(element, attributes) { // https://bobbyhadz.com/blog/javascript-set-multiple-attributes-to-element
	Object.keys(attributes).forEach(attr => {
		element.setAttribute(attr, attributes[attr])
	});
};
function addTblRecords(tblid, json_data) {
  const credList = document.getElementById(tblid);
  const tbl_rec = credList.insertRow(-1)
  for(const key in json_data) {
		if(json_data[key] == 'uid') {
			{}
		}
		else if(json_data[key] == 'credid') {
			const ID = json_data[key]
		}
		else {
			const tbl_dat = document.createElement('td');
			if(key == 'password') {
				tbl_dat.setAttribute('class','pwd')
			};
			tbl_dat.innerText = json_data[key];
			tbl_rec.appendChild(tbl_dat);
		}
  };
	const delBtn_dat = document.createElement('td');
	const modifyBtn_dat = document.createElement('td');
	const delBtn = document.createElement('input');
	const modifyBtn = document.createElement('input');
	modifyBtn.value = 'Modify';
	delBtn.value = 'Delete';
  const attributes = {
		'type': 'button',
		'class': 'tblBtn delBtn',
		'id': ID
	};
	setAttributes(delBtn, attributes);
	attributes['class'] = 'tblBtn modifyBtn';
	setAttributes(modifyBtn, attributes)

	delBtn_dat.appendChild(delBtn)
	modifyBtn_dat.appendChild(modifyBtn)

	tbl_rec.appendChild(delBtn_dat)
	tbl_rec.appendChild(modifyBtn_dat)
  credList.appendChild(tbl_rec);
};
function redirectAdd() {
	window.location.href = "./addPwd"
};
function redirectModify(btn) {
	const row = btn.parentNode;
	var lst = [];
	for (const data in row) {
		lst.push(data.innerText)
	}
	window.location.href = './modifyCred.html?credid='+btn.id+"&site="+lst[0]+'&email='+lst[1]+'&username='+lst[2]+'&pwd='+lst[3]; // test/debug this, then this page will be basically done
};

function delCred(id) {
	const options = {
		method: 'DELETE',
		headers: {
			'Authorization': getCookieToken()
		},
		body: {'credid': id, 'save': save}
	};
	fetch('https://passwordless.duckdns.org:8000/creds/delCred', options)
	.then(data => data.json())
	.then(function(data) {
		if(data) {
			alert('Successfully deleted, it can be found in your password history')
		}
	})
}


$(document).ready(function(){
	const token = getCookieToken();
	const headers = {'Authorization': 'Bearer '+token}
	fetch("https://passwordless.duckdns.org:8000/creds/getCreds", {headers})
	.then(data => data.json())
	.then(function(data) {
		console.log(data)
	  clearElement("credList")
    for(let i = 0; i < data.length; i++) {
    	addTblRecords('credList',data[i]);
  	};
  });
	delBtns = document.querySelectorAll('.delBtn');
	modifyBtns = document.querySelectorAll('.modifyBtn')
	for(const btn of delBtns) {
		alert(btn.id) //temp
		btn.addEventListener('click', delCred(btn.id))
	};
	for(const tbn of modifyBtns) {
		btn.addEventListener('click', redirectModify(btn));
	};
});

