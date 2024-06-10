document.addEventListener('DOMContentLoaded', function () {
    autocomplete();
    document.getElementById("serachform").addEventListener("submit", (e)=>{
        if (e.preventDefault) e.preventDefault();
        showPlayer(document.getElementById("search").value)
        return false;
    });
});


async function ajaxSearch(search) {
    if(search === '') return [];
    const response = await fetch(`/api/search/${search}`);
    const res = await response.json();
    return res.res;
}

function showPlayer(playername) {
    window.location.href = `/player/${playername}`;
}

function autocomplete() {
    let currentFocus;
    const inp = document.getElementById("search");
    let results = [];

    inp.addEventListener("input", async function (e) {
        showList(filterList(results));
        results = await ajaxSearch(inp.value);
        showList(filterList(results));
    });

    function filterList(list) {
        return list.filter((i) => i.toUpperCase().includes(inp.value.toUpperCase())).slice(0,5);
    }

    function showList(arr) {
        closeAllLists();
        currentFocus = -1;
        const a = document.createElement("DIV");
        a.setAttribute("id", inp.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        inp.parentNode.appendChild(a);
        for (const item of arr) {
            const b = document.createElement("DIV");
            b.innerHTML += item;
            b.innerHTML += "<input type='hidden' value='" + item + "'>";
            b.addEventListener("click", function(e) {
                showPlayer(this.getElementsByTagName("input")[0].value);
                closeAllLists();
            });
            a.appendChild(b);
        }
    }


    inp.addEventListener("keydown", function(e) {
        let x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            if (currentFocus > -1) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        const x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt !== x[i] && elmnt !== inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}