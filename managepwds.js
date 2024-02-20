// function sendSignupData() {
// 	const options = {
// 		method: 'POST',
// 		headers: {
// 				'Content-Type':
// 						'application/json'
// 		},
// 		body: JSON.stringify({
//       uid: null,  // need to find a way to get uid perhaps from login session which is incomplete atm
// 			site: window.location.href.split(/[?#]/)[0],
//       email: document.querySelector('input[type=email]').value,
// 			username: document.querySelector('input[type=text]').value,
// 			password: document.querySelector('input[type=password]').value
// 		},)
// 	};
// 	let fetchRes = fetch("http://192.168.0.135:8000/addCred",options);
// 		fetchRes.then(res => res.json())
// 		.then(d => {console.log(d)});
// }; 

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

function updateCreds() {
	fetch("http://192.168.0.135:8000/users/getAll")
	.then(data => data.json())
	.then(function(data) {
	clearList("credList")
    for (x = 0;x<data.length;x++) {
      addListItem("credList",data[x]);
    }
  });
}

$(document).ready(function(){
	updateCreds()
	});

