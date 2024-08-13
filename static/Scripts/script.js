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

function searchTable() {
    let input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("searchBar");
    filter = input.value.toUpperCase();
    table = document.getElementById("inventoryTable");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        tr[i].style.display = "none";
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                }
            }
        }
    }
}

function addItem() {
    const table = document.getElementById("inventoryTable").getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td><input type="text" placeholder="Item ID"></td>
        <td><input type="text" placeholder="Item Type"></td>
        <td><input type="text" placeholder="Describtion"></td>
        <td><input type="number" placeholder="Quantity"></td>
        <td><input type="date" placeholder="Addition Date"></td>
        <td><input type="text" placeholder="Price"></td>
        <td>
            <button onclick="saveItem(this)" class="save-button">Save</button>
            <button onclick="cancelAdd(this)" class="cancel-button">Cancel</button>
        </td>
    `;
    toggleContainerSize(true);
}

function saveItem(button) {
    const row = button.parentNode.parentNode;
    const inputs = row.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        const value = inputs[i].value;
        const cell = inputs[i].parentNode;
        cell.innerHTML = value;
    }
    button.textContent = 'Edit';
    button.className = 'edit-button';
    button.onclick = function() {
        editItem(button);
    };
    const cancelButton = row.querySelector('.cancel-button');
    if (cancelButton) {
        cancelButton.remove();
    }
    toggleContainerSize(false);
}

function editItem(button) {
    const row = button.parentNode.parentNode;
    const cells = row.getElementsByTagName('td');
    for (let i = 0; i < cells.length - 1; i++) {
        const value = cells[i].innerText;
        cells[i].innerHTML = `<input type="text" value="${value}">`;
    }
    button.textContent = 'Save';
    button.className = 'save-button';
    button.onclick = function() {
        saveItem(button);
    };

    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancel';
    cancelButton.className = 'cancel-button';
    cancelButton.onclick = function() {
        cancelEdit(row, button);
    };
    button.parentNode.appendChild(cancelButton);
    toggleContainerSize(true);
}

function cancelEdit(row, button) {
    const cells = row.getElementsByTagName('td');
    for (let i = 0; i < cells.length - 1; i++) {
        const input = cells[i].querySelector('input');
        if (input) {
            cells[i].innerHTML = input.defaultValue;
        }
    }
    button.textContent = 'Edit';
    button.className = 'edit-button';
    button.onclick = function() {
        editItem(button);
    };
    const cancelButton = row.querySelector('.cancel-button');
    if (cancelButton) {
        cancelButton.remove();
    }
    toggleContainerSize(false);
}

function cancelAdd(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
    toggleContainerSize(false);
}

function deleteItem(button) {
    if (confirm("Are you sure you want to delete this item?")) {
        const row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
}

function toggleContainerSize(expand) {
    const container = document.getElementById('inventoryContainer');
    if (expand) {
        container.classList.add('expanded');
    } else {
        container.classList.remove('expanded');
    }
}