/* 
    Events flow in order from 1 to 4.
    When search button is clicked, tags are updated and shown.
    Then request is made to server and resulting restaurants are shown.

*/

let element = document.getElementById("tags")
let scrollBar = document.getElementById("restaurants")

// 1.
const getNewTag = () => {
    console.log("getNewTag")
    let tags = []
    let tag = document.getElementById("tag").value
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
}

// 2.
const showTags = (tags) => {
    console.log("showTags")
    element.innerHTML = ""
    tags.forEach(tag => {
        let newTag = document.createElement("div")
        newTag.innerText = tag
        element.appendChild(newTag)
    })

    sendTags(tags)
}

// 3.
const sendTags = async (searchTags) => {
    console.log("sendTags")
    const searchMode = document.querySelector('input[name="mode"]:checked').value
    const csrfToken = document.querySelector('input[name="csrf_token"]').value
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
    let result = await response.json()
    console.log("Response:", result)

    showResult(result)
}

// 4.
const showResult = (restaurants) => {
    console.log("showResult")
    scrollBar.innerHTML = ""
    if (restaurants.length === 0) {
        console.log("empty list")
        noResult = noResultsElement()
        scrollBar.appendChild(noResult)
        return
    }
    
    restaurants.forEach(r => {
        e = restaurantElement(r)
        scrollBar.appendChild(e)
    })
}

// Build no results element
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
    title.innerText = r.name
    let lineBreak = document.createElement("br")
    let link = document.createElement("a")
    let linkText = document.createTextNode("Katso tiedot")
    link.appendChild(linkText)
    link.href = "/restaurant/" + r.id
    let hr = document.createElement("hr")

    restaurantElement.appendChild(title)
    restaurantElement.appendChild(lineBreak)
    restaurantElement.appendChild(link)
    restaurantElement.appendChild(hr)

    return restaurantElement
}


const clearTags = () => {
    console.log("clearTags")
    localStorage.removeItem("tags")
    element.innerHTML = ""
}

document.getElementById("clearTags").onclick = clearTags
document.getElementById("search").onclick = getNewTag