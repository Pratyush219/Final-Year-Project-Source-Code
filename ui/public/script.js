window.onload = () => {
    console.log("Loaded");

    const uploadFileBtn = document.getElementById('chooseFile')
    const leftDropDown = document.querySelector(".dropdowns")
    const rightDropDown = document.querySelector(".dropdowns_right")

    addSingleCellRow = (parentTable, text, klassName, element) => {
        const row = document.createElement("tr")
        const cell = document.createElement(element)
        cell.className = klassName
        cell.textContent = text
        row.appendChild(cell)
        parentTable.appendChild(row)
    }
    fetch('/datasets')
        .then(response => {
            response.text().then(files => {
                console.log(files);
                files.split(',').forEach(file => {
                    if(file.split('.')[1] == "csv") {
                        const datasets = document.getElementsByClassName('datasets')[0]
                        const button = document.createElement('a')
                        button.className = 'dataset'
                        button.id = file
                        button.innerText = file
                        button.style.margin = "0"
                        button.style.textOverflow = "ellipsis"
                        datasets.appendChild(button)
                        button.addEventListener('click', () => {
                            // let tbl = document.getElementById("features")
                            // tbl.innerHTML = ''
                            console.log("Click")
                            uploadFileBtn.textContent = "Current File: "+file+"    Hover to change to another file.";
                            leftDropDown.innerHTML = ""
                            rightDropDown.innerHTML = ""
                            fetch('/results/' + file)
                                .then(response => {
                                    response.text().then(features => {
                                        //console.log(features);
                                        featuresDict = JSON.parse(features)
                                        console.log(featuresDict)
                                        display_features(featuresDict);
                                        // for (const [k, v] of Object.entries(featuresDict)) {
                                        //     addSingleCellRow(tbl, k, "feature", "th")
                                        //     v.forEach(feature => {
                                        //         addSingleCellRow(tbl, feature, "feature", "td")
                                        //     })
                                        // }
                                        // featuresArray.forEach(feature => {
                                        //     const row = document.createElement("tr")
                                        //     const cell = document.createElement("td")
                                        //     cell.className = "feature"
                                        //     cell.textContent = feature
                                        //     row.appendChild(cell)
                                        //     tbl.appendChild(row)
                                        // })
                                    })
                                })
                            fetch('/compare_results/'+file)
                            .then(response => {
                                console.log(response)
                                console.log('Plotting graphs');
                                const folder = file.split('.')[0];
                                var graphs = {
                                    "Features: Unreduced v/s Reduced": folder + "/features.jpg",
                                    "Features: Standard Apriori": folder + "/standard.png",
                                    "Runtime": folder + "/runtime.jpg"
                                }
                                show_graphs(graphs)
                            })
                        })
                    }
                });
            })

        })
}

function display_features(tableData){
    console.log("DISPLAY FEATURES CALLED!");
    // Get the dropdowns container element
    var dropdowns = document.querySelector(".dropdowns");
    dropdowns.innerHTML = "";

    // Loop through the tableData object and create a dropdown list for each key-value pair
    for (var key in tableData) {
        // Get the value array for the key
        var value = tableData[key];

        // Create a dropdown list with the key and the value
        var dropdown = createDropdownLeft(key, value);

        // Append the dropdown list to the dropdowns container
        dropdowns.appendChild(dropdown);
    }
}

function createDropdownLeft(id, data) {
    // Create a div element for the dropdown
    var dropdown = document.createElement("div");
    dropdown.className = "dropdown";
    dropdown.id = id;

    // Create a button element for the dropdown
    var button = document.createElement("button");
    button.innerHTML = 'Class Label: '+ id;
    button.onclick = function() {
        // Toggle the show class on the dropdown element
        dropdown.classList.toggle("show");
    };

    // Create a div element for the dropdown content
    var content = document.createElement("div");
    content.className = "dropdown-content";

    // Create a table element for the table data
    var table = document.createElement("table");

    // Loop through the data array and create a table row for each item
    for (var i = 0; i < data.length; i++) {
        // Create a table row element
        var row = document.createElement("tr");

        // Create a table cell element
        var cell = document.createElement("td");

        // Set the cell text to the data item
        cell.innerHTML = data[i];

        // Append the cell to the row
        row.appendChild(cell);

        // Append the row to the table
        table.appendChild(row);
    }

    // Append the table to the content
    content.appendChild(table);

    // Append the button and the content to the dropdown
    dropdown.appendChild(button);
    dropdown.appendChild(content);

    // Return the dropdown element
    return dropdown;
}

function show_graphs(graphs){
    var dropdowns = document.querySelector(".dropdowns_right")
    dropdowns.innerHTML = ""
    for (var key in graphs) {
        // Get the value array for the key
        var value = graphs[key];

        // Create a dropdown list with the key and the value
        var dropdown = createDropdownRight(key, value);

        // Append the dropdown list to the dropdowns container
        dropdowns.appendChild(dropdown);
    }
}

function createDropdownRight(id, data) {
    // Create a div element for the dropdown
    var dropdown = document.createElement("div");
    dropdown.className = "dropdown";
    dropdown.id = id;

    // Create a button element for the dropdown
    var button = document.createElement("button");
    button.className = "graph-image-btn"
    button.innerHTML = id;
    button.onclick = function() {
        // Toggle the show class on the dropdown element
        dropdown.classList.toggle("show");
    };

    // Create a div element for the dropdown content
    var content = document.createElement("div");
    content.className = "dropdown-content-img";

    // Create a table element for the table data
    var image = document.createElement("img");

    image.src = data;

    // Append the table to the content
    content.appendChild(image);

    // Append the button and the content to the dropdown
    dropdown.appendChild(button);
    dropdown.appendChild(content);

    // Return the dropdown element
    return dropdown;
}
