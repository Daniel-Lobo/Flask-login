async function login(msg)
{
    let response = await fetch(`/login?${msg}`);
    let data     = await response.json();
    document.getElementById('login_err').innerHTML = data.err;
}

async function register(msg)
{
    let response = await fetch(`/register?${msg}`);
    let data     = await response.json();
    document.getElementById('login_err').innerHTML = data.err;
} 

function get_user_input()
{
    data = {        
        email      : document.getElementById('email').value,         
        password   : document.getElementById('password').innerHTML     
    }
    data.msg =`&email=${data.email}&password=${data.password}`;
    return data
}

function validate_input(data)
{       
    if ('' == data.email)
    {
        document.getElementById('login_err').innerHTML = 'Please enter your email';
        return false;
    }   
    if (8 > data.password.length)
    {
        document.getElementById('login_err').innerHTML = 'Password must be at least 4 images long';
        return false;
    }  
    return true 
}

document.getElementById('login_button').onclick = function()
{
    var user = get_user_input();
    if (validate_input(user) == false)
    {
        return;
    }
    login(user.msg);    
}

document.getElementById('register_button').onclick = function()
{
    var user = get_user_input();
    if (validate_input(user) == false)
    {
        return;
    }
    register(user.msg);
}

function emojiclicked(element)
{
    if (document.getElementById('password').innerHTML.length == 20)
    {
        document.getElementById('login_err').innerHTML = '10 images is enougth!';
        return
    }
    document.getElementById('password').innerHTML += element.innerHTML;
}

document.getElementById('backspace').onclick = function()
{
    password = document.getElementById('password').innerHTML;   
    password = password.substring(0, password.length - 2);
    document.getElementById('password').innerHTML = password;
}
