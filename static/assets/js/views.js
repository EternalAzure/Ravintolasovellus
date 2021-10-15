
addView = document.getElementById("addView")
searchView = document.getElementById("searchView")
registerView = document.getElementById("registerView")
loginView = document.getElementById("loginView")

const openAddRestaurant = () => {
    loginView.style.display = "none"
    registerView.style.display = "none"
    addView.style.display = ""
    searchView.style.display = "none"
}

const openSearch = () => {
    loginView.style.display = "none"
    registerView.style.display = "none"
    addView.style.display = "none"
    searchView.style.display = ""
    onEnter()
}

const openRegister = () => {
    loginView.style.display = "none"
    registerView.style.display = ""
    addView.style.display = "none"
    searchView.style.display = "none"
}

const openLogin = () => {
    loginView.style.display = ""
    registerView.style.display = "none"
    addView.style.display = "none"
    searchView.style.display = "none"
}

// Existing tags are shown immediately
// If page is refreshed this comes handy
const onEnter = () => {
    element.innerHTML = ""
    let splitString = []
    try {
        const storedString = localStorage.getItem("tags")
        splitString = storedString.split(",")
    } catch (TypeError) {
        console.log("Empty localStorage")
    }

    splitString.forEach(tag => {
        let newTag = document.createElement("div")
        newTag.innerText = tag
        element.appendChild(newTag)
    })
}

document.getElementById("openAddView").onclick = openAddRestaurant
document.getElementById("openSearchView").onclick = openSearch
try {
    document.getElementById("openLoginView").onclick = openLogin
    document.getElementById("openRegisterView").onclick = openRegister
} catch (TypeError) {
    
}
