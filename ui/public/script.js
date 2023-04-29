window.onload = () => {
    console.log("Loaded");

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
                            let tbl = document.getElementById("features")
                            tbl.innerHTML = ''
                            console.log("Click");
                            fetch('/results/' + file)
                                .then(response => {
                                    response.text().then(features => {
                                        featuresDict = JSON.parse(features)
                                        console.log(featuresDict)
                                        
                                        for (const [k, v] of Object.entries(featuresDict)) {
                                            addSingleCellRow(tbl, k, "feature", "th")
                                            v.forEach(feature => {
                                                addSingleCellRow(tbl, feature, "feature", "td")
                                            })
                                        }
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
                        })
                    }
                });
            })

        })
}