const userForm = document.querySelector('#userForm')
userForm.addEventListener("submit", e => {
    e.preventDefault()
    const username = userForm["username"].value
    const email = userForm["email"].value
    const password = userForm["password"].value
    const response = fetch("/api/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, email, password})})
    const data = response.JSON
    console.log(data)
    userForm.reset()
})