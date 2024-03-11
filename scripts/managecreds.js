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
function addTblRecord(tblid, json_data) {
  const credList = document.getElementById(tblid);
  const tbl_rec = credList.insertRow(-1);
	const ID = json_data['id'];
	delete json_data.id;

  for(const key in json_data) { // adding data to tblrec element
		const tbl_dat = document.createElement('td');
		if(key == 'password') {
			tbl_dat.setAttribute('class','pwd');
			tbl_dat.id = ID;
		};
		tbl_dat.innerText = json_data[key];
		tbl_rec.appendChild(tbl_dat);
  };
	const delBtn_dat = document.createElement('td');
	const modifyBtn_dat = document.createElement('td');
	const viewHistoryBtn_dat = document.createElement('td');
	const delBtn = document.createElement('button');
	const modifyBtn = document.createElement('button');
	const viewHistoryBtn = document.createElement('button');
	viewHistoryBtn.title = "View Credential History";
	modifyBtn.title = "Modfy Credential";
	delBtn.title = "Delete Credential";
	const delBtn_icon = document.createElement('i');
	const modifyBtn_icon = document.createElement('i');
	const viewHistoryBtn_icon = document.createElement('i');
	delBtn_icon.setAttribute('class',"fa fa-trash fa-xl");
	modifyBtn_icon.setAttribute('class',"fa fa-pencil fa-xl");
	viewHistoryBtn_icon.setAttribute('class',"fa fa-eye fa-xl");

	delBtn.appendChild(delBtn_icon);
	modifyBtn.appendChild(modifyBtn_icon);
	viewHistoryBtn.appendChild(viewHistoryBtn_icon);

  const attributes = {
		'class': 'btn delBtn',
		'id': ID
	};
	setAttributes(delBtn, attributes);
	attributes['class'] = 'btn modifyBtn';
	setAttributes(modifyBtn, attributes);
	attributes['class'] = 'btn viewHistoryBtn';
	setAttributes(viewHistoryBtn, attributes);

	delBtn_dat.appendChild(delBtn);
	modifyBtn_dat.appendChild(modifyBtn);
	viewHistoryBtn_dat.appendChild(viewHistoryBtn);

	viewHistoryBtn_dat.setAttribute('class','tblBtn');
	delBtn_dat.setAttribute('class','tblBtn');
	modifyBtn_dat.setAttribute('class','tblBtn');
	tbl_rec.appendChild(viewHistoryBtn_dat);
	tbl_rec.appendChild(modifyBtn_dat);
	tbl_rec.appendChild(delBtn_dat);
  credList.appendChild(tbl_rec);
};
function redirectAdd() {
	window.location.href = "./addCred.html"
};
function redirectModify(btn) {
	const row = btn.parentNode.parentNode;
	const fillerValues = [];
	data = row.querySelectorAll('td')
	for (const value of data.values()) {
		fillerValues.push(value.innerText)
	}
  window.location.href = './modifyCred.html?credid='+btn.id+"&site="+fillerValues[0]+'&username='+fillerValues[1]+'&email='+fillerValues[2]; // test/debug this, then this page will be basically done
};
function delCred(id) {
	const token = getCookieToken();
	const options = {
		method: 'DELETE',
		headers: {
			'Authorization': 'Bearer '+token
		}
	};
	fetch('https://passwordless.duckdns.org:8000/creds/delCred?credid='+id, options)
	.then(data => data.json())
	.catch(console.log(error))
	.then(function(data) {
		if(data) {
			alert('Successfully deleted, it can be found in your password history')
		};
	});
};
function updateCreds(Creds) {
	clearElement("credBody")
	for(let i = 0; i < Creds.length; i++) {
		addTblRecord('credBody',Creds[i]);
	};
	delBtns = document.querySelectorAll(".delBtn");
	modifyBtns = document.querySelectorAll('.modifyBtn');
	viewHistoryBtns = document.querySelectorAll('.viewHistoryBtn')
	pwdCells = document.querySelectorAll('.pwd')
	delBtns.forEach(function(btn) {
		btn.addEventListener('click', function() {
			delCred(btn.id)
		});
	});
	modifyBtns.forEach(function(btn) {
		btn.addEventListener('click', function() {
			redirectModify(btn)
		});
	});
	viewHistoryBtns.forEach(function(btn) {
		btn.addEventListener('click', function() {
			window.location.href = "/view.html?credid="+btn.id
		});
	});
	pwdCells.forEach(function(cell) {
		cell.addEventListener('click', function() {
			displayPassword(cell)
		}, {once: true});
	});
};
function displayPassword(pwdcell) {
	const token = getCookieToken();
	options = {
		method: "GET",
		headers: {"Authorization": "Bearer "+token}
	};
	fetch("https://passwordless.duckdns.org:8000/creds/getDecryptPassword?tbl=c&credid="+pwdcell.id, options)
	.catch(console.error())
	.then(data => data.json())
	.then(function(data) {
		credid = pwdcell.id
		pwdcell.innerText = data[credid];
	});
};
function refresh() {
	const token = getCookieToken();
	const headers = {'Authorization': 'Bearer '+token};
	fetch("https://passwordless.duckdns.org:8000/creds/getCreds",{headers})
	.then(data => data.json())
	.then(function(data) {
		updateCreds(data);
	});
};
$(document).ready(function(){
	const token = getCookieToken();
	if(!token) {
		window.location.href = "/loginsignup.html?created=SessionTimeOut"
	};
	refresh();
});


