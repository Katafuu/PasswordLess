function setAttributes(element, attributes) { // https://bobbyhadz.com/blog/javascript-set-multiple-attributes-to-element
	Object.keys(attributes).forEach(attr => {
		element.setAttribute(attr, attributes[attr])
	});
};
function addTblRecord(tblid, json_data) {
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

    const delBtn = document.createElement('button');
    const modifyBtn = document.createElement('button');

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
  
  
    delBtn_dat.appendChild(delBtn)
    modifyBtn_dat.appendChild(modifyBtn)
  
    tbl_rec.appendChild(delBtn_dat)
    tbl_rec.appendChild(modifyBtn_dat)
    tbl_rec.appendChild(viewHistoryBtn_dat)
    credList.appendChild(tbl_rec);
  };
}
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

$(document).ready(function() {
  const searchParams = new URLSearchParams(window.location.search);
  const credid = searchParams.get("credid");
  const token = getCookieToken();
	if(!token) {
		window.location.href = "/loginsignup.html?created=SessionTimeOut"
	};
	const headers = {'Authorization': 'Bearer '+token}
	fetch("https://passwordless.duckdns.org:8000/creds/getOldCreds?credid="+credid, {headers})
	.then(data => data.json())
	.then(function(data) {
	  clearElement("credBody")
    for(let i = 0; i < data.length; i++) {
    	addTblRecord('credList',data[i]);
  	};
		delBtns = document.querySelectorAll(".delBtn");
		delBtns.forEach(function(btn) {
			btn.addEventListener('click', function() {
				delCred(btn.id)
			});
		});
  });
});