function emojiclicked(element)
{
    if (document.getElementById('password').innerHTML.length == 20)
    {
        document.getElementById('login_err').innerHTML = '10 images is enougth!';
        return
    }
    document.getElementById('password').innerHTML += element.innerHTML;
}

async function reset(code, password)
{
    var user     =  document.getElementById('email').innerHTML;
    var msg      = `/Resetsubmit?&email=${user}&code=${code}&password=${password}`;
    let response = await fetch(msg);
    let err      = await response.json();
    if ('OK' == err.code)
    {
        alert('Passwrod was reset, You\'ll be redirected to the login page')
        window.location.href = '/';
    } else {    
        document.getElementById('login_err').innerHTML = err.code;
    }
}

document.getElementById('Reset').onclick = function()
{
    var code     = window.location.href.split('&code=')[1]
    var password = document.getElementById('password').innerHTML
    if (8 > password.length)
    {
        document.getElementById('login_err').innerHTML = 'Password must be at least 4 images long';
        return false;
    }
    reset(code, password);    
}

document.getElementById('backspace').onclick = function()
{
    password = document.getElementById('password').innerHTML;   
    password = password.substring(0, password.length - 2);
    document.getElementById('password').innerHTML = password;
}


