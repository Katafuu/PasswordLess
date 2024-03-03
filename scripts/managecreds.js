

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
	const ID = json_data['credid'];
	delete json_data.credid;

  for(const key in json_data) { // adding data to tblrec element
		const tbl_dat = document.createElement('td');
		if(key == 'password') {
			tbl_dat.setAttribute('class','pwd')
		};
		tbl_dat.innerText = json_data[key];
		tbl_rec.appendChild(tbl_dat);
  };
	const delBtn_dat = document.createElement('td');
	const modifyBtn_dat = document.createElement('td');
	const viewHistoryBtn_dat = document.createElement('td');
	const delBtn = document.createElement('button');
	const modifyBtn = document.createElement('button');
	const viewHistoryBtn = document.createElement('button')
	viewHistoryBtn.innerText = "ˇ"
	viewHistoryBtn.title = "View Credential History"
	modifyBtn.innerText = '~';
	modifyBtn.title = "Modfy Credential"
	delBtn.innerText = '-';
	delBtn.title = "Delete Credential"
  const attributes = {
		'class': 'delBtn',
		'id': ID
	};
	setAttributes(delBtn, attributes);
	attributes['class'] = 'tblBtn modifyBtn';
	setAttributes(modifyBtn, attributes)
	attributes['class'] = 'tblBtn viewHistoryBtn'
	setAttributes(viewHistoryBtn, attributes)


	delBtn_dat.appendChild(delBtn)
	modifyBtn_dat.appendChild(modifyBtn)
	viewHistoryBtn_dat.appendChild(viewHistoryBtn)

	tbl_rec.appendChild(delBtn_dat)
	tbl_rec.appendChild(modifyBtn_dat)
	tbl_rec.appendChild(viewHistoryBtn_dat)
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
  window.location.href = './modifyCred.html?credid='+btn.id+"&site="+fillerValues[0]+'&username='+fillerValues[1]+'&email='+fillerValues[2]+'&pwd='+fillerValues[3]; // test/debug this, then this page will be basically done
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

$(document).ready(function(){
	const token = getCookieToken();
	if(!token) {
		// window.location.href = "/loginsignup.html?created=SessionTimeOut"
	};
	const headers = {'Authorization': 'Bearer '+token}
	fetch("https://passwordless.duckdns.org:8000/creds/getCreds", {headers})
	.then(data => data.json())
	.then(function(data) {
		console.log(data)
	  // clearElement("credBody")
    for(let i = 0; i < data.length; i++) {
    	addTblRecord('credList',data[i]);
  	};
		delBtns = document.querySelectorAll(".delBtn");
		modifyBtns = document.querySelectorAll('.modifyBtn');
		viewHistoryBtns = document.querySelectorAll('.viewHistoryBtn')
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
				window.location.href = "/view?credid="+btn.id
			});
		});
  });
});

