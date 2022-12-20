document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#dropdownbutton-head, #dropdownbutton').forEach(button => {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            if (button.value != 0)
            {
                request.open('POST', `/filter`);
                request.setRequestHeader("ID", button.value);
                document.getElementById("dropdownbutton-head").innerHTML = button.textContent+" ";
                // request.onload = () => {
                //     const response = request.responseText;
                    
                // }; 
                request.send();
                location.reload();
            }
        };
    });
})