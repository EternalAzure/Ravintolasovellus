/* 
    When the search button is clicked, tags are updated and shown.
    Then request is made to the server and received restaurants are shown.
*/

let selectedTagsElement = document.getElementById("tags")
let scrollBar = document.getElementById("restaurants")

// 1.
const getNewTag = () => {
    console.log("getNewTag")
    let tags = []
    const tag = document.getElementById("tag").value
    document.getElementById("tag").value = ""
    if (tag !== '' && tag !== null) {
        tags.push(String(tag).toLocaleLowerCase())
    }
    
    try {
        const storedString = localStorage.getItem("tags")
        let splitString = storedString.split(",")
        tags = tags.concat(splitString)
    } catch (TypeError) {
        console.log("Empty localStorage")
    }
    
    localStorage.setItem("tags", tags)

    showTags(tags)
    makeRequest(tags)
}

// 2.a
const showTags = (tags) => {
    console.log("showTags")
    selectedTagsElement.innerHTML = ""
    tags.forEach(tag => {
        let newTag = document.createElement("div")
        newTag.innerText = tag
        selectedTagsElement.appendChild(newTag)
    })
}

// 2.b
const makeRequest = async (searchTags) => {
    console.log("makeRequest")
    const csrfToken = document.querySelector('input[name="csrf_token"]').value
    const searchMode = document.querySelector('input[name="mode"]:checked').value
    console.log("mode:", searchMode)
    console.log("tags:", searchTags)
    console.log("token:", csrfToken)

    const response = await fetch(baseUrl + "/api/search/tags" , {
        method: "POST",
        body: JSON.stringify({
            "tags": searchTags,
            "mode": searchMode
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Access-Control-Allow-Origin": baseUrl,
            "X-CSRFToken": csrfToken
        }
    })
    const result = await response.json()
    showResult(result)
}

// 3.
const showResult = (restaurants) => {
    console.log("showResult")
    scrollBar.innerHTML = ""

    if (restaurants.length === 0) {
        let noResult = noResultsElement()
        scrollBar.appendChild(noResult)
        return
    }
    
    restaurants.forEach(r => {
        scrollBar.appendChild(restaurantElement(r))
    })
}

const noResultsElement = () => {
    let element = document.createElement("div")
    element.className = "center"
    element.style.paddingTop = "5em"
    let text = document.createElement("h3")
    text.appendChild(document.createTextNode("Ei tuloksia"))

    const reset = document.createElement("form")
    reset.action = "/refresh"
    reset.method = "GET"
    const input = document.createElement("input")
    input.type = "submit"
    input.value = "Nollaa" 
    reset.appendChild(input)

    element.appendChild(text)
    element.appendChild(document.createElement("br"))
    element.appendChild(reset)

    return element
}

const restaurantElement = (r) => {
    let restaurantElement = document.createElement("div")
    let title = document.createElement("h3")
    title.innerText = `${r.name} | ${r.rating}`
    let lineBreak = document.createElement("br")

    let info = document.createElement("a")
    let linkText = document.createTextNode("Katso tiedot | ")
    info.appendChild(linkText)
    info.href = "/info/" + r.id

    let review = document.createElement("a")
    linkText = document.createTextNode("Arvostelut | ")
    review.appendChild(linkText)
    review.href = "/review/" + r.id

    let city = document.createTextNode(r.city)
    let hr = document.createElement("hr")

    restaurantElement.appendChild(title)
    restaurantElement.appendChild(lineBreak)
    restaurantElement.appendChild(info)
    restaurantElement.appendChild(review)
    restaurantElement.appendChild(city)
    restaurantElement.appendChild(hr)

    return restaurantElement
}


const clearTags = () => {
    console.log("clearTags")
    localStorage.removeItem("tags")
    selectedTagsElement.innerHTML = ""
}

const searchByName = async () => {
    console.log("searchByName")
    const name = document.getElementById("name").value
    const csrfToken = document.querySelector('input[name="csrf_token"]').value
    document.getElementById("name").value = ""
    const response = await fetch(baseUrl + "/api/search/name" , {
        method: "POST",
        body: JSON.stringify({
            "name": name
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Access-Control-Allow-Origin": baseUrl,
            "X-CSRFToken": csrfToken
        }
    })
    let result = await response.json()
    showResult(result)
}

document.getElementById("clearTags").onclick = clearTags
document.getElementById("search").onclick = getNewTag
document.getElementById("searchByName").onclick = searchByName