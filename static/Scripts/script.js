document.getElementById('loginForm').addEventListener('submit', function(event) 
{
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    if (email === 'admin@gmail.com' && password === 'password')
    {
        alert('Login successful!');
        errorMessage.textContent = '';
    }
     else 
    {
        errorMessage.textContent = 'Invalid username or password';
    }
});

function searchTable() 
{
    let input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("searchBar");
    filter = input.value.toUpperCase();
    table = document.getElementById("inventoryTable");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) 
    {
        tr[i].style.display = "none";
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) 
        {
            if (td[j]) 
            {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) 
                {
                    tr[i].style.display = "";
                    break;
                }
            }
        }
    }
}