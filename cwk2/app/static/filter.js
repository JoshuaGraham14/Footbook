document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            if(button.name == "like" || button.name == "dislike")
            {
                request.open('POST', `/${button.name}`);
                request.setRequestHeader("ID", button.value);
                request.onload = () => {
                    const response = request.responseText;
                    if (response.indexOf("s") == -1)
                    {
                        var value = response.substring(0, response.length-1);
                        var code = response.substring(response.length - 1);
                        if(code == "a")
                        {
                        if(button.name == "like")
                        {
                            document.getElementById(button.id).innerHTML = "Likes: " + value;
                            document.getElementById(button.id).className = "btn btn-success";
                        }
                        else
                        {
                            document.getElementById(button.id).innerHTML = "Dislikes: " + value;
                            document.getElementById(button.id).className = "btn btn-danger";
                        }
                        }
                        else
                        {
                            if(button.name == "like")
                            {
                                document.getElementById(button.id).innerHTML = "Likes: " + value;
                            }
                            else
                            {
                                document.getElementById(button.id).innerHTML = "Dislikes: " + value;
                            }
                            document.getElementById(button.id).className = "btn btn-secondary";
                        }
                    }
                    else
                    {
                        const myArray = response.split("s");
                        value = myArray[0]
                        otherValue = myArray[1]
                        if(button.name == "like")
                        {
                            document.getElementById(button.id).innerHTML = "Likes: " + value;
                            document.getElementById("dislike"+button.value).innerHTML = "Dislikes: " + otherValue;
                            document.getElementById(button.id).className = "btn btn-success";
                            document.getElementById("dislike"+button.value).className = "btn btn-secondary";
                        }
                        else
                        {
                            document.getElementById(button.id).innerHTML = "Dislikes: " + value;
                            document.getElementById("like"+button.value).innerHTML = "Likes: " + otherValue;
                            document.getElementById(button.id).className = "btn btn-danger";
                            document.getElementById("like"+button.value).className = "btn btn-secondary";
                        }
                    }
                }; 
                request.send();
            }
        };
    });
})