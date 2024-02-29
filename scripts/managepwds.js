
function addListItem(lstid, data) {
  const vallist = document.getElementById(lstid);

	var newListItem = document.createElement('li');
  var newVal = document.createTextNode(data);
  var newLink = document.createElement('a')
	newLink.setAttribute('href','#')
  newLink.appendChild(newVal);
	newListItem.appendChild(newLink)

  vallist.appendChild(newListItem);
}

function clearList(lstid) {
	const lst = document.getElementById(lstid);
	lst.innerHTML = '';
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

function updateCreds() {
	
};

function addTblRecords(tblid, json_data) {
  const credList = document.getElementById(tblid);
  const tbl_rec = credList.insertRow(-1)
  for(const key in json_data) {
		if(json_data[key] == 'uid' || json_data[key] == 'credid') {
			{}
		}
		else {
			const tbl_dat = document.createElement('td');
			tbl_dat.innerText = json_data[key];
			tbl_rec.appendChild(tbl_dat);
		}
  };
  credList.appendChild(tbl_rec);
};

$(document).ready(function(){
	const token = getCookieToken();
	const headers = {'Authorization': 'Bearer '+token}
	fetch("https://passwordless.duckdns.org:8000/creds/getCreds", {headers})
	.then(data => data.json())
	.then(function(data) {
	console.log(data.json())
	clearList("credList")
    for(const i = 0; i < data.length; i++) {
    	addTblRecords('credList',data[i]);
  	};
  });
});
