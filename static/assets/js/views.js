
addView = document.getElementById("addView")
searchView = document.getElementById("searchView")
registerView = document.getElementById("registerView")
loginView = document.getElementById("loginView")
defaultView = document.getElementById("defaultView")

const openAddRestaurant = () => {
    loginView.style.display = "none"
    registerView.style.display = "none"
    addView.style.display = ""
    searchView.style.display = "none"
    defaultView.style.display = "none"
}

const openSearch = () => {
    loginView.style.display = "none"
    registerView.style.display = "none"
    addView.style.display = "none"
    searchView.style.display = ""
    defaultView.style.display = "none"
    onEnter()
}

const openRegister = () => {
    loginView.style.display = "none"
    registerView.style.display = ""
    addView.style.display = "none"
    searchView.style.display = "none"
    defaultView.style.display = "none"
}

const openLogin = () => {
    loginView.style.display = ""
    registerView.style.display = "none"
    addView.style.display = "none"
    searchView.style.display = "none"
    defaultView.style.display = "none"
}

// Existing tags are shown immediately
// If page is refreshed this comes handy
const onEnter = () => {
    let splitString = []
    try {
        const storedString = localStorage.getItem("tags")
        splitString = storedString.split(",")
    } catch (TypeError) {}

    showTags(splitString)
}

document.getElementById("openAddView").onclick = openAddRestaurant
document.getElementById("openSearchView").onclick = openSearch
try {
    document.getElementById("openLoginView").onclick = openLogin
    document.getElementById("openRegisterView").onclick = openRegister
} catch (TypeError) {
    
}
