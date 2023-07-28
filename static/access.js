async function access(user)
{
    var code     =  document.getElementById('access_code').value
    var msg      = `/access_submit?&email=${user}&code=${code}`
    let response = await fetch(msg);
    let err      = await response.json();
    if ('OK' == err.code)
    {
        document.body.innerHTML = err.msg;
    } else {    
        document.getElementById('login_err').innerHTML = err.code;
    }
}

document.getElementById('submit').onclick = function()
{
    var user = window.location.href.split('access?&user=')[1]
    access(user);    
}

