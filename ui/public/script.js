window.onload = () => {
    console.log("Loaded");
    fetch('/datasets')
        .then(response => {
            response.text().then(files => {
                console.log(files);
                files.split(',').forEach(file => {
                    const datasets = document.getElementsByClassName('datasets')[0]
                    const button = document.createElement('button')
                    button.className = 'dataset'
                    button.id = file
                    button.innerText = file
                    datasets.appendChild(button)
                    datasets.appendChild(document.createElement('br'))
                    button.addEventListener('click', () => {
                        console.log("Click");
                        fetch('/results/' + file)
                        .then(response => {
                            response.text().then(features => console.log(features))
                        })
                    })
                });
            })

        })
}