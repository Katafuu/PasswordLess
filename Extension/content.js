function checkField(name){
  let field = document.querySelector('input[type*='+name+']'); // the * indicates it is looking for one instance of the args[0] value within the query. https://www.w3.org/TR/selectors/#attribute-substrings
  console.log('checking Type '+name)
  if (!field){
    console.log("checking ID: "+name)
    field = document.querySelector('input[id*='+name+']'); // extra checks added to maximise chances of finding it
    if (!field) {
      console.log('checking Name '+name)
      field = document.querySelector('input[name*='+name+']');
      if (!field) {
        console.log(name+ " FIELD NOT FOUND")
        console.log('-----')
        return null
      }
      else {
        console.log(name+ " FIELD FOUND: "+field)
        return field
      }
    } 
    else{
      console.log(name+ " FIELD FOUND: "+field)
      return field
    };
  } 
  else {
    console.log(name+ " FIELD FOUND: "+field)
    return field
  };
};

function findFieldFromNames(standardNames) {
  var field = null;
  var count = 0;
  while(!field && count < standardNames.length) {
    field = checkField(standardNames[count]);
    count++;
  };
  return field
};

function loadCred(data, pwd_field) {
  console.log(data)
  const email_field = findFieldFromNames(['email','logEmail']);
  const uname_field = findFieldFromNames(['signName','username','name']);
  pwd_field.value = data.password;;
  uname_field.value = data.username;
  email_field.value = data.email;;
}
function autofill(token) {
      const pwd_field = findFieldFromNames(['password','password-field','pwd','user_password']);
      if (pwd_field) {
        const options = {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer '+token
          }
        }; 
        fetch("https://passwordless.duckdns.org:8000/creds/getCredAutoFill?siteurl="+window.location.href,options)
        .then(function(data){
          if (data.status == 200) {
            return data.json()
          } else {
            console.log("No credential found for this page, please visit the site to add it")
            throw new Error("Credential not saved:"+data.status+' '+data.statusText)
          }
        })
        .then(function(data) {
          if(data.length == 1) {
            loadCred(data[0], pwd_field);
            delete data[0];
          }
          else {
            let ask_credentials = '[n]   email  |  username\n';
            for (i = 0;i <= data.length-1; i++) {
              const cred = data[i];
              ask_credentials = ask_credentials+'['+i+']   '+cred.email+' | '+cred.username+'\n';
              console.log(ask_credentials) //current
            }
            const choice = parseInt(prompt("Multiple Saved Credentials, please select the number of which to load:\n"+ask_credentials));
            loadCred(data[0], pwd_field)
            delete data[0];
          }
        }) 
      };
}

function main() {
  (async () => {
    const consent = await chrome.runtime.sendMessage({rq:'autofill_consent'})
    if (consent.consent) {
      const response = await chrome.runtime.sendMessage({rq:'token'});
      autofill(response.token);
    }
  })()
};


if (document.readyState !== 'loading') {
  main()
}
else {
  document.addEventListener("DOMContentLoaded", function(){
    main()
  })
}






