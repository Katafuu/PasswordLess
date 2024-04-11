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
  const delBtn = document.createElement('button');
	const delBtn_icon = document.createElement('i');
	delBtn_icon.setAttribute('class',"fa fa-trash fa-xl");
  delBtn.title = "Delete Credential"
  const attributes = {
    'class': 'delBtn',
    'id': ID
  };
  setAttributes(delBtn, attributes);
  delBtn_dat.setAttribute('class', 'tblBtn')
  delBtn_dat.appendChild(delBtn)
  tbl_rec.appendChild(delBtn_dat)
  credList.appendChild(tbl_rec);
};

function delCred(id) {
	const token = getCookieToken();
	const options = {
		method: 'DELETE',
		headers: {
			'Authorization': 'Bearer '+token
		}
	};
	fetch('https://passwordless.duckdns.org:8000/creds/delOldCred?credid='+id, options)
	.then(data => data.json())
	.catch(console.log(error))
	.then(function(data) {
		if(data) {
			alert('Successfully deleted from credential history')
		};
	});
};
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
function clearElement(id) {
	const element = document.getElementById(id);
	element.innerHTML = '';
};
function displayPassword(pwdcell) {
	const token = getCookieToken();
	options = {
		method: "GET",
		headers: {"Authorization": "Bearer "+token}
	};
	fetch("https://passwordless.duckdns.org:8000/creds/getDecryptPassword?tbl=old&credid="+pwdcell.id, options)
	.catch(console.error())
	.then(data => data.json())
	.then(function(data) {
		credid = pwdcell.id
		pwdcell.innerText = data[credid];
	});
};
function updateCreds(Creds) {
	clearElement("credBody")
	for(let i = 0; i < Creds.length; i++) {
		addTblRecord('credBody',Creds[i]);
	};
	delBtns = document.querySelectorAll(".delBtn");
	pwdCells = document.querySelectorAll('.pwd')
	delBtns.forEach(function(btn) {
		btn.addEventListener('click', function() {
		delCred(btn.id)
		});
	});
	pwdCells.forEach(function(cell) {
		cell.addEventListener('click', function() {
			displayPassword(cell)
		}, {once: true});
	});
};

function refresh() {
	const token = getCookieToken();
	if(!token) {
		window.location.href = "/loginsignup.html?status=SessionTimeOut"
	};
	const searchParams = new URLSearchParams(window.location.search);
  const credid = searchParams.get("credid");
	const headers = {'Authorization': 'Bearer '+token};
	fetch("https://passwordless.duckdns.org:8000/creds/getOldCreds?tbl=old&credid="+credid, {headers})
	.then(data => data.json())
	.then(function(data) {
		console.log(data)
    updateCreds(data)
  });
}